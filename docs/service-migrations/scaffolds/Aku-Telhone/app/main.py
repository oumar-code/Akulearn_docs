"""Aku-Telhone FastAPI application factory — eSIM provisioning service."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import devices, esim


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown hook — initialise MVNO client here if needed."""
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Aku-Telhone",
        description=(
            "eSIM provisioning and OTA lifecycle management service for the Aku Platform. "
            "Handles eSIM profile provisioning, status tracking, OTA network switching, "
            "profile deactivation, and device attestation via Aku-IGHub."
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

    app.include_router(esim.router)
    app.include_router(devices.router)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "Aku-Telhone"}

    return app


app = create_app()
