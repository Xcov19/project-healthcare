"""
Application settings handled using Pydantic Settings management.

Pydantic is used both to read app settings from various sources, and to validate their
values.

https://docs.pydantic.dev/latest/usage/settings/
"""

from typing import Annotated
from blacksheep import FromHeader
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIInfo(BaseModel):
    title: str = "xcov19 API"
    version: str = "0.0.1"


class App(BaseModel):
    show_error_details: bool = False


class Site(BaseModel):
    copyright: str = "Example"


class Settings(BaseSettings):
    db_engine_url: Annotated[str, "database connection string"] = Field(default=...)

    # to override info:
    # export app_info='{"title": "x", "version": "0.0.2"}'
    info: APIInfo = APIInfo()

    # to override app:
    # export app_app='{"show_error_details": True}'
    app: App = App()

    model_config = SettingsConfigDict(env_prefix="APP_")


def load_settings() -> Settings:
    settings = Settings()
    if not settings.db_engine_url:
        raise ValueError("Missing environment variable: APP_DB_ENGINE_URL")
    return settings


class FromOriginMatchHeader(FromHeader[str]):
    name = "X-Origin-Match-Header"
    secret = "secret"
