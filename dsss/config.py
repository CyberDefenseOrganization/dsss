from dsss.team import Team

from dataclasses import dataclass


@dataclass
class Config:
    event_name_long: str
    event_name_short: str
    organization_name_long: str
    organization_name_short: str
    target_round_time: float
    port: int
    num_worker_processes: int
    database_path: str
    admin_username: str
    admin_password: str
    teams: dict[str, Team]

