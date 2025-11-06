from abc import ABC, abstractmethod


class BaseCheck(ABC):
    host: str
    port: int | None
    timeout_seconds: int = 10

    def __init__(self, host: str, port: int | None, timeout_seconds: int) -> None:
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds

    @abstractmethod
    async def check(self) -> tuple[bool, str | None]:
        pass
