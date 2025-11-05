from dataclasses import dataclass

from dsss.checks.base import BaseCheck


@dataclass
class Service:
    name: str
    point_value: int
    check: BaseCheck
