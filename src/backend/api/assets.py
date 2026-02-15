#!/usr/bin/env python3
"""Phase 1 Assets API Router

Provides endpoints for:
- Getting generated assets for lessons
- Retrieving asset manifests
- Asset availability summary
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import logging

from src.backend.asset_loader import get_global_asset_loader, initialize_asset_loader

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assets", tags=["Generated Assets"])


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class AssetContent(BaseModel):
    """Generated asset content."""
    type: str  # "text", "html"
    content: str
    format: str  # "ascii", "interactive_html"


class GeneratedAssets(BaseModel):
    """Generated assets for a lesson."""
    lesson_id: str
    ascii_diagram: Optional[AssetContent] = None
    truth_table: Optional[AssetContent] = None


class AssetSummary(BaseModel):
    """Summary of generated assets."""
    total_ascii_diagrams: int
    total_truth_tables: int
    total_assets: int
    by_subject: Dict[str, Dict[str, int]]
    by_type: Dict[str, int]


# ============================================================================
# ENDPOINTS
# ============================================================================

def ensure_loader_initialized():
    """Ensure asset loader is initialized."""
    loader = get_global_asset_loader()
    if loader is None:
        try:
            initialize_asset_loader()
        except FileNotFoundError as e:
            logger.warning(f"Asset loader initialization failed: {e}")
            return None
    return get_global_asset_loader()


@router.get("/summary", response_model=AssetSummary)
def get_assets_summary():
    """Get summary of all generated assets."""
    loader = ensure_loader_initialized()
    if not loader:
        raise HTTPException(
            status_code=503,
            detail="Asset loader not available - Phase 1 assets may not be generated"
        )
    
    summary = loader.get_assets_summary()
    return AssetSummary(**summary)


@router.get("/lesson/{lesson_id}", response_model=GeneratedAssets)
def get_lesson_assets(lesson_id: str):
    """Get generated assets for a specific lesson."""
    loader = ensure_loader_initialized()
    if not loader:
        raise HTTPException(
            status_code=503,
            detail="Asset loader not available"
        )
    
    ascii_diagram = loader.get_ascii_diagram(lesson_id)
    truth_table = loader.get_truth_table(lesson_id)
    
    if not ascii_diagram and not truth_table:
        raise HTTPException(
            status_code=404,
            detail=f"No generated assets found for lesson {lesson_id}"
        )
    
    assets = {
        "lesson_id": lesson_id,
        "ascii_diagram": None,
        "truth_table": None
    }
    
    if ascii_diagram:
        assets["ascii_diagram"] = {
            "type": "text",
            "content": ascii_diagram,
            "format": "ascii"
        }
    
    if truth_table:
        assets["truth_table"] = {
            "type": "html",
            "content": truth_table,
            "format": "interactive_html"
        }
    
    return GeneratedAssets(**assets)


@router.get("/ascii/{lesson_id}")
def get_ascii_diagram(lesson_id: str):
    """Get ASCII diagram for a lesson (raw text)."""
    loader = ensure_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Asset loader not available")
    
    diagram = loader.get_ascii_diagram(lesson_id)
    if not diagram:
        raise HTTPException(
            status_code=404,
            detail=f"No ASCII diagram found for lesson {lesson_id}"
        )
    
    return {
        "lesson_id": lesson_id,
        "type": "ascii",
        "content": diagram
    }


@router.get("/table/{lesson_id}")
def get_truth_table(lesson_id: str):
    """Get truth table for a lesson (raw HTML)."""
    loader = ensure_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Asset loader not available")
    
    table = loader.get_truth_table(lesson_id)
    if not table:
        raise HTTPException(
            status_code=404,
            detail=f"No truth table found for lesson {lesson_id}"
        )
    
    return {
        "lesson_id": lesson_id,
        "type": "html",
        "content": table
    }


@router.post("/initialize")
def initialize_assets(assets_dir: str = Query("generated_assets")):
    """Initialize asset loader (call once on startup)."""
    try:
        loader = initialize_asset_loader(assets_dir)
        summary = loader.get_assets_summary()
        return {
            "success": True,
            "message": "Asset loader initialized",
            "summary": summary
        }
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize asset loader: {str(e)}"
        )
