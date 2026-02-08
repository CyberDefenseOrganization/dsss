from click import command
import uvicorn
from dsss.checks.base import BaseCheck
from dsss.checks.ftp import FTPCheck
from dsss.checks.http import HTTPCheck
from dsss.checks.ldap import LDAPCheck
from dsss.checks.random import RandomCheck
from dsss.checks.smb import SMBCheck
from dsss.checks.ssh import SSHCheck
from dsss.checks.tcp import TCPCheck
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
    teams = {}
    team_names = [f"Team{i}" for i in range(1, 13)]

    SCORING_USER = "scoring"
    SCORING_PASSWORD = "scoring"
    LDAP_USER = "analyst5"
    LDAP_PASSWORD = "bb123#123"
    TIMEOUT = 20

    for index, team_name in enumerate(team_names):
        team_number = index + 1 + 20

        services = [
            (
                "Router SSH",
                10,
                SSHCheck(
                    f"172.16.{team_number}.1",
                    SCORING_USER,
                    SCORING_PASSWORD,
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Router ICMP",
                10,
                PingCheck(
                    f"172.16.{team_number}.1",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Router WebUI",
                10,
                HTTPCheck(
                    f"http://172.16.{team_number}.1:80",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Backup ICMP",
                10,
                PingCheck(
                    f"172.16.{team_number}.10",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Backup SSH",
                10,
                SSHCheck(
                    f"172.16.{team_number}.10",
                    SCORING_USER,
                    SCORING_PASSWORD,
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Backup FTP",
                10,
                FTPCheck(
                    f"172.16.{team_number}.10",
                    SCORING_USER,
                    SCORING_PASSWORD,
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Backup FileBrowser",
                10,
                HTTPCheck(
                    f"http://172.16.{team_number}.10:8080/",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "IRC ICMP",
                10,
                PingCheck(
                    f"172.16.{team_number}.20",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "IRC SSH",
                10,
                SSHCheck(
                    f"172.16.{team_number}.20",
                    SCORING_USER,
                    SCORING_PASSWORD,
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "IRC IRC Server",
                10,
                TCPCheck(
                    host=f"172.16.{team_number}.20",
                    port=6667,
                    messages=None,
                    expected_response=None,
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "IRC TheLounge",
                10,
                HTTPCheck(
                    f"http://172.16.{team_number}.20:8080",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "AmogOS ICMP",
                10,
                PingCheck(
                    f"172.16.{team_number}.30",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "AmogOS SSH",
                10,
                SSHCheck(
                    f"172.16.{team_number}.30",
                    username=SCORING_USER,
                    password="bb123#123",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "AmogOS Minecraft",
                10,
                TCPCheck(
                    host=f"172.16.{team_number}.30",
                    port=25565,
                    messages=None,
                    expected_response=None,
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "AmogOS Grafana",
                10,
                HTTPCheck(
                    f"http://172.16.{team_number}.30:3000",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "IRC TheLounge",
                10,
                HTTPCheck(
                    f"http://172.16.{team_number}.20:8080",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Windows Server ICMP",
                5,
                PingCheck(f"172.16.{team_number}.40", timeout_seconds=TIMEOUT),
            ),
            (
                "Windows Server RDP",
                5,
                TCPCheck(
                    host=f"172.16.{team_number}.40",
                    port=3389,
                    messages=None,
                    expected_response=None,
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Windows Server IIS HTTP",
                5,
                HTTPCheck(
                    f"http://172.16.{team_number}.40:80",
                    "IIS Windows Server",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Windows Server LDAP",
                5,
                LDAPCheck(
                    f"ldap://172.16.{team_number}.40",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Windows Workstation ICMP",
                5,
                PingCheck(
                    f"172.16.{team_number}.50",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Windows Workstation SSH",
                5,
                SSHCheck(
                    f"172.16.{team_number}.50",
                    username=SCORING_USER,
                    password="bb123#123",
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Windows Workstation RDP",
                5,
                TCPCheck(
                    host=f"172.16.{team_number}.50",
                    port=3389,
                    messages=None,
                    expected_response=None,
                    timeout_seconds=TIMEOUT,
                ),
            ),
            (
                "Windows Workstation SMB",
                5,
                TCPCheck(
                    host=f"172.16.{team_number}.50",
                    port=445,
                    messages=None,
                    expected_response=None,
                    timeout_seconds=TIMEOUT,
                ),
            ),
        ]

        teams[team_name] = make_team(team_name, services)

    # teams = {name: make_team(name, service_defs) for name in team_names}

    config = Config(
        port=8080,
        target_round_time=35,
        teams=teams,
        admin_username="admin",
        admin_password="bb123#123",
        database_path="rounds.db",
        max_concurrent_checks=1000,
    )

    return config


def main():
    uvicorn.run("dsss.api.api:app", host="0.0.0.0", port=8080, log_level="error")


if __name__ == "__main__":
    main()
