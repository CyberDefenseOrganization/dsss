from abc import ABC, abstractmethod


class BaseCheck(ABC):
    host: str
    port: int | None
    timeout_seconds: float = 30

    def __init__(self, host: str, port: int | None, timeout_seconds: float) -> None:
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds

class AsyncCheck(BaseCheck, ABC):
    @abstractmethod
    async def check(self) -> tuple[bool, str | None]:
        pass

class SyncCheck(BaseCheck, ABC):
    @abstractmethod
    def check(self) -> tuple[bool, str | None]:
        pass
