from dsss.team import Team

from dataclasses import dataclass


@dataclass
class Config:
    target_round_time: int
    port: int
    database_path: str
    admin_username: str
    admin_password: str
    teams: dict[str, Team]
