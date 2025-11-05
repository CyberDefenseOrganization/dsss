from dataclasses import dataclass

from dsss.service import Service


@dataclass
class Team:
    name: str
    services: dict[str, Service]
