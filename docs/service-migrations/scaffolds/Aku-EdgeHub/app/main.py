"""Aku-EdgeHub FastAPI application entry point."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session_sqlite import init_db
from app.routers import devices, edge

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Aku-EdgeHub",
    description="Offline edge server — local SQLite store, dual online/offline modes.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(edge.router)
app.include_router(devices.router)


@app.get("/health", tags=["ops"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "Aku-EdgeHub"}


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("EdgeHub starting — mode=%s", settings.operating_mode)
    await init_db()
