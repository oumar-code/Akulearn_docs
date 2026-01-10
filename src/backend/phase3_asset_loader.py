#!/usr/bin/env python3
"""Phase 3 Asset Loader - Specialized Educational Diagrams

Extends ExtendedAssetLoader to include Phase 3 specialized diagrams:
1. Venn Diagrams (set theory)
2. Flowcharts (algorithms)
3. Timelines (historical events)
4. Electrical Circuits
5. Logic Circuits
6. Molecular Structures
7. Chemical Reactions
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from src.backend.extended_asset_loader import ExtendedAssetLoader


@dataclass
class DiagramAsset:
    """Represents a Phase 3 diagram asset."""
    lesson_id: str
    diagram_id: str
    title: str
    subject: str
    diagram_type: str  # venn_2, venn_3, flowchart, timeline, circuit_*, chemistry_*
    path: str
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Phase3AssetLoader(ExtendedAssetLoader):
    """Extended asset loader with Phase 3 specialized diagram support."""
    
    def __init__(self, assets_dir: str = "generated_assets"):
        super().__init__(assets_dir)
        self.phase3_manifest_path = self.assets_dir / "phase3_manifest.json"
        self._phase3_manifest = None
        self._diagram_cache = {}
    
    # ====================
    # MANIFEST LOADING
    # ====================
    
    def load_phase3_manifest(self) -> Dict[str, Any]:
        """Load Phase 3 manifest file."""
        if self._phase3_manifest is None:
            if self.phase3_manifest_path.exists():
                with self.phase3_manifest_path.open("r", encoding="utf-8") as f:
                    self._phase3_manifest = json.load(f)
            else:
                self._phase3_manifest = {
                    "venn_diagrams": [],
                    "flowcharts": [],
                    "timelines": [],
                    "electrical_circuits": [],
                    "logic_circuits": [],
                    "molecular_structures": [],
                    "chemical_reactions": [],
                    "metadata": {"total_diagrams": 0}
                }
        return self._phase3_manifest
    
    # ====================
    # DIAGRAM RETRIEVAL
    # ====================
    
    def get_diagrams_for_lesson(self, lesson_id: str) -> List[DiagramAsset]:
        """Get all diagrams for a specific lesson."""
        manifest = self.load_phase3_manifest()
        diagrams = []
        
        # Search all diagram types
        for category in ["venn_diagrams", "flowcharts", "timelines", 
                         "electrical_circuits", "logic_circuits",
                         "molecular_structures", "chemical_reactions"]:
            items = manifest.get(category, [])
            for item in items:
                if item.get("lesson_id") == lesson_id:
                    diagrams.append(DiagramAsset(
                        lesson_id=item["lesson_id"],
                        diagram_id=item["id"],
                        title=item.get("title", "Untitled Diagram"),
                        subject=item.get("subject", "General"),
                        diagram_type=item["type"],
                        path=item["path"],
                        metadata=item
                    ))
        
        return diagrams
    
    def get_diagram_by_id(self, diagram_id: str) -> Optional[DiagramAsset]:
        """Get a specific diagram by ID."""
        manifest = self.load_phase3_manifest()
        
        # Search all categories
        for category in ["venn_diagrams", "flowcharts", "timelines",
                         "electrical_circuits", "logic_circuits", 
                         "molecular_structures", "chemical_reactions"]:
            items = manifest.get(category, [])
            for item in items:
                if item.get("id") == diagram_id:
                    return DiagramAsset(
                        lesson_id=item["lesson_id"],
                        diagram_id=item["id"],
                        title=item.get("title", "Untitled Diagram"),
                        subject=item.get("subject", "General"),
                        diagram_type=item["type"],
                        path=item["path"],
                        metadata=item
                    )
        
        return None
    
    def get_diagrams_by_type(self, diagram_type: str) -> List[DiagramAsset]:
        """Get all diagrams of a specific type."""
        manifest = self.load_phase3_manifest()
        diagrams = []
        
        # Map type to category
        type_to_category = {
            "venn_2": "venn_diagrams",
            "venn_3": "venn_diagrams",
            "flowchart": "flowcharts",
            "timeline": "timelines",
            "circuit_electrical": "electrical_circuits",
            "circuit_logic": "logic_circuits",
            "chemistry_molecular": "molecular_structures",
            "chemistry_reaction": "chemical_reactions"
        }
        
        category = type_to_category.get(diagram_type)
        if category:
            items = manifest.get(category, [])
            for item in items:
                if item.get("type") == diagram_type:
                    diagrams.append(DiagramAsset(
                        lesson_id=item["lesson_id"],
                        diagram_id=item["id"],
                        title=item.get("title", "Untitled Diagram"),
                        subject=item.get("subject", "General"),
                        diagram_type=item["type"],
                        path=item["path"],
                        metadata=item
                    ))
        
        return diagrams
    
    def load_diagram_svg(self, diagram_asset: DiagramAsset) -> str:
        """Load SVG content for a diagram."""
        if diagram_asset.diagram_id in self._diagram_cache:
            return self._diagram_cache[diagram_asset.diagram_id]
        
        diagram_path = self.assets_dir / diagram_asset.path
        if diagram_path.exists():
            with diagram_path.open("r", encoding="utf-8") as f:
                content = f.read()
                self._diagram_cache[diagram_asset.diagram_id] = content
                return content
        
        return None
    
    # ====================
    # LESSON ENRICHMENT
    # ====================
    
    def enrich_lesson(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich lesson with all assets (Phase 1, 2, and 3)."""
        # First enrich with Phase 1 & 2
        lesson = super().enrich_lesson(lesson)
        
        # Add Phase 3 diagrams
        lesson_id = lesson.get("id")
        if lesson_id:
            diagrams = self.get_diagrams_for_lesson(lesson_id)
            
            if diagrams:
                # Organize diagrams by type
                lesson["phase3_diagrams"] = {
                    "venn_diagrams": [],
                    "flowcharts": [],
                    "timelines": [],
                    "circuits": [],
                    "chemistry": []
                }
                
                for diagram in diagrams:
                    svg_content = self.load_diagram_svg(diagram)
                    diagram_data = {
                        "id": diagram.diagram_id,
                        "title": diagram.title,
                        "type": diagram.diagram_type,
                        "svg": svg_content
                    }
                    
                    # Categorize
                    if diagram.diagram_type.startswith("venn"):
                        lesson["phase3_diagrams"]["venn_diagrams"].append(diagram_data)
                    elif diagram.diagram_type == "flowchart":
                        lesson["phase3_diagrams"]["flowcharts"].append(diagram_data)
                    elif diagram.diagram_type == "timeline":
                        lesson["phase3_diagrams"]["timelines"].append(diagram_data)
                    elif diagram.diagram_type.startswith("circuit"):
                        lesson["phase3_diagrams"]["circuits"].append(diagram_data)
                    elif diagram.diagram_type.startswith("chemistry"):
                        lesson["phase3_diagrams"]["chemistry"].append(diagram_data)
                
                lesson["phase3_diagram_count"] = len(diagrams)
        
        return lesson
    
    # ====================
    # STATISTICS
    # ====================
    
    def get_phase3_stats(self) -> Dict[str, Any]:
        """Get Phase 3 asset statistics."""
        manifest = self.load_phase3_manifest()
        metadata = manifest.get("metadata", {})
        
        return {
            "total_diagrams": metadata.get("total_diagrams", 0),
            "venn_diagrams": metadata.get("venn_diagrams_count", 0),
            "flowcharts": metadata.get("flowcharts_count", 0),
            "timelines": metadata.get("timelines_count", 0),
            "electrical_circuits": metadata.get("electrical_circuits_count", 0),
            "logic_circuits": metadata.get("logic_circuits_count", 0),
            "molecular_structures": metadata.get("molecular_structures_count", 0),
            "chemical_reactions": metadata.get("chemical_reactions_count", 0),
            "generated_at": metadata.get("generated_at", "")
        }
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics for all phases."""
        return {
            "phase1": self.get_phase1_stats(),
            "phase2": self.get_phase2_stats(),
            "phase3": self.get_phase3_stats(),
            "total": {
                "phase1_assets": self.get_phase1_stats().get("total_assets", 0),
                "phase2_graphs": self.get_phase2_stats().get("total_graphs", 0),
                "phase3_diagrams": self.get_phase3_stats().get("total_diagrams", 0)
            }
        }


# ====================
# CONVENIENCE FUNCTIONS
# ====================

def get_loader() -> Phase3AssetLoader:
    """Get singleton asset loader instance."""
    return Phase3AssetLoader()


def enrich_lesson_with_all_assets(lesson: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich a lesson with all available assets (Phase 1, 2, 3)."""
    loader = get_loader()
    return loader.enrich_lesson(lesson)


def enrich_lessons_with_all_assets(lessons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enrich multiple lessons with all available assets."""
    loader = get_loader()
    return loader.enrich_lessons(lessons)

# ====================
# GLOBAL INSTANCE HELPERS
# ====================

_phase3_loader: Optional[Phase3AssetLoader] = None

def initialize_phase3_loader(assets_dir: str = "generated_assets") -> Phase3AssetLoader:
    """Initialize global Phase 3 asset loader."""
    global _phase3_loader
    if _phase3_loader is None:
        _phase3_loader = Phase3AssetLoader(assets_dir)
    return _phase3_loader

def get_phase3_loader() -> Optional[Phase3AssetLoader]:
    """Get global Phase 3 asset loader instance."""
    return _phase3_loader
