from typing import override
import asyncio

from dsss.checks.base import BaseCheck


class TCPCheck(BaseCheck):
    messages: list[str] | None
    expected_response: str | None

    def __init__(
        self,
        host: str,
        port: int,
        messages: list[str] | None,
        expected_response: str | None,
        timeout_seconds: float = 10,
    ) -> None:
        self.messages = messages
        self.expected_response = expected_response

        super().__init__(host, port, timeout_seconds=timeout_seconds)

    @override
    async def check(self) -> tuple[bool, str | None]:
        reader, writer = await asyncio.open_connection(self.host, self.port)

        if self.messages is None:
            return (True, "Service is online")

        for message in self.messages:
            writer.write(message.encode())
            await writer.drain()

        data = await reader.read(100)
        print(f"Received: {data.decode()!r}")

        print("Close the connection")
        writer.close()
        await writer.wait_closed()

        if self.expected_response or "" in data.decode():
            return (True, "Expected response found")
        else:
            return (False, "Unexpected server response")
