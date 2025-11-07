from typing import override
import random

from dsss.checks.base import BaseCheck


class RandomCheck(BaseCheck):
    liklihood: float

    def __init__(self, liklihood: float = 0.5) -> None:
        self.liklihood = liklihood
        super().__init__("0.0.0.0", None, 10)

    @override
    async def check(self) -> tuple[bool, str | None]:
        if random.random() > self.liklihood:
            return (True, "lucky")
        else:
            return (False, "unlucky")
