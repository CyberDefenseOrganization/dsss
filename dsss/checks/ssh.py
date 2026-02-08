from math import exp
from typing import override

from dsss.checks.base import BaseCheck

import asyncssh


class SSHCheck(BaseCheck):
    username: str
    password: str

    command: str | None
    expected_output: str

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = 22,
        timeout_seconds: float = 10,
        command: str | None = "echo scoring",
        expected_output: str = "scoring",
    ) -> None:
        super().__init__(host, port, timeout_seconds)
        self.username = username
        self.password = password
        self.command = command
        self.expected_output = expected_output

    @override
    async def check(self) -> tuple[bool, str | None]:
        try:
            async with asyncssh.connect(
                self.host,
                self.port,
                username=self.username,
                password=self.password,
                known_hosts=None,
            ) as conn:
                if self.command is None:
                    return (True, "SSH appears to be up.")

                result = await conn.run(self.command, check=False)
                await conn.run("exit")

                stdout = str(result.stdout).strip()
                expected_output = self.expected_output.strip()

                if stdout == expected_output:
                    return (
                        True,
                        f'Ran command "{self.command}" as user "{self.username}".\nRecieved: "{stdout}"',
                    )
                else:
                    return (
                        False,
                        f'Ran command "{self.command}" as user "{self.username}".\nRecieved: "{stdout}", expected: "{expected_output}"',
                    )
        except asyncssh.PermissionDenied:
            return (
                False,
                f"Permission denied for user {self.username} on host {self.host}",
            )
