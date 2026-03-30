"""Application settings loaded from environment / .env file."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_env: str = "development"
    debug: bool = False
    log_level: str = "info"

    # Operating mode
    operating_mode: str = Field("online", pattern="^(online|offline)$")

    # SQLite
    database_url: str = "sqlite+aiosqlite:///./edge_hub.db"
    db_echo: bool = False

    # Akudemy
    akudemy_base_url: str = "https://akudemy.example.com"
    akudemy_api_key: str = "changeme"
    sync_timeout_seconds: float = 30.0

    # AkuAI
    akuai_base_url: str = "https://akuai.example.com"
    akuai_api_key: str = "changeme"
    infer_timeout_seconds: float = 60.0


settings = Settings()
