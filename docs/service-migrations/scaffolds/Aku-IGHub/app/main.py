"""Aku-IGHub FastAPI application factory — global gateway service."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import clearing, compliance, credentials, metadata


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown hook — add DB pool init here if needed."""
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Aku-IGHub",
        description=(
            "Global API gateway for the Aku Platform. "
            "Handles verifiable credential issuance/verification, Aku Coin financial "
            "clearing, anonymised metadata exchange, and cross-border compliance checks. "
            "JWT validation at this boundary is the system-wide auth layer."
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

    app.include_router(credentials.router)
    app.include_router(clearing.router)
    app.include_router(metadata.router)
    app.include_router(compliance.router)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "Aku-IGHub"}

    return app


app = create_app()
