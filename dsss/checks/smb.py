from typing import override
from dsss.checks.base import SyncCheck

from smbclient import register_session, listdir


class SMBCheck(SyncCheck):
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
    def check(self) -> tuple[bool, str | None]:
        register_session(self.host, username="scoring", password="bb123#123")
        for filename in listdir(f"\\\\{self.host}"):
            print(filename)
        return (True, None)
