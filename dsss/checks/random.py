import random
from typing import override

from dsss.checks.base import BaseCheck


class RandomCheck(BaseCheck):
    likelihood: float

    def __init__(self, likelihood: float = 0.5) -> None:
        self.likelihood = likelihood
        super().__init__("0.0.0.0", None, 10)

    @override
    async def check(self) -> tuple[bool, str | None]:
        if random.random() > 1 - self.likelihood:
            return (True, "lucky")
        else:
            return (False, "unlucky")
