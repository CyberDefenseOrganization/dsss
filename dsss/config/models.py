from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    InstanceOf,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from dsss.checks.base import BaseCheck, Port, Timeout

NonEmpty = Annotated[str, Field(min_length=1)]


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)


class Branding(Settings):
    event_name_long: NonEmpty
    event_name_short: NonEmpty
    organization_name_long: NonEmpty
    organization_name_short: NonEmpty
    logo_path: NonEmpty | None = None


class EngineSettings(Settings):
    host: NonEmpty = "0.0.0.0"
    port: Port = 8080
    target_round_time: Annotated[float, Field(gt=0)]
    num_worker_processes: Annotated[int, Field(gt=0)]
    database_path: NonEmpty


class AdminSettings(Settings):
    username: NonEmpty
    password: NonEmpty


class CheckDefaults(Settings):
    timeout_seconds: Timeout | Annotated[list[Timeout], Field(min_length=1)] = 10
    username: str | Annotated[list[str], Field(min_length=1)] | None = None
    password: str | Annotated[list[str], Field(min_length=1)] | None = None


class ServiceOverride(Settings):
    name: NonEmpty
    points: Annotated[int, Field(ge=0)] | None = None
    check: dict[str, object] = Field(default_factory=dict)


def unique_services(services: list[ServiceOverride]) -> list[ServiceOverride]:
    names = [service.name for service in services]

    if len(names) != len(set(names)):
        raise ValueError("Service names must be unique")

    return services


class TeamSettings(Settings):
    name: NonEmpty
    variables: dict[str, str | int] = Field(default_factory=dict)
    services: list[ServiceOverride] = Field(default_factory=list)
    validate_services = field_validator("services")(unique_services)


class Document(BaseSettings):
    model_config = SettingsConfigDict(
        **Settings.model_config,
        env_prefix="DSSS_",
        env_nested_delimiter="__",
    )

    branding: Branding
    engine: EngineSettings
    admin: AdminSettings
    defaults: CheckDefaults = Field(default_factory=CheckDefaults)
    services: list[ServiceOverride] = Field(default_factory=list)
    teams: Annotated[list[TeamSettings], Field(min_length=1)]
    validate_services = field_validator("services")(unique_services)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, init_settings

    @model_validator(mode="after")
    def validate_teams(self):
        names = [team.name for team in self.teams]

        if len(names) != len(set(names)):
            raise ValueError("Team names must be unique")

        for team in self.teams:
            if not self.services and not team.services:
                raise ValueError(f"Team {team.name} has no services")

        return self


class ServiceSettings(Settings):
    name: NonEmpty
    points: Annotated[int, Field(ge=0)]
    check: InstanceOf[BaseCheck]

    @field_validator("check", mode="before")
    @classmethod
    def validate_check(cls, value: object, info: ValidationInfo) -> BaseCheck:
        if isinstance(value, BaseCheck):
            return value
        if not isinstance(value, dict):
            raise ValueError("Check configuration must be a table")

        context = info.context or {}

        return BaseCheck.create(
            value, context.get("defaults", {}), context.get("variables", {})
        )
