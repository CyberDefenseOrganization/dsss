from typing import override
import aioftp

from dsss.checks.base import BaseCheck


class FTPCheck(BaseCheck):
    username: str
    password: str

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = 21,
        timeout_seconds: float = 10,
    ) -> None:
        super().__init__(host, port, timeout_seconds=timeout_seconds)

        self.username = username
        self.password = password

    @override
    async def check(self) -> tuple[bool, str | None]:
        try:
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
