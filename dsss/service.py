from dataclasses import dataclass

from dsss.checks.base import BaseCheck


@dataclass
class Service:
    id: str
    point_value: int
    check: BaseCheck
    host: str | None
    name: str
