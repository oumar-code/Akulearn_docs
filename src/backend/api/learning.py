#!/usr/bin/env python3
"""Main FastAPI Application - Akulearn Learning Platform

Aggregates all API routers:
- Assets (Phase 1, Phase 2, Phase 3)
- User Learning Progress
- Admin/Super Admin endpoints
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import routers
from src.backend.api.assets import router as assets_v1_router
from src.backend.api.assets_v2 import router as assets_v2_router
from src.backend.api.assets_v3 import router as assets_v3_router
from src.backend.api.assets_v4 import router as assets_v4_router
from src.backend.api.learning_endpoints import router as learning_router
from src.backend.api.super_admin import router as super_admin_router
from src.backend.api.users import router as users_router

# Import initializers
from src.backend.phase3_asset_loader import initialize_phase3_loader
from src.backend.phase4_asset_loader import initialize_phase4_loader

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Akulearn Learning Platform",
    description="Comprehensive API for Nigerian education platform with Phase 1 (ASCII diagrams), Phase 2 (Charts), Phase 3 (Specialized diagrams), and Phase 4 (Practice Questions)",
    version="4.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize asset loaders on startup
@app.on_event("startup")
async def startup_event():
    """Initialize all asset loaders"""
    try:
        logger.info("Initializing Phase 3 asset loader...")
        initialize_phase3_loader("generated_assets")
        logger.info("✅ Phase 3 asset loader initialized")
    except Exception as e:
        logger.warning(f"Phase 3 loader initialization warning: {e}")
    
    try:
        logger.info("Initializing Phase 4 asset loader...")
        initialize_phase4_loader("generated_assets")
        logger.info("✅ Phase 4 asset loader initialized")
    except Exception as e:
        logger.warning(f"Phase 4 loader initialization warning: {e}")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "akulearn-api",
        "version": "4.0.0"
    }

# Include routers
logger.info("Mounting API routers...")
app.include_router(assets_v1_router, tags=["Phase 1 Assets"])
app.include_router(assets_v2_router, tags=["Phase 2 Assets"])
app.include_router(assets_v3_router, tags=["Phase 3 Assets"])
app.include_router(assets_v4_router, tags=["Phase 4 Assets"])
app.include_router(learning_router, tags=["Learning"])
app.include_router(super_admin_router, tags=["Admin"])
app.include_router(users_router, tags=["Users"])

logger.info("✅ All routers mounted successfully")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.backend.api.learning:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
