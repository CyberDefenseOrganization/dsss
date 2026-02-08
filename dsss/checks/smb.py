from typing import override
from dsss.checks.base import BaseCheck

import asyncio
from smbclient import register_session, listdir


class SMBCheck(BaseCheck):
    """
    Performs an anonymous LDAP connection against a specified server
    """

    def __init__(
        self,
        host: str,
        port: int,
        timeout_seconds: float = 10,
    ) -> None:
        super().__init__(host, port, timeout_seconds=timeout_seconds)

    @override
    async def check(self) -> tuple[bool, str | None]:
        # blocking
        def do_bind():
            register_session(self.host, username="scoring", password="bb123#123")
            for filename in listdir(f"\\\\{self.host}"):
                print(filename)
            return True

        response = await asyncio.to_thread(do_bind)
        return (response, None)
