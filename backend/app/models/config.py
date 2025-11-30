from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    DATABASE_URL: str = "sqlite:///travel_plans.db"
    GEO_USER_AGENT: str = "portfolio_planner_v2"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Singleton
_config = AppConfig()


def get_config() -> AppConfig:
    return _config


# --- DEPENDENCY ALIAS ---
ConfigDep = Annotated[AppConfig, Depends(get_config)]
