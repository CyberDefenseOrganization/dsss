import uvicorn

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
        ("Ping", 100, RandomCheck(0.5)),
        ("Ping1", 100, RandomCheck(0.5)),
        ("Ping2", 100, RandomCheck(0.5)),
        ("Ping3", 100, RandomCheck(0.5)),
        ("Ping4", 100, RandomCheck(0.5)),
        ("Ping5", 100, RandomCheck(0.5)),
        ("Ping6", 100, RandomCheck(0.5)),
        ("Ping7", 100, RandomCheck(0.5)),
        ("Ping8", 100, RandomCheck(0.5)),
        ("Ping9", 100, RandomCheck(0.5)),
        ("Ping10", 100, RandomCheck(0.5)),
        ("Ping11", 100, RandomCheck(0.5)),
        ("Ping12", 100, RandomCheck(0.5)),
        ("Ping13", 100, RandomCheck(0.5)),
        ("Ping14", 100, RandomCheck(0.5)),
        ("Ping15", 100, RandomCheck(0.5)),
        ("Ping16", 101, RandomCheck(0.5)),
        ("Ping17", 100, RandomCheck(0.5)),
        ("Ping18", 100, RandomCheck(0.5)),
        ("Ping19", 100, RandomCheck(0.5)),
        ("Ping20", 100, RandomCheck(0.5)),
        ("Ping21", 100, RandomCheck(0.5)),
        ("Ping21", 100, RandomCheck(0.5)),
        ("Ping22", 100, RandomCheck(0.5)),
        ("Ping23", 100, RandomCheck(0.5)),
    ]

    team_names = [f"Team{i}" for i in range(1, 12)]
    teams = {name: make_team(name, service_defs) for name in team_names}

    config = Config(
        port=8080,
        target_round_time=10,
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
