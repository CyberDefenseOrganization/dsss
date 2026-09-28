from typing import override
import asyncio

from dsss.checks.base import AsyncCheck, Host, Port, Timeout


class TCPCheck(AsyncCheck):
    name = "TCP"

    messages: list[str] | None
    expected_response: str | None

    def __init__(
        self,
        host: Host,
        port: Port,
        messages: list[str] | None = None,
        expected_response: str | None = None,
        timeout_seconds: Timeout = 10,
    ) -> None:
        self.messages = messages
        self.expected_response = expected_response

        super().__init__(host, port, timeout_seconds=timeout_seconds)

    @override
    async def check(self) -> tuple[bool, str | None]:
        try:
            async with asyncio.timeout(self.timeout_seconds):
                reader, writer = await asyncio.open_connection(self.host, self.port)
                try:
                    if self.messages is None:
                        return (True, "Service is online")

                    for message in self.messages:
                        writer.write(message.encode())
                        await writer.drain()

                    data = await reader.read(100)
                    if (
                        self.expected_response is None
                        or self.expected_response in data.decode()
                    ):
                        return (True, "Expected response found")
                    return (False, "Unexpected server response")
                finally:
                    writer.close()
                    await writer.wait_closed()
        except TimeoutError:
            return (False, "Timeout occurred")
