"""AkuWorkspace service configuration — loaded from environment / .env file."""

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

    # Downstream services
    aku_ai_url: str = Field("http://akuai:8001", alias="AKU_AI_URL")
    aku_daas_url: str = Field("http://aku-daas:8002", alias="AKU_DAAS_URL")
    akudemy_url: str = Field("http://akudemy:8003", alias="AKUDEMY_URL")

    # Redis
    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")

    # HTTP client
    http_timeout: float = Field(30.0, alias="HTTP_TIMEOUT")

    # Service identity
    service_name: str = Field("akuworkspace", alias="SERVICE_NAME")
    service_version: str = Field("0.1.0", alias="SERVICE_VERSION")
    log_level: str = Field("info", alias="LOG_LEVEL")

    # CORS
    cors_origins: list[str] = Field(
        default_factory=list, alias="CORS_ORIGINS"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
