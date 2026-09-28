from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from functools import cache
from importlib import import_module
from inspect import isabstract, signature
from ipaddress import ip_address
from pkgutil import walk_packages
from random import choice
from typing import Annotated, ClassVar, cast, get_type_hints

from pydantic import (
    AfterValidator,
    ConfigDict,
    Field,
    TypeAdapter,
    ValidationError,
    validate_call,
)


def validate_host(host: str) -> str:
    try:
        ip_address(host)
    except ValueError:
        try:
            domain = host.removesuffix(".").encode("idna").decode("ascii")
        except UnicodeError:
            raise ValueError(
                "Host must be an IPv4 address, IPv6 address, or FQDN"
            ) from None
        labels = domain.split(".")
        if (
            len(domain) > 253
            or len(labels) < 2
            or labels[-1].isdigit()
            or any(
                not 1 <= len(label) <= 63
                or label.startswith("-")
                or label.endswith("-")
                or not all(
                    character.isalnum() or character == "-" for character in label
                )
                for label in labels
            )
        ):
            raise ValueError("Host must be an IPv4 address, IPv6 address, or FQDN")

    return host


def expand_variables(value: object, variables: Mapping[str, str | int]) -> object:
    if isinstance(value, str):
        for name, replacement in variables.items():
            value = value.replace(f"{{{name}}}", str(replacement))

    elif isinstance(value, list):
        return [expand_variables(item, variables) for item in value]

    elif isinstance(value, dict):
        return {key: expand_variables(item, variables) for key, item in value.items()}

    return value


Host = Annotated[str, AfterValidator(validate_host)]
Port = Annotated[int, Field(ge=1, le=65535)]
Timeout = Annotated[float, Field(gt=0)]


class BaseCheck(ABC):
    name: ClassVar[str]
    options: ClassVar[frozenset[str]]
    registry: ClassVar[dict[str, type["BaseCheck"]]] = {}
    host: str
    port: int | None
    timeout_seconds: float = 30

    def __init_subclass__(cls, *, register: bool = True) -> None:
        """
        __init_subclass__ is called on the definition of sub classes,
        and allows us to basically do reflection
        """
        super().__init_subclass__()

        if not register or isabstract(cls):
            return

        name = cls.__dict__.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{cls.__name__} must declare a non-empty name")

        if name in BaseCheck.registry:
            raise ValueError(f"Duplicate check type: {name}")

        cls.options = frozenset(signature(cls).parameters)
        cls.__init__ = validate_call(  # pyright: ignore[reportCallIssue]
            cls.__init__, config=ConfigDict(strict=True, allow_inf_nan=False)
        )

        BaseCheck.registry[name] = cls

    @classmethod
    @cache
    def discover_checks(cls) -> dict[str, type["BaseCheck"]]:
        assert __package__ is not None
        package = import_module(__package__)

        for entry in walk_packages(package.__path__, prefix=f"{package.__name__}."):
            _ = import_module(entry.name)

        return cls.registry

    @classmethod
    def create(
        cls,
        options: Mapping[str, object],
        defaults: Mapping[str, object],
        variables: Mapping[str, str | int],
    ) -> "BaseCheck":
        options = dict(options)
        name = options.pop("type", None)
        checks = cls.discover_checks()

        if not isinstance(name, str) or name not in checks:
            raise ValueError(
                f"Unknown check type; available types: {', '.join(sorted(checks))}"
            )

        check = checks[name]

        options = {
            **{key: value for key, value in defaults.items() if key in check.options},
            **options,
        }

        options = {
            key: expand_variables(value, variables) for key, value in options.items()
        }

        hints = get_type_hints(check.__init__, include_extras=True)
        alternatives: dict[str, list[object]] = {}
        initial = dict(options)

        for key, value in options.items():
            if not isinstance(value, list) or key not in hints:
                continue

            adapter = TypeAdapter(hints[key])

            try:
                adapter.validate_python(value, strict=True)
            except ValidationError:
                if not value:
                    raise ValueError(f"{key}: random alternatives cannot be empty")

                for item in value:
                    adapter.validate_python(item, strict=True)

                alternatives[key] = value
                initial[key] = value[0]

        constructor = cast(Callable[..., BaseCheck], check)
        instance = constructor(**initial)
        if not alternatives:
            return instance

        def create_check() -> BaseCheck:
            return constructor(
                **{
                    **options,
                    **{key: choice(values) for key, values in alternatives.items()},
                }
            )

        timeout = max(alternatives.get("timeout_seconds", [instance.timeout_seconds]))
        if isinstance(instance, AsyncCheck):
            return _RandomAsyncCheck(instance, create_check, float(timeout))

        return _RandomSyncCheck(instance, create_check, float(timeout))

    def __init__(self, host: str, port: int | None, timeout_seconds: float) -> None:
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds


class AsyncCheck(BaseCheck, ABC):
    @abstractmethod
    async def check(self) -> tuple[bool, str | None]:
        pass


class SyncCheck(BaseCheck, ABC):
    @abstractmethod
    def check(self) -> tuple[bool, str | None]:
        pass


class _RandomAsyncCheck(AsyncCheck, register=False):
    def __init__(
        self, template: BaseCheck, factory: Callable[[], BaseCheck], timeout: float
    ) -> None:
        super().__init__(template.host, template.port, timeout)
        self.factory = factory
        self.name = template.name

    async def check(self) -> tuple[bool, str | None]:
        check = self.factory()
        assert isinstance(check, AsyncCheck)
        return await check.check()


class _RandomSyncCheck(SyncCheck, register=False):
    def __init__(
        self, template: BaseCheck, factory: Callable[[], BaseCheck], timeout: float
    ) -> None:
        super().__init__(template.host, template.port, timeout)
        self.factory = factory
        self.name = template.name

    def check(self) -> tuple[bool, str | None]:
        check = self.factory()
        assert isinstance(check, SyncCheck)
        return check.check()
