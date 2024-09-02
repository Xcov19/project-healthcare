"""
Application settings handled using Pydantic Settings management.

Pydantic is used both to read app settings from various sources, and to validate their
values.

https://docs.pydantic.dev/latest/usage/settings/
"""

from blacksheep import FromHeader
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIInfo(BaseModel):
    title: str = "xcov19 API"
    version: str = "0.0.1"


class App(BaseModel):
    show_error_details: bool = False


class Site(BaseModel):
    copyright: str = "Example"


class Settings(BaseSettings):
    # to override info:
    # export app_info='{"title": "x", "version": "0.0.2"}'
    info: APIInfo = APIInfo()

    # to override app:
    # export app_app='{"show_error_details": True}'
    app: App = App()

    db_engine_url: str = "sqlite+aiosqlite:///"  # "sqlite+aiosqlite:///xcov19.db"

    model_config = SettingsConfigDict(env_prefix="APP_")


def load_settings() -> Settings:
    return Settings()


class FromOriginMatchHeader(FromHeader[str]):
    name = "X-Origin-Match-Header"
    secret = "secret"
