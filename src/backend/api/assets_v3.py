#!/usr/bin/env python3
"""Phase 3 Assets API Router - Specialized Diagrams

Provides endpoints for:
- Phase 3: Venn diagrams, flowcharts, timelines, circuits, chemistry
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import logging

from src.backend.phase3_asset_loader import (
    initialize_phase3_loader,
    get_phase3_loader,
    Phase3AssetLoader
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assets/phase3", tags=["Phase 3 Diagrams"]) 


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class DiagramInfo(BaseModel):
    id: str
    title: str
    type: str
    path: str
    subject: str

class DiagramsByType(BaseModel):
    venn_diagrams: List[DiagramInfo] = []
    flowcharts: List[DiagramInfo] = []
    timelines: List[DiagramInfo] = []
    electrical_circuits: List[DiagramInfo] = []
    logic_circuits: List[DiagramInfo] = []
    molecular_structures: List[DiagramInfo] = []
    chemical_reactions: List[DiagramInfo] = []

class Phase3Summary(BaseModel):
    total_diagrams: int
    venn_diagrams: int
    flowcharts: int
    timelines: int
    electrical_circuits: int
    logic_circuits: int
    molecular_structures: int
    chemical_reactions: int
    generated_at: Optional[str] = None

class DiagramContent(BaseModel):
    id: str
    title: str
    type: str
    svg: str


# ============================================================================
# HELPERS
# ============================================================================

def ensure_phase3_loader_initialized() -> Optional[Phase3AssetLoader]:
    loader = get_phase3_loader()
    if loader is None:
        try:
            loader = initialize_phase3_loader()
        except FileNotFoundError as e:
            logger.warning(f"Phase 3 loader initialization failed: {e}")
            return None
    return loader


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/summary", response_model=Phase3Summary)
def get_phase3_summary():
    loader = ensure_phase3_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 3 loader not available")
    stats = loader.get_phase3_stats()
    return Phase3Summary(
        total_diagrams=stats["total_diagrams"],
        venn_diagrams=stats["venn_diagrams"],
        flowcharts=stats["flowcharts"],
        timelines=stats["timelines"],
        electrical_circuits=stats["electrical_circuits"],
        logic_circuits=stats["logic_circuits"],
        molecular_structures=stats["molecular_structures"],
        chemical_reactions=stats["chemical_reactions"],
        generated_at=stats.get("generated_at")
    )


@router.get("/lesson/{lesson_id}", response_model=DiagramsByType)
def get_phase3_diagrams_for_lesson(lesson_id: str):
    loader = ensure_phase3_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 3 loader not available")
    diagrams = loader.get_diagrams_for_lesson(lesson_id)
    if not diagrams:
        raise HTTPException(status_code=404, detail=f"No Phase 3 diagrams found for lesson {lesson_id}")
    
    by_type = DiagramsByType()
    for d in diagrams:
        info = DiagramInfo(id=d.diagram_id, title=d.title, type=d.diagram_type, path=d.path, subject=d.subject)
        if d.diagram_type.startswith("venn"):
            by_type.venn_diagrams.append(info)
        elif d.diagram_type == "flowchart":
            by_type.flowcharts.append(info)
        elif d.diagram_type == "timeline":
            by_type.timelines.append(info)
        elif d.diagram_type == "circuit_electrical":
            by_type.electrical_circuits.append(info)
        elif d.diagram_type == "circuit_logic":
            by_type.logic_circuits.append(info)
        elif d.diagram_type == "chemistry_molecular":
            by_type.molecular_structures.append(info)
        elif d.diagram_type == "chemistry_reaction":
            by_type.chemical_reactions.append(info)
    return by_type


@router.get("/diagram/{diagram_id}", response_model=DiagramContent)
def get_phase3_diagram(diagram_id: str):
    loader = ensure_phase3_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 3 loader not available")
    diagram = loader.get_diagram_by_id(diagram_id)
    if not diagram:
        raise HTTPException(status_code=404, detail=f"Diagram {diagram_id} not found")
    svg = loader.load_diagram_svg(diagram)
    if not svg:
        raise HTTPException(status_code=404, detail=f"SVG content not found for {diagram_id}")
    return DiagramContent(id=diagram.diagram_id, title=diagram.title, type=diagram.diagram_type, svg=svg)


@router.get("/type/{diagram_type}")
def get_phase3_diagrams_by_type(diagram_type: str, lesson_id: Optional[str] = Query(None)):
    loader = ensure_phase3_loader_initialized()
    if not loader:
        raise HTTPException(status_code=503, detail="Phase 3 loader not available")
    diagrams = loader.get_diagrams_by_type(diagram_type)
    if lesson_id:
        diagrams = [d for d in diagrams if d.lesson_id == lesson_id]
    if not diagrams:
        raise HTTPException(status_code=404, detail="No diagrams found")
    return {
        "type": diagram_type,
        "count": len(diagrams),
        "diagrams": [
            {
                "id": d.diagram_id,
                "title": d.title,
                "type": d.diagram_type,
                "path": d.path,
                "subject": d.subject
            } for d in diagrams
        ]
    }


@router.post("/initialize")
def initialize_phase3_assets(assets_dir: str = Query("generated_assets")):
    try:
        loader = initialize_phase3_loader(assets_dir)
        stats = loader.get_phase3_stats()
        return {
            "success": True,
            "message": "Phase 3 asset loader initialized",
            "summary": stats
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize: {str(e)}")
