from abc import ABC, abstractmethod


class BaseCheck(ABC):
    timeout_seconds: int = 10

    @abstractmethod
    async def check(self) -> tuple[bool, str]:
        pass
