import asyncio

from dsss.checks.base import BaseCheck
from dsss.engine.engine import Engine
from dsss.config import Config
from dsss.team import Team
from dsss.service import Service

from dsss.checks.ping import PingCheck


def make_team(name: str, service_list: list[tuple[str, int, BaseCheck]]) -> Team:
    services: dict[str, Service] = {}

    for name, points, check in service_list:
        services[name] = Service(name, points, check)

    return Team(
        name=name,
        services=services,
    )


async def main():
    service_defs = [
        ("Ping", 100, PingCheck("1.1.1.1", 5)),
    ]

    team_names = [f"Team{i}" for i in range(1, 100)]
    teams = {name: make_team(name, service_defs) for name in team_names}

    config = Config(
        target_round_time=1,
        teams=teams,
        admin_username="admin",
        admin_password="bb123#123",
        database_path="rounds.db",
    )

    engine = Engine(config)
    await engine.start()


if __name__ == "__main__":
    asyncio.run(main())
