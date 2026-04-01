"""AkuAI FastAPI application factory."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import inference, models
from app.services.inference import inference_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Load models on startup; release resources on shutdown."""
    await inference_service.startup()
    yield
    await inference_service.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(
        title="AkuAI",
        description=(
            "Shared inference layer for the Aku Platform. "
            "All other services delegate text generation, classification, "
            "summarisation, embeddings, and Gemma edge-relay to this service."
        ),
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten via CORS_ORIGINS env var in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(inference.router)
    app.include_router(models.router)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "AkuAI"}

    return app


app = create_app()
