from typing import override
import aiohttp

from dsss.checks.base import BaseCheck


class HTTPCheck(BaseCheck):
    """
    Performs a GET request to the specified host
    """

    required_content: str | None

    def __init__(
        self,
        host: str,
        required_conent: str | None = None,
        timeout_seconds: float = 10,
    ) -> None:
        self.required_content = required_conent

        if not host.startswith("http://") and not host.startswith("https://"):
            host = "http://" + host

        super().__init__(host, None, timeout_seconds=timeout_seconds)

    @override
    async def check(self) -> tuple[bool, str | None]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.host, ssl=False) as response:
                    if response.status != 200:
                        return (
                            False,
                            f"Expected status code 200, got: {response.status}",
                        )

                    response = await response.text()

                    if (
                        self.required_content is not None
                        and self.required_content not in response
                    ):
                        return (
                            False,
                            f'Expected "{self.required_content}" in response, got: "{response}"',
                        )

                    return (True, "success")
        except aiohttp.ClientSSLError:
            return (False, "SSL verification error")
        except aiohttp.ClientResponseError:
            return (False, "Client response error")
        except aiohttp.ClientConnectionError:
            return (False, "Unable to connect to host")
