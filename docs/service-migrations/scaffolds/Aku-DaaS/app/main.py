"""Aku-DaaS FastAPI application factory — data governance service."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import consent, datasets, metadata


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown hook — initialise anonymisation pipeline here if needed."""
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Aku-DaaS",
        description=(
            "Data governance and anonymisation pipeline service for the Aku Platform. "
            "Handles dataset ingestion, anonymisation pipeline execution, "
            "metadata publishing to Aku-IGHub, and user consent management."
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

    app.include_router(datasets.router)
    app.include_router(metadata.router)
    app.include_router(consent.router)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "Aku-DaaS"}

    return app


app = create_app()
