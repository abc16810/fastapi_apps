from enum import Enum

from pydantic import BaseSettings, Field


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = Field(..., env=AppEnvTypes.prod)

    class Config:
        env_file = ".env"