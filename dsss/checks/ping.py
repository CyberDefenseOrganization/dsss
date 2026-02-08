import socket
import aioping
from typing import override

from dsss.checks.base import BaseCheck


class PingCheck(BaseCheck):
    def __init__(self, host: str, timeout_seconds: float = 10) -> None:
        super().__init__(host, None, timeout_seconds=timeout_seconds)

    @override
    async def check(self) -> tuple[bool, str | None]:
        try:
            delay_ms: int = (
                await aioping.ping(
                    self.host,
                    timeout=int(self.timeout_seconds * 1000),
                    family=socket.AddressFamily.AF_INET,
                )
                * 1000
            )
            return (True, f"ping took {delay_ms}ms")
        except TimeoutError:
            return (False, "timeout")
