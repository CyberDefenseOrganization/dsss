from typing import override
from dsss.checks.base import BaseCheck

from ldap3 import Server, Connection, ALL, ASYNC
import asyncio
import smbclient


class LDAPCheck(BaseCheck):
    """
    Performs an anonymous LDAP connection against a specified server
    """

    username: str
    password: str
    required_content: str | None
    sasl_mechanism: str
    query: str | None
    tls: bool

    def __init__(
        self,
        host: str,
        # username: str,
        # password: str,
        # sasl_mechanism: str = "EXTERNAL",
        # query: str | None = None,
        # expected_response: str | None = None,
        tls: bool = False,
        timeout_seconds: float = 10,
    ) -> None:
        # self.expected_response = expected_response
        # self.username = username
        # self.password = password
        # self.sasl_mechanism = sasl_mechanism
        # self.query = query

        self.tls = tls
        if not host.startswith("ldap://"):
            host = "ldap://" + host

        # if query is None and expected_response is not None:
        #     # TODO: create custom Exception class for configration related exceptions
        #     raise Exception(
        #         "If LDAP query is not set, then expected response cannot be set"
        #     )

        super().__init__(host, None, timeout_seconds=timeout_seconds)

    @override
    async def check(self) -> tuple[bool, str | None]:
        server = Server(self.host, get_info=ALL, use_ssl=self.tls)

        # blocking
        def do_bind():
            with Connection(
                server, authentication="ANONYMOUS", receive_timeout=self.timeout_seconds
            ) as conn:
                ok = conn.bind()
                return ok

        response = await asyncio.to_thread(do_bind)
        return (response, None)
