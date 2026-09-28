import asyncio
from typing import Literal, override

from dsss.checks.base import AsyncCheck, Host, Port, Timeout

import asyncssh


class SSHCheck(AsyncCheck):
    name = "SSH"

    username: str | None
    password: str | None
    availability_only: bool

    command: str | None
    expected_output: str

    def __init__(
        self,
        host: Host,
        username: str | None = None,
        password: str | None = None,
        port: Port = 22,
        timeout_seconds: Timeout = 10,
        command: str | None | Literal[False] = "echo scoring",
        expected_output: str = "scoring",
        availability_only: bool = False,
    ) -> None:
        if not availability_only and (username is None or password is None):
            raise ValueError("username and password are required for SSH login checks")
        super().__init__(host, port, timeout_seconds)
        self.username = username
        self.password = password
        self.command = None if command is False else command
        self.expected_output = expected_output
        self.availability_only = availability_only

    @override
    async def check(self) -> tuple[bool, str | None]:
        try:
            if self.availability_only:
                async with asyncio.timeout(self.timeout_seconds):
                    key = await asyncssh.get_server_host_key(self.host, self.port)
                if key is None:
                    return (False, "SSH server did not provide a host key.")
                return (True, "SSH appears to be up.")

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
