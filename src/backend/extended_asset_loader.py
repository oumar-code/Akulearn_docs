#!/usr/bin/env python3
"""Extended Asset Loader - Support Phase 1 and Phase 2 assets

This module extends asset loading capabilities to include:
1. Phase 1: ASCII diagrams and truth tables
2. Phase 2: Mathematical graphs and visualizations
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class GraphAsset:
    """Represents a mathematical graph asset."""
    lesson_id: str
    graph_id: str
    title: str
    subject: str
    graph_type: str  # function_graph, bar_chart, pie_chart, line_chart
    path: str
    content: Optional[str] = None


class ExtendedAssetLoader:
    """Load and manage Phase 1 and Phase 2 generated assets."""
    
    def __init__(self, assets_dir: str = "generated_assets"):
        self.assets_dir = Path(assets_dir)
        self.phase1_manifest_path = self.assets_dir / "phase1_manifest.json"
        self.phase2_manifest_path = self.assets_dir / "phase2_manifest.json"
        
        self._phase1_manifest = None
        self._phase2_manifest = None
        self._ascii_cache = {}
        self._table_cache = {}
        self._graph_cache = {}
        
        if not self.assets_dir.exists():
            raise FileNotFoundError(f"Assets directory not found: {assets_dir}")
    
    def load_phase1_manifest(self) -> Dict[str, Any]:
        """Load Phase 1 manifest file."""
        if self._phase1_manifest is None:
            if self.phase1_manifest_path.exists():
                with self.phase1_manifest_path.open("r", encoding="utf-8") as f:
                    self._phase1_manifest = json.load(f)
            else:
                self._phase1_manifest = {"ascii_diagrams": [], "truth_tables": []}
        return self._phase1_manifest
    
    def load_phase2_manifest(self) -> Dict[str, Any]:
        """Load Phase 2 manifest file."""
        if self._phase2_manifest is None:
            if self.phase2_manifest_path.exists():
                with self.phase2_manifest_path.open("r", encoding="utf-8") as f:
                    self._phase2_manifest = json.load(f)
            else:
                self._phase2_manifest = {
                    "function_graphs": [],
                    "bar_charts": [],
                    "pie_charts": [],
                    "line_charts": []
                }
        return self._phase2_manifest
    
    # Phase 1 methods (unchanged)
    
    def get_ascii_diagram(self, lesson_id: str) -> Optional[str]:
        """Get ASCII diagram for a lesson."""
        if lesson_id in self._ascii_cache:
            return self._ascii_cache[lesson_id]
        
        manifest = self.load_phase1_manifest()
        
        for item in manifest.get("ascii_diagrams", []):
            if item["lesson_id"] == lesson_id:
                path = Path(item["path"])
                if path.exists():
                    with path.open("r", encoding="utf-8") as f:
                        content = f.read()
                    self._ascii_cache[lesson_id] = content
                    return content
        
        return None
    
    def get_truth_table(self, lesson_id: str) -> Optional[str]:
        """Get truth table HTML for a lesson."""
        if lesson_id in self._table_cache:
            return self._table_cache[lesson_id]
        
        manifest = self.load_phase1_manifest()
        
        for item in manifest.get("truth_tables", []):
            if item["lesson_id"] == lesson_id:
                path = Path(item["path"])
                if path.exists():
                    with path.open("r", encoding="utf-8") as f:
                        content = f.read()
                    self._table_cache[lesson_id] = content
                    return content
        
        return None
    
    # Phase 2 methods (new)
    
    def get_graphs_for_lesson(self, lesson_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get all graphs for a lesson organized by type."""
        manifest = self.load_phase2_manifest()
        
        result = {
            "function_graphs": [],
            "bar_charts": [],
            "pie_charts": [],
            "line_charts": []
        }
        
        for graph_type in result.keys():
            for graph_item in manifest.get(graph_type, []):
                if graph_item.get("lesson_id") == lesson_id:
                    result[graph_type].append({
                        "id": graph_item.get("id"),
                        "title": graph_item.get("title"),
                        "type": graph_item.get("type"),
                        "path": graph_item.get("path"),
                        "subject": graph_item.get("subject")
                    })
        
        return result
    
    def get_graph_svg(self, graph_id: str) -> Optional[str]:
        """Get SVG content for a specific graph."""
        if graph_id in self._graph_cache:
            return self._graph_cache[graph_id]
        
        manifest = self.load_phase2_manifest()
        
        for graph_type in manifest.keys():
            for graph_item in manifest.get(graph_type, []):
                if graph_item.get("id") == graph_id:
                    path = Path(graph_item["path"])
                    if path.exists():
                        with path.open("r", encoding="utf-8") as f:
                            content = f.read()
                        self._graph_cache[graph_id] = content
                        return content
        
        return None
    
    def get_all_graphs_for_lesson(self, lesson_id: str) -> List[Dict[str, Any]]:
        """Get flattened list of all graphs for a lesson."""
        graphs = self.get_graphs_for_lesson(lesson_id)
        result = []
        for graph_type, graph_list in graphs.items():
            result.extend(graph_list)
        return result
    
    # Enrichment methods
    
    def enrich_lesson(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich lesson with all generated assets (Phase 1 & 2)."""
        lesson_id = lesson.get("id")
        if not lesson_id:
            return lesson
        
        generated_assets = lesson.get("generated_assets", {})
        
        # Phase 1 assets
        ascii_diagram = self.get_ascii_diagram(lesson_id)
        if ascii_diagram:
            generated_assets["ascii_diagram"] = {
                "type": "text",
                "content": ascii_diagram,
                "format": "ascii"
            }
        
        truth_table = self.get_truth_table(lesson_id)
        if truth_table:
            generated_assets["truth_table"] = {
                "type": "html",
                "content": truth_table,
                "format": "interactive_html"
            }
        
        # Phase 2 assets
        graphs = self.get_graphs_for_lesson(lesson_id)
        if any(graphs.values()):  # If any graphs exist
            generated_assets["graphs"] = {
                "type": "svg",
                "graphs_by_type": graphs,
                "total_graphs": sum(len(g) for g in graphs.values())
            }
        
        lesson["generated_assets"] = generated_assets
        return lesson
    
    def enrich_lessons(self, lessons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich multiple lessons with all assets."""
        return [self.enrich_lesson(lesson) for lesson in lessons]
    
    # Summary methods
    
    def get_assets_summary(self) -> Dict[str, Any]:
        """Get summary of all loaded assets."""
        phase1 = self.load_phase1_manifest()
        phase2 = self.load_phase2_manifest()
        
        phase2_total = sum(
            len(phase2.get(key, []))
            for key in ["function_graphs", "bar_charts", "pie_charts", "line_charts"]
        )
        
        return {
            "phase1": {
                "total_ascii_diagrams": len(phase1.get("ascii_diagrams", [])),
                "total_truth_tables": len(phase1.get("truth_tables", [])),
                "total": len(phase1.get("ascii_diagrams", [])) + len(phase1.get("truth_tables", []))
            },
            "phase2": {
                "function_graphs": len(phase2.get("function_graphs", [])),
                "bar_charts": len(phase2.get("bar_charts", [])),
                "pie_charts": len(phase2.get("pie_charts", [])),
                "line_charts": len(phase2.get("line_charts", [])),
                "total": phase2_total
            },
            "combined_total": len(phase1.get("ascii_diagrams", [])) + len(phase1.get("truth_tables", [])) + phase2_total,
            "by_subject": self._summarize_by_subject(phase1, phase2)
        }
    
    @staticmethod
    def _summarize_by_subject(
        phase1_manifest: Dict[str, Any],
        phase2_manifest: Dict[str, Any]
    ) -> Dict[str, Dict[str, int]]:
        """Summarize assets by subject across phases."""
        summary = {}
        
        # Phase 1
        for item in phase1_manifest.get("ascii_diagrams", []):
            subject = item.get("subject", "Unknown")
            if subject not in summary:
                summary[subject] = {"phase1": 0, "phase2": 0}
            summary[subject]["phase1"] += 1
        
        for item in phase1_manifest.get("truth_tables", []):
            subject = item.get("subject", "Unknown")
            if subject not in summary:
                summary[subject] = {"phase1": 0, "phase2": 0}
            summary[subject]["phase1"] += 1
        
        # Phase 2
        for graph_type in ["function_graphs", "bar_charts", "pie_charts", "line_charts"]:
            for item in phase2_manifest.get(graph_type, []):
                subject = item.get("subject", "Unknown")
                if subject not in summary:
                    summary[subject] = {"phase1": 0, "phase2": 0}
                summary[subject]["phase2"] += 1
        
        return summary


def get_extended_asset_loader(
    assets_dir: str = "generated_assets"
) -> ExtendedAssetLoader:
    """Factory function to get extended asset loader."""
    return ExtendedAssetLoader(assets_dir)


# Global instance
_extended_loader: Optional[ExtendedAssetLoader] = None


def initialize_extended_loader(
    assets_dir: str = "generated_assets"
) -> ExtendedAssetLoader:
    """Initialize global extended asset loader."""
    global _extended_loader
    if _extended_loader is None:
        _extended_loader = ExtendedAssetLoader(assets_dir)
    return _extended_loader


def get_extended_loader() -> Optional[ExtendedAssetLoader]:
    """Get global extended asset loader instance."""
    return _extended_loader
