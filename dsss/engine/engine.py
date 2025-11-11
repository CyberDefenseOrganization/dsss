from dataclasses import dataclass
import time
import sqlite3
import asyncio
from asyncio import Task
from typing import TypedDict

from dsss.config import Config
from dsss.service import Service
from dsss.team import Team
from dsss.logger import get_logger

logger = get_logger("Engine")


@dataclass
class ServiceStatus:
    online: bool
    message: str


class TeamOverview(TypedDict):
    score: int
    services: dict[str, ServiceStatus]


class Engine:
    config: Config
    db: sqlite3.Connection

    paused: bool
    current_round: int

    # epoch time when last round finished
    last_round_finished: float

    def __init__(self, config: Config) -> None:
        self.config = config
        self.paused = False
        self.current_round = 0
        self.last_round_finished = time.time()

        self.db = sqlite3.connect(self.config.database_path)
        _ = self.db.execute("""
            CREATE TABLE IF NOT EXISTS results (
                round INTEGER,
                team TEXT,
                service TEXT,
                success INTEGER,
                message TEXT,
                timestamp REAL
            )
        """)

        self.current_round = (
            self.db.execute("SELECT MAX(round) FROM results").fetchone()[0] or 0
        )

    async def start(self):
        logger.info("Starting Engine")

        if self.current_round != 0:
            logger.info(
                f"Existing rounds found, resuming at round: {self.current_round}"
            )

        while True:
            time_before = time.time()
            if not self.paused:
                await self.run_round()

            time_taken = time.time() - time_before
            logger.info(
                f"Round {self.current_round} completed in {time_taken:01.5f} seconds"
            )

            time_to_sleep = self.config.target_round_time - time_taken

            if time_to_sleep < 0:
                logger.warning(
                    f"Round checks took longer than specified target round time of {self.config.target_round_time} seconds by {abs(time_to_sleep):01.2f} seconds"
                )

            self.last_round_finished = time.time()
            await asyncio.sleep(max(0, time_to_sleep))

    async def run_round(self):
        self.current_round += 1

        tasks: list[Task[tuple[str, str, bool, str | None]]] = []
        for _, team in self.config.teams.items():
            for _, service in team.services.items():
                tasks.append(asyncio.create_task(self._run_check(team, service)))

        results = await asyncio.gather(*tasks)
        self._store_results(self.current_round, results)

    def get_time_to_next_round(self) -> float:
        return max(
            0, self.config.target_round_time - (time.time() - self.last_round_finished)
        )

    def get_scores_round(self, round_id: int) -> dict[str, int]:
        """
        Returns scores up until the specified round
        """
        rows: list[tuple[str, str, int]] = self.db.execute(
            "SELECT team, service, success FROM results WHERE round <= (?)",
            (round_id,),
        ).fetchall()

        scores: dict[str, int] = {}
        for team, service, success in rows:
            if team not in scores:
                scores[team] = 0

            scores[team] += (
                self.config.teams[team].services[service].point_value * success
            )

        return scores

    def get_scores(self) -> dict[str, int]:
        """
        Returns current scores
        """
        return self.get_scores_round(self.current_round)

    def get_rounds_cumulative(self) -> dict[str, list[int]]:
        """
        Returns the cumulative score at each round in the following format:
        dict[team, list[score]]
        """
        teams = self.get_rounds()

        cumulative_teams: dict[str, list[int]] = {}

        for team, rounds in teams.items():
            if team not in cumulative_teams:
                cumulative_teams[team] = []

            for index, round in enumerate(rounds):
                cumulative_teams[team].append(round)

                if index != 0:
                    cumulative_teams[team][index] += cumulative_teams[team][index - 1]

        return cumulative_teams

    def get_rounds(self) -> dict[str, list[int]]:
        """
        Returns the scores attained each round in the following format:
        dict[team, list[score]]
        """
        rows: list[tuple[str, str, int, int]] = self.db.execute(
            "SELECT team, service, round, success FROM results"
        ).fetchall()

        rounds: dict[str, dict[int, int]] = {}

        for team, service, current_round, success in rows:
            if team not in rounds:
                rounds[team] = {}

            if current_round not in rounds[team]:
                rounds[team][current_round] = 0

            rounds[team][current_round] += (
                self.config.teams[team].services[service].point_value * success
            )

        rounds_list: dict[str, list[int]] = {}

        for team in rounds:
            max_round = max(rounds[team].keys())
            rounds_list[team] = [rounds[team].get(i, 0) for i in range(max_round + 1)][
                1::
            ]

        return rounds_list

    def get_overview(self) -> dict[str, TeamOverview]:
        """
        Returns the results of the most recent round
        """
        rows: list[tuple[str, str, int, str]] = self.db.execute(
            "SELECT team, service, success, message FROM results"
        ).fetchall()
        scores = self.get_scores()
        overview: dict[str, TeamOverview] = {}

        for team, service, success, message in rows:
            if team not in overview:
                overview[team] = {"score": scores[team], "services": {}}

            overview[team]["services"][service] = ServiceStatus(success > 0, message)

        return overview

    async def _run_check(
        self, team: Team, service: Service
    ) -> tuple[str, str, bool, str | None]:
        try:
            success, msg = await asyncio.wait_for(
                service.check.check(),
                timeout=service.check.timeout_seconds,
            )
            return (team.name, service.name, success, msg)
        except asyncio.TimeoutError:
            return (team.name, service.name, False, "Timeout occurred")

        except Exception as e:
            logger.warning(
                f"Unhandled exception while performing check '{service.name}': {repr(e)}"
            )
            return (team.name, service.name, False, f"Error: {e}")

    def _store_results(
        self, round_id: int, results: list[tuple[str, str, bool, str | None]]
    ):
        with self.db:
            _ = self.db.executemany(
                "INSERT INTO results (round, team, service, success, message, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (round_id, team, service, int(success), msg or "", time.time())
                    for team, service, success, msg in results
                ],
            )
