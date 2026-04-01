"""AkuTutor FastAPI application factory."""

from __future__ import annotations

import logging

from fastapi import FastAPI

from app.dependencies import get_settings
from app.routers import feedback, sessions

settings = get_settings()

logging.basicConfig(level=settings.log_level.upper())

app = FastAPI(
    title=settings.app_name,
    description=(
        "Curriculum-aware AI tutoring service. "
        "Delegates all text generation to AkuAI."
    ),
    version="0.1.0",
)

app.include_router(sessions.router)
app.include_router(feedback.router)


@app.get("/health", tags=["ops"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
