from typing import override
from dsss.checks.base import SyncCheck, Host, Timeout

from ldap3 import Server, Connection, ALL


class LDAPCheck(SyncCheck):
    """
    Performs an anonymous LDAP connection against a specified server
    """

    name = "LDAP"

    tls: bool

    def __init__(
        self,
        host: Host,
        tls: bool = False,
        timeout_seconds: Timeout = 10,
    ) -> None:
        self.tls = tls
        super().__init__(host, None, timeout_seconds=timeout_seconds)

    @override
    def check(self) -> tuple[bool, str | None]:
        server = Server(
            self.host,
            get_info=ALL,
            use_ssl=self.tls,
            connect_timeout=self.timeout_seconds,
        )
        with Connection(
            server, authentication="ANONYMOUS", receive_timeout=self.timeout_seconds
        ) as conn:
            return (conn.bind(), None)
