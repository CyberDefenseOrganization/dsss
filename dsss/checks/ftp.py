from typing import override
import aioftp

from dsss.checks.base import AsyncCheck, Host, Port, Timeout


class FTPCheck(AsyncCheck):
    name = "FTP"

    username: str | None
    password: str | None
    availability_only: bool

    def __init__(
        self,
        host: Host,
        username: str | None = None,
        password: str | None = None,
        port: Port = 21,
        timeout_seconds: Timeout = 10,
        availability_only: bool = False,
    ) -> None:
        if not availability_only and (username is None or password is None):
            raise ValueError("username and password are required for FTP login checks")
        super().__init__(host, port, timeout_seconds=timeout_seconds)

        self.username = username
        self.password = password
        self.availability_only = availability_only

    @override
    async def check(self) -> tuple[bool, str | None]:
        try:
            if self.availability_only:
                client = aioftp.Client(
                    connection_timeout=self.timeout_seconds,
                    socket_timeout=self.timeout_seconds,
                )
                try:
                    await client.connect(self.host, self.port or 21)
                    return (True, "FTP appears to be up.")
                finally:
                    client.close()

            async with aioftp.Client.context(
                self.host, self.port or 21, self.username, self.password
            ) as client:
                await client.make_directory("scoring_test")

                for path, info in await client.list(recursive=False):
                    if info["type"] == "dir" and path.name == "scoring_test":
                        await client.remove_directory("scoring_test")
                        return (True, "success")

                await client.remove_directory("scoring_test")
                return (False, "Could not find scoring directory")

        except aioftp.AIOFTPException:
            return (False, "Error occured while running FTP commands")
