from typing import override
import aiohttp
from pydantic import HttpUrl

from dsss.checks.base import AsyncCheck, Timeout, validate_host


class HTTPCheck(AsyncCheck):
    """
    Performs a GET request to the specified host
    """

    name = "HTTP"

    url: str
    required_content: str | None

    def __init__(
        self,
        url: HttpUrl,
        required_content: str | None = None,
        timeout_seconds: Timeout = 10,
    ) -> None:
        self.required_content = required_content
        self.url = str(url)
        host = validate_host((url.host or "").removeprefix("[").removesuffix("]"))
        super().__init__(host, url.port, timeout_seconds=timeout_seconds)

    @override
    async def check(self) -> tuple[bool, str | None]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, ssl=False) as response:
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
