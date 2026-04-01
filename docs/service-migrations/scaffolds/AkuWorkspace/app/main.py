"""AkuWorkspace FastAPI application factory."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import context, docs_gen, workflows
from app.services.orchestrator import OrchestratorConfig, WorkflowOrchestrator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialise shared resources on startup; clean up on shutdown."""
    settings = get_settings()

    # Redis client
    app.state.redis = aioredis.from_url(
        settings.redis_url, encoding="utf-8", decode_responses=False
    )

    # Orchestrator
    cfg = OrchestratorConfig(
        aku_ai_url=settings.aku_ai_url,
        aku_daas_url=settings.aku_daas_url,
        akudemy_url=settings.akudemy_url,
        redis_url=settings.redis_url,
        http_timeout=settings.http_timeout,
    )
    app.state.orchestrator = WorkflowOrchestrator(cfg)

    # In-process workflow store (swap for a DB session factory in production)
    app.state.workflow_store = {}

    yield

    await app.state.redis.aclose()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="AkuWorkspace",
        description=(
            "AI-native productivity layer — orchestrates AkuAI, Aku-DaaS, "
            "and Akudemy into multi-step AI workflows."
        ),
        version=settings.service_version,
        lifespan=lifespan,
    )

    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(workflows.router)
    app.include_router(context.router)
    app.include_router(docs_gen.router)

    @app.get("/health", tags=["Health"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": settings.service_name}

    return app


app = create_app()
