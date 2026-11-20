from ipaddress import ip_address
from typing import override

import dns.asyncquery
import dns.exception
import dns.message
import dns.name
import dns.rcode
import dns.rdatatype

from dsss.checks.base import AsyncCheck, Host, Port, Timeout


class DNSCheck(AsyncCheck):
    name = "DNS"

    def __init__(
        self,
        host: Host,
        query: str,
        record_type: str = "A",
        availability_only: bool = False,
        port: Port = 53,
        timeout_seconds: Timeout = 10,
    ) -> None:
        super().__init__(str(ip_address(host)), port, timeout_seconds)
        try:
            self.query = dns.name.from_text(query)
            self.record_type = dns.rdatatype.from_text(record_type)
        except (dns.exception.DNSException, ValueError) as error:
            raise ValueError(f"Invalid DNS query: {error}") from error
        self.availability_only = availability_only

    @property
    @override
    def target(self) -> str:
        record_type = dns.rdatatype.to_text(self.record_type)
        return f"{record_type} {self.query} @ {super().target}"

    @override
    async def check(self) -> tuple[bool, str | None]:
        request = dns.message.make_query(self.query, self.record_type)

        try:
            response, _ = await dns.asyncquery.udp_with_fallback(
                request, self.host, port=self.port or 53, timeout=self.timeout_seconds
            )
        except (dns.exception.Timeout, TimeoutError):
            return (False, "Timeout occurred")

        except (OSError, dns.exception.DNSException) as error:
            return (False, f"DNS query failed: {error}")

        rcode = response.rcode()

        # any well-formed reply, including NXDOMAIN, means the server is up
        if self.availability_only and rcode in (dns.rcode.NOERROR, dns.rcode.NXDOMAIN):
            return (True, f"DNS responded with {dns.rcode.to_text(rcode)}.")

        if rcode != dns.rcode.NOERROR:
            return (False, f"DNS returned {dns.rcode.to_text(rcode)}.")

        if not any(rrset.rdtype == self.record_type for rrset in response.answer):
            return (False, "DNS response did not contain the requested record type.")

        return (True, "DNS returned an answer.")
