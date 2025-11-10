import uvicorn
import random
from dsss.checks.base import BaseCheck
from dsss.checks.random import RandomCheck
from dsss.config import Config
from dsss.team import Team
from dsss.service import Service
from dsss.checks.ping import PingCheck


def make_team(name: str, service_list: list[tuple[str, int, BaseCheck]]) -> Team:
    services: dict[str, Service] = {}

    for service_name, points, check in service_list:
        services[service_name] = Service(service_name, points, check)

    return Team(
        name=name,
        services=services,
    )


def get_config() -> Config:
    service_defs = [
        ("Web Content", 100, RandomCheck(0.5)),
        ("SSH Daemon", 100, RandomCheck(0.5)),
        ("Test Fortnite Long", 100, RandomCheck(0.5)),
        ("Ping3", 100, RandomCheck(random.random())),
        ("Ping4", 100, RandomCheck(random.random())),
        ("Ping5", 100, RandomCheck(random.random())),
        ("Ping6", 100, RandomCheck(random.random())),
        ("Ping7", 100, RandomCheck(random.random())),
        ("Ping8", 100, RandomCheck(random.random())),
        ("Ping9", 100, RandomCheck(random.random())),
        ("Ping10", 100, RandomCheck(random.random())),
        ("Ping11", 100, RandomCheck(random.random())),
        ("Ping12", 100, RandomCheck(random.random())),
        ("Ping13", 100, RandomCheck(random.random())),
        ("Ping14", 100, RandomCheck(random.random())),
        ("Ping15", 100, RandomCheck(random.random())),
        ("Ping16", 101, RandomCheck(random.random())),
        ("Ping17", 100, RandomCheck(random.random())),
        ("Ping18", 100, RandomCheck(random.random())),
        ("Ping19", 100, RandomCheck(random.random())),
        ("Ping20", 100, RandomCheck(random.random())),
        ("Ping21", 100, RandomCheck(random.random())),
        ("Ping21", 100, RandomCheck(random.random())),
        ("Ping22", 100, RandomCheck(random.random())),
        ("Ping23", 100, RandomCheck(random.random())),
    ]

    team_names = [f"Team{i}" for i in range(1, 12)]
    teams = {name: make_team(name, service_defs) for name in team_names}

    config = Config(
        port=8080,
        target_round_time=180,
        teams=teams,
        admin_username="admin",
        admin_password="bb123#123",
        database_path="rounds.db",
    )

    return config


def main():
    uvicorn.run("dsss.api.api:app", host="0.0.0.0", port=8080, log_level="error")


if __name__ == "__main__":
    main()
