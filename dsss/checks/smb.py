from typing import override
from dsss.checks.base import SyncCheck, Host, Port, Timeout

from smbclient import register_session, listdir


class SMBCheck(SyncCheck):
    name = "SMB"

    def __init__(
        self,
        host: Host,
        port: Port = 445,
        timeout_seconds: Timeout = 10,
    ) -> None:
        super().__init__(host, port, timeout_seconds=timeout_seconds)

    @override
    def check(self) -> tuple[bool, str | None]:
        register_session(self.host, username="scoring", password="bb123#123")
        for filename in listdir(f"\\\\{self.host}"):
            print(filename)
        return (True, None)
