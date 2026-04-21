"""Akudemy application settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Akudemy"
    log_level: str = "info"

    # Redis
    redis_url: str = Field("redis://redis:6379", alias="REDIS_URL")

    # Polygon / blockchain
    polygon_rpc_url: str = Field("https://polygon-rpc.com", alias="POLYGON_RPC_URL")
    polygon_network: str = Field("amoy", alias="POLYGON_NETWORK")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
