from typing import override
import asyncio

from dsss.checks.base import BaseCheck


class PingCheck(BaseCheck):
    @override
    async def check(self) -> tuple[bool, str]:
        reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
        writer.write("hello, world".encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()

        return (True, "BASED")
