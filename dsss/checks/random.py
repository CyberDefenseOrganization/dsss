import random
from typing import Annotated, override
from pydantic import Field

from dsss.checks.base import AsyncCheck


class RandomCheck(AsyncCheck):
    name = "Random"

    likelihood: float

    def __init__(self, likelihood: Annotated[float, Field(ge=0, le=1)] = 0.5) -> None:
        self.likelihood = likelihood
        super().__init__("0.0.0.0", None, 10)

    @override
    async def check(self) -> tuple[bool, str | None]:
        if random.random() > 1 - self.likelihood:
            return (True, "lucky")
        else:
            return (False, "unlucky")
