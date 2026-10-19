from typing import Annotated, override

from pydantic import Field
from smbclient import listdir, register_session
from smbprotocol.connection import Connection
from smbprotocol.exceptions import SMBException

from dsss.checks.base import SyncCheck, Host, Port, Timeout


class SMBCheck(SyncCheck):
    """Authenticate each run and optionally list a share's root directory."""

    name = "SMB"

    def __init__(
        self,
        host: Host,
        port: Port = 445,
        timeout_seconds: Timeout = 10,
        username: str | None = None,
        password: str | None = None,
        share: Annotated[str, Field(min_length=1, pattern=r"^[^\\/]+$")] | None = None,
    ) -> None:
        if username is None or password is None:
            raise ValueError("username and password are required for SMB login checks")
        super().__init__(host, port, timeout_seconds=timeout_seconds)
        self.username = username
        self.password = password
        self.share = share

    @override
    def check(self) -> tuple[bool, str | None]:
        connection_cache: dict[str, Connection] = {}
        try:
            register_session(
                self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                connection_timeout=self.timeout_seconds,
                connection_cache=connection_cache,
            )
            if self.share is not None:
                listdir(
                    rf"\\{self.host}\{self.share}",
                    username=self.username,
                    password=self.password,
                    port=self.port,
                    connection_timeout=self.timeout_seconds,
                    connection_cache=connection_cache,
                )
                return (True, f'SMB share "{self.share}" is accessible.')
            return (True, "SMB login successful.")
        except TimeoutError:
            return (False, "Timeout occurred")
        except (OSError, SMBException, ValueError) as error:
            return (False, f"SMB check failed: {error}")
        finally:
            for connection in connection_cache.values():
                connection.disconnect(close=False)
