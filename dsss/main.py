import uvicorn

from dsss.checks.base import BaseCheck
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
        ("Ping", 100, PingCheck("1.1.1.1", 5)),
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
