"""FastAPI dependency providers for AkuTutor."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    aku_ai_url: str = "http://akuai:8001"
    app_name: str = "AkuTutor"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()


# Module-level singleton so every request shares one TutorService instance.
_tutor_service_instance: "TutorService | None" = None  # noqa: F821


def get_tutor_service() -> "TutorService":  # noqa: F821
    from app.services.tutor import TutorService  # local import to avoid circular refs

    global _tutor_service_instance
    if _tutor_service_instance is None:
        settings = get_settings()
        _tutor_service_instance = TutorService(aku_ai_url=settings.aku_ai_url)
    return _tutor_service_instance
