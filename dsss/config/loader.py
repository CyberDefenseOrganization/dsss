from pathlib import Path
import tomllib

from pydantic import ValidationError
from pydantic_settings import SettingsError, TomlConfigSettingsSource

from dsss.config import Config
from dsss.config.models import Document, ServiceSettings
from dsss.service import Service
from dsss.team import Team


class ConfigError(ValueError):
    pass


def validation_error(location: str, error: ValidationError) -> ConfigError:
    details = "; ".join(
        f"{'.'.join(map(str, item['loc']))}: {item['msg']}"
        for item in error.errors(include_input=False)
    )
    return ConfigError(f"{location}: {details}")


def build_teams(document: Document, source: Path) -> dict[str, Team]:
    location = str(source)
    try:
        templates = {
            service.name: service.model_dump(exclude_none=True)
            for service in document.services
        }
        defaults = document.defaults.model_dump(exclude_none=True)
        teams = {}
        for team in document.teams:
            context = {
                "defaults": defaults,
                "variables": {"team": team.name, **team.variables},
            }
            definitions = dict(templates)
            for override in team.services:
                original = definitions.get(override.name, {})
                value = override.model_dump(exclude_none=True)
                definitions[override.name] = {
                    **original,
                    **value,
                    "check": {**original.get("check", {}), **value["check"]},
                }
            services = {}
            for name, definition in definitions.items():
                location = f"{source}, team {team.name}, service {name}"
                service = ServiceSettings.model_validate(definition, context=context)
                services[name] = Service(name, service.points, service.check)
            teams[team.name] = Team(team.name, services)
    except ValidationError as error:
        raise validation_error(location, error) from None
    return teams


def resolve_path(source: Path, value: str) -> Path:
    return (source.parent / Path(value).expanduser()).resolve()


def load_config(path: str | Path | None = None) -> Config:
    source = Path(path or "config.toml").expanduser().resolve()
    location = str(source)
    try:
        if not source.is_file():
            raise ConfigError(f"Configuration file not found: {source}")
        document = Document(**TomlConfigSettingsSource(Document, source)())
        teams = build_teams(document, source)
    except ValidationError as error:
        raise validation_error(location, error) from None
    except (OSError, tomllib.TOMLDecodeError, SettingsError) as error:
        raise ConfigError(f"Cannot read configuration {source}: {error}") from None

    return Config(
        **document.branding.model_dump(exclude={"logo_path"}),
        logo_path=resolve_path(source, document.branding.logo_path)
        if document.branding.logo_path
        else None,
        host=document.engine.host,
        port=document.engine.port,
        target_round_time=document.engine.target_round_time,
        num_worker_processes=document.engine.num_worker_processes,
        database_path=str(resolve_path(source, document.engine.database_path)),
        admin_username=document.admin.username,
        admin_password=document.admin.password,
        teams=teams,
        source_path=source,
    )
