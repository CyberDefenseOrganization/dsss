import aioping
from typing import override

from dsss.checks.base import AsyncCheck, Host, Timeout


class PingCheck(AsyncCheck):
    name = "Ping"

    def __init__(self, host: Host, timeout_seconds: Timeout = 10) -> None:
        super().__init__(host, None, timeout_seconds=timeout_seconds)

    @override
    async def check(self) -> tuple[bool, str | None]:
        try:
            delay_ms = (
                await aioping.ping(
                    self.host,
                    timeout=self.timeout_seconds,
                )
                * 1000
            )
            return (True, f"ping took {delay_ms}ms")
        except TimeoutError:
            return (False, "timeout")
