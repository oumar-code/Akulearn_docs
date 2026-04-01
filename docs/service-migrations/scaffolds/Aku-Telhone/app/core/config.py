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

    # JWT / Auth
    jwt_algorithm: str = "RS256"
    jwt_public_key_path: str = "/secrets/jwt_public.pem"

    # MVNO / SM-DP+
    smdp_base_url: str = "https://smdp.telhone.akulearn.io"
    smdp_api_key: str = "changeme"
    mvno_operator_id: str = "akulearn-mvno"

    # QR code generation service
    qr_base_url: str = "https://qr.telhone.akulearn.io"

    # Aku-IGHub integration (device attestation)
    aku_ighub_url: str = "https://ighub.akulearn.io"
    aku_ighub_api_key: str = "changeme"
    ighub_timeout_seconds: float = 10.0

    # OTA platform
    ota_platform_url: str = "https://ota.telhone.akulearn.io"
    ota_platform_api_key: str = "changeme"
    ota_timeout_seconds: float = 30.0

    # CORS
    allowed_origins: str = "https://app.akulearn.io,https://admin.akulearn.io"

    # Rate limiting
    rate_limit_per_minute: int = Field(60, ge=1)


settings = Settings()
