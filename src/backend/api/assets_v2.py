#!/usr/bin/env python3
"""Extended Assets API Router - Phase 1 & Phase 2

Provides endpoints for:
- Phase 1: ASCII diagrams and truth tables
- Phase 2: Mathematical graphs and visualizations
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import logging

from src.backend.extended_asset_loader import (
    get_extended_asset_loader,
    initialize_extended_loader,
    get_extended_loader
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assets", tags=["Generated Assets"])


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class AssetContent(BaseModel):
    """Generated asset content."""
    type: str  # "text", "html", "svg"
    content: Optional[str] = None
    format: Optional[str] = None


class GraphInfo(BaseModel):
    """Information about a mathematical graph."""
    id: str
    title: str
    type: str  # function_graph, bar_chart, pie_chart, line_chart
    path: str
    subject: str


class GraphCollection(BaseModel):
    """Collection of graphs for a lesson."""
    function_graphs: List[GraphInfo] = []
    bar_charts: List[GraphInfo] = []
    pie_charts: List[GraphInfo] = []
    line_charts: List[GraphInfo] = []


class GeneratedAssets(BaseModel):
    """Generated assets for a lesson (Phase 1 & 2)."""
    lesson_id: str
    ascii_diagram: Optional[AssetContent] = None
    truth_table: Optional[AssetContent] = None
    graphs: Optional[GraphCollection] = None


class AssetSummary(BaseModel):
    """Summary of all generated assets."""
    phase1: Dict[str, Any]
    phase2: Dict[str, Any]
    combined_total: int
    by_subject: Dict[str, Dict[str, int]]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def ensure_extended_loader_initialized():
    """Ensure extended asset loader is initialized."""
    loader = get_extended_loader()
    if loader is None:
        try:
            initialize_extended_loader()
        except FileNotFoundError as e:
            logger.warning(f"Extended asset loader initialization failed: {e}")
            return None
    return get_extended_loader()


# ============================================================================
# PHASE 1 ENDPOINTS (EXTENDED)
# ============================================================================

@router.get("/summary", response_model=AssetSummary)
def get_assets_summary():
    """Get summary of all generated assets (Phase 1 & 2)."""
    loader = ensure_extended_loader_initialized()
    if not loader:
        raise HTTPException(
            status_code=503,
            detail="Asset loader not available - Generated assets may not be available"
        )
    
    summary = loader.get_assets_summary()
    return AssetSummary(**summary)


@router.get("/lesson/{lesson_id}", response_model=GeneratedAssets)
def get_lesson_assets(lesson_id: str):
    """Get all generated assets for a specific lesson (Phase 1 & 2)."""
    loader = ensure_extended_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Asset loader not available")
    
    # Get Phase 1 assets
    ascii_diagram = loader.get_ascii_diagram(lesson_id)
    truth_table = loader.get_truth_table(lesson_id)
    
    # Get Phase 2 assets
    graphs = loader.get_graphs_for_lesson(lesson_id)
    has_graphs = any(graphs.values())
    
    if not ascii_diagram and not truth_table and not has_graphs:
        raise HTTPException(
            status_code=404,
            detail=f"No generated assets found for lesson {lesson_id}"
        )
    
    assets = {
        "lesson_id": lesson_id,
        "ascii_diagram": None,
        "truth_table": None,
        "graphs": None
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
    
    if has_graphs:
        graphs_data = {
            "function_graphs": graphs.get("function_graphs", []),
            "bar_charts": graphs.get("bar_charts", []),
            "pie_charts": graphs.get("pie_charts", []),
            "line_charts": graphs.get("line_charts", [])
        }
        assets["graphs"] = graphs_data
    
    return GeneratedAssets(**assets)


@router.get("/ascii/{lesson_id}")
def get_ascii_diagram(lesson_id: str):
    """Get ASCII diagram for a lesson (raw text)."""
    loader = ensure_extended_loader_initialized()
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
    loader = ensure_extended_loader_initialized()
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


# ============================================================================
# PHASE 2 ENDPOINTS (NEW)
# ============================================================================

@router.get("/graphs/lesson/{lesson_id}", response_model=GraphCollection)
def get_graphs_for_lesson(lesson_id: str):
    """Get all mathematical graphs for a lesson (Phase 2)."""
    loader = ensure_extended_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Asset loader not available")
    
    graphs = loader.get_graphs_for_lesson(lesson_id)
    
    if not any(graphs.values()):
        raise HTTPException(
            status_code=404,
            detail=f"No graphs found for lesson {lesson_id}"
        )
    
    return GraphCollection(**graphs)


@router.get("/graph/{graph_id}")
def get_graph_svg(graph_id: str):
    """Get SVG content for a specific graph (Phase 2)."""
    loader = ensure_extended_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Asset loader not available")
    
    svg_content = loader.get_graph_svg(graph_id)
    if not svg_content:
        raise HTTPException(
            status_code=404,
            detail=f"Graph not found: {graph_id}"
        )
    
    return {
        "graph_id": graph_id,
        "type": "svg",
        "content": svg_content
    }


@router.get("/graphs/type/{graph_type}")
def get_graphs_by_type(
    graph_type: str,
    lesson_id: Optional[str] = Query(None)
):
    """Get all graphs of a specific type, optionally filtered by lesson."""
    loader = ensure_extended_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Asset loader not available")
    
    valid_types = ["function_graphs", "bar_charts", "pie_charts", "line_charts"]
    if graph_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid graph type. Must be one of: {', '.join(valid_types)}"
        )
    
    manifest = loader.load_phase2_manifest()
    graphs = manifest.get(graph_type, [])
    
    if lesson_id:
        graphs = [g for g in graphs if g.get("lesson_id") == lesson_id]
    
    if not graphs:
        raise HTTPException(
            status_code=404,
            detail=f"No {graph_type} found" + (
                f" for lesson {lesson_id}" if lesson_id else ""
            )
        )
    
    return {
        "type": graph_type,
        "count": len(graphs),
        "graphs": graphs
    }


# ============================================================================
# INITIALIZATION ENDPOINT
# ============================================================================

@router.post("/initialize")
def initialize_assets(assets_dir: str = Query("generated_assets")):
    """Initialize extended asset loader (call once on startup)."""
    try:
        loader = initialize_extended_loader(assets_dir)
        summary = loader.get_assets_summary()
        return {
            "success": True,
            "message": "Extended asset loader initialized with Phase 1 & 2 support",
            "summary": summary
        }
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize asset loader: {str(e)}"
        )
