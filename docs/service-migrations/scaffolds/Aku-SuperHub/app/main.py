"""Aku-SuperHub FastAPI application factory — regional analytics service."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analytics, fleet, models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown hook — initialise Kafka consumer here if needed."""
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Aku-SuperHub",
        description=(
            "Regional analytics and fleet management service for the Aku Platform. "
            "Aggregates telemetry from Edge Hubs, provides regional analytics summaries, "
            "and triggers model fine-tuning jobs."
        ),
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(fleet.router)
    app.include_router(analytics.router)
    app.include_router(models.router)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "Aku-SuperHub"}

    return app


app = create_app()
