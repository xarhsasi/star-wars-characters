"""Base settings class contains only important fields."""

# mypy: ignore-errors
import logging
from pathlib import Path
from typing import List

from environs import Env
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


BASE_FOLDER = Path(__file__).parents[1]

# For local support, not needed on docker as it is already set in docker-compose
env = Env()
env.read_env(BASE_FOLDER / ".envs" / ".fastapi")
env.read_env(BASE_FOLDER / ".envs" / ".postgres")


def get_logging_config(log_level: str, log_format: str = "json") -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {process} {thread} "
                "{pathname}:{funcName}:{lineno} - {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "json" if log_format == "json" else "verbose",
            },
            "celery": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "json" if log_format == "json" else "verbose",
            },
            "mailgenie": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "json" if log_format == "json" else "verbose",
            },
        },
        "root": {"level": log_level, "handlers": ["console"]},
        "loggers": {
            "celery": {
                "handlers": ["celery"],
                "propagate": False,
            },
            "mailgenie": {
                "handlers": ["mailgenie"],
                "level": log_level,
                "propagate": False,
            },
        },
    }


class CeleryConfig(BaseModel):
    timezone: str = "UTC"
    broker_url: str = env.str("CELERY_BROKER_URL")
    accept_content: List[str] = ["json"]
    task_serializer: str = "json"
    result_serializer: str = "json"
    task_time_limit: int = 5 * 60
    task_soft_time_limit: int = 60
    result_expires: int = 60 * 24 * 7
    result_backend: str = (
        f"db+{env.str('DATABASE_URL').replace('asyncpg', 'psycopg2')}"
    )


class AuthenticationConfig(BaseModel):
    JWT_SECRET_KEY: str = env.str("JWT_SECRET")
    JWT_ALGORITHM: str = env.str("JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: str = env.int(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    JWT_TOKEN_URL: str = env.str("JWT_TOKEN_URL", "/v1/user/token")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    API_STR: str = "/v1"
    PROJECT_NAME: str = "Star Wars Characters"
    DESCRIPTION: str = (
        "The ultimate mail-agent project using the FastApi framework."
    )
    VERSION: str = env.str("VERSION", "0.1.0")
    ENABLE_SWAGGER: bool = env.bool("ENABLE_SWAGGER", False)
    CORS_ORIGINS: List = env.list("CORS_ORIGINS")
    DATABASE_URL: str = env.str("DATABASE_URL", "")
    TEST_DATABASE_URL: str = DATABASE_URL.replace("mailgenie", "test")
    # Celery
    # ------------------------------------------------------------------------------
    CELERY_CONFIG: CeleryConfig = CeleryConfig()
    DEBUG: bool = False
    LOGGING_CONFIG: dict = get_logging_config(
        env.str("LOGGING_LEVEL", "INFO"), env.str("LOGGING_FORMAT", "json")
    )
    # Authentication
    # ------------------------------------------------------------------------------
    AUTH_CONFIG: AuthenticationConfig = AuthenticationConfig()


settings = Settings()
