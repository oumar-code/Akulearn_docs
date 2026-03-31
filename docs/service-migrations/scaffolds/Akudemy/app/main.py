"""Akudemy FastAPI application factory."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import content, credentials


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialise Redis on startup; close connection on shutdown."""
    app.state.redis = aioredis.from_url(
        settings.redis_url, encoding="utf-8", decode_responses=True
    )
    yield
    await app.state.redis.aclose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Akudemy",
        description=(
            "Content delivery and offline sync service for the Aku Platform. "
            "Provides lesson catalogues, content sync for Edge Hubs, and "
            "blockchain credential issuance via Polygon."
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

    app.include_router(content.router)
    app.include_router(credentials.router)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "Akudemy"}

    return app


app = create_app()
