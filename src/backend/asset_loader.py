#!/usr/bin/env python3
"""Backend Asset Loader - Load and serve generated Phase 1 assets

This module provides:
1. Asset manifest management
2. Lesson enrichment with generated assets
3. Asset serving utilities
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from functools import lru_cache


class Phase1AssetLoader:
    """Load and manage Phase 1 generated assets."""
    
    def __init__(self, assets_dir: str = "generated_assets"):
        self.assets_dir = Path(assets_dir)
        self.manifest_path = self.assets_dir / "phase1_manifest.json"
        self._manifest = None
        self._ascii_cache = {}
        self._table_cache = {}
        
        if not self.assets_dir.exists():
            raise FileNotFoundError(f"Assets directory not found: {assets_dir}")
        
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {self.manifest_path}")
    
    def load_manifest(self) -> Dict[str, Any]:
        """Load the manifest file."""
        if self._manifest is None:
            with self.manifest_path.open("r", encoding="utf-8") as f:
                self._manifest = json.load(f)
        return self._manifest
    
    def get_ascii_diagram(self, lesson_id: str) -> Optional[str]:
        """Get ASCII diagram for a lesson."""
        if lesson_id in self._ascii_cache:
            return self._ascii_cache[lesson_id]
        
        manifest = self.load_manifest()
        
        # Find in manifest
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
        
        manifest = self.load_manifest()
        
        # Find in manifest
        for item in manifest.get("truth_tables", []):
            if item["lesson_id"] == lesson_id:
                path = Path(item["path"])
                if path.exists():
                    with path.open("r", encoding="utf-8") as f:
                        content = f.read()
                    self._table_cache[lesson_id] = content
                    return content
        
        return None
    
    def enrich_lesson(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich lesson with generated assets."""
        lesson_id = lesson.get("id")
        if not lesson_id:
            return lesson
        
        # Add ASCII diagram
        ascii_diagram = self.get_ascii_diagram(lesson_id)
        if ascii_diagram:
            lesson["generated_assets"] = lesson.get("generated_assets", {})
            lesson["generated_assets"]["ascii_diagram"] = {
                "type": "text",
                "content": ascii_diagram,
                "format": "ascii"
            }
        
        # Add truth table
        truth_table = self.get_truth_table(lesson_id)
        if truth_table:
            lesson["generated_assets"] = lesson.get("generated_assets", {})
            lesson["generated_assets"]["truth_table"] = {
                "type": "html",
                "content": truth_table,
                "format": "interactive_html"
            }
        
        return lesson
    
    def enrich_lessons(self, lessons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich multiple lessons with assets."""
        return [self.enrich_lesson(lesson) for lesson in lessons]
    
    def get_assets_summary(self) -> Dict[str, Any]:
        """Get summary of loaded assets."""
        manifest = self.load_manifest()
        return {
            "total_ascii_diagrams": len(manifest.get("ascii_diagrams", [])),
            "total_truth_tables": len(manifest.get("truth_tables", [])),
            "total_assets": len(manifest.get("ascii_diagrams", [])) + len(manifest.get("truth_tables", [])),
            "by_subject": self._summarize_by_subject(manifest),
            "by_type": self._summarize_by_type(manifest),
        }
    
    @staticmethod
    def _summarize_by_subject(manifest: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
        """Summarize assets by subject."""
        summary = {}
        
        for item in manifest.get("ascii_diagrams", []):
            subject = item.get("subject", "Unknown")
            if subject not in summary:
                summary[subject] = {"ascii": 0, "tables": 0}
            summary[subject]["ascii"] += 1
        
        for item in manifest.get("truth_tables", []):
            subject = item.get("subject", "Unknown")
            if subject not in summary:
                summary[subject] = {"ascii": 0, "tables": 0}
            summary[subject]["tables"] += 1
        
        return summary
    
    @staticmethod
    def _summarize_by_type(manifest: Dict[str, Any]) -> Dict[str, int]:
        """Summarize ASCII diagrams by type."""
        types = {}
        
        for item in manifest.get("ascii_diagrams", []):
            dtype = item.get("type", "unknown")
            types[dtype] = types.get(dtype, 0) + 1
        
        return types


def get_asset_loader(assets_dir: str = "generated_assets") -> Phase1AssetLoader:
    """Factory function to get asset loader."""
    return Phase1AssetLoader(assets_dir)


# Global instance
_asset_loader: Optional[Phase1AssetLoader] = None


def initialize_asset_loader(assets_dir: str = "generated_assets") -> Phase1AssetLoader:
    """Initialize global asset loader."""
    global _asset_loader
    if _asset_loader is None:
        _asset_loader = Phase1AssetLoader(assets_dir)
    return _asset_loader


def get_global_asset_loader() -> Optional[Phase1AssetLoader]:
    """Get global asset loader instance."""
    return _asset_loader
