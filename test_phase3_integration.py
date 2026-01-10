#!/usr/bin/env python3
"""
Phase 3 Integration Tests

Tests for Phase 3 specialized diagram system including:
- Asset loader functionality
- API endpoints
- Lesson enrichment
- Manifest integrity
"""

import pytest
import json
from pathlib import Path
from src.backend.phase3_asset_loader import Phase3AssetLoader, initialize_phase3_loader, get_phase3_loader


class TestPhase3AssetLoader:
    """Test Phase 3 asset loader functionality."""
    
    @pytest.fixture
    def loader(self):
        """Create Phase 3 asset loader instance."""
        return Phase3AssetLoader("generated_assets")
    
    def test_loader_initialization(self, loader):
        """Test loader initializes correctly."""
        assert loader is not None
        assert loader.assets_dir.exists()
        assert loader.phase3_manifest_path.exists()
    
    def test_load_phase3_manifest(self, loader):
        """Test Phase 3 manifest loading."""
        manifest = loader.load_phase3_manifest()
        assert manifest is not None
        assert "metadata" in manifest
        assert "venn_diagrams" in manifest
        assert "flowcharts" in manifest
        assert "electrical_circuits" in manifest
        assert "logic_circuits" in manifest
        assert "chemical_reactions" in manifest
    
    def test_manifest_metadata(self, loader):
        """Test manifest metadata structure."""
        manifest = loader.load_phase3_manifest()
        metadata = manifest.get("metadata", {})
        
        assert "total_diagrams" in metadata
        assert "phase" in metadata
        assert metadata["phase"] == 3
        assert isinstance(metadata["total_diagrams"], int)
        assert metadata["total_diagrams"] > 0
    
    def test_get_diagrams_for_lesson(self, loader):
        """Test retrieving diagrams for a lesson."""
        manifest = loader.load_phase3_manifest()
        
        # Find a lesson ID from manifest
        lesson_id = None
        for category in ["venn_diagrams", "flowcharts", "electrical_circuits"]:
            items = manifest.get(category, [])
            if items:
                lesson_id = items[0].get("lesson_id")
                break
        
        if lesson_id:
            diagrams = loader.get_diagrams_for_lesson(lesson_id)
            assert isinstance(diagrams, list)
            assert len(diagrams) > 0
            
            for diagram in diagrams:
                assert hasattr(diagram, 'lesson_id')
                assert hasattr(diagram, 'diagram_id')
                assert hasattr(diagram, 'diagram_type')
                assert hasattr(diagram, 'path')
    
    def test_get_diagram_by_id(self, loader):
        """Test retrieving a specific diagram by ID."""
        manifest = loader.load_phase3_manifest()
        
        # Get first diagram ID
        diagram_id = None
        for category in manifest.keys():
            if category != "metadata":
                items = manifest.get(category, [])
                if items:
                    diagram_id = items[0].get("id")
                    break
        
        if diagram_id:
            diagram = loader.get_diagram_by_id(diagram_id)
            assert diagram is not None
            assert diagram.diagram_id == diagram_id
    
    def test_get_diagrams_by_type(self, loader):
        """Test retrieving diagrams by type."""
        manifest = loader.load_phase3_manifest()
        
        # Test venn_2 diagrams
        if manifest.get("venn_diagrams"):
            venn_diagrams = loader.get_diagrams_by_type("venn_2")
            assert isinstance(venn_diagrams, list)
            for diagram in venn_diagrams:
                assert diagram.diagram_type == "venn_2"
        
        # Test circuit diagrams
        if manifest.get("electrical_circuits"):
            circuits = loader.get_diagrams_by_type("circuit_electrical")
            assert isinstance(circuits, list)
            for diagram in circuits:
                assert diagram.diagram_type == "circuit_electrical"
    
    def test_load_diagram_svg(self, loader):
        """Test loading SVG content for diagrams."""
        manifest = loader.load_phase3_manifest()
        
        # Get first diagram
        diagram_id = None
        for category in manifest.keys():
            if category != "metadata":
                items = manifest.get(category, [])
                if items:
                    diagram_id = items[0].get("id")
                    break
        
        if diagram_id:
            diagram = loader.get_diagram_by_id(diagram_id)
            svg_content = loader.load_diagram_svg(diagram)
            
            assert svg_content is not None
            assert isinstance(svg_content, str)
            assert "<svg" in svg_content
            assert "</svg>" in svg_content
    
    def test_get_phase3_stats(self, loader):
        """Test Phase 3 statistics."""
        stats = loader.get_phase3_stats()
        
        assert stats is not None
        assert "total_diagrams" in stats
        assert "venn_diagrams" in stats
        assert "flowcharts" in stats
        assert "electrical_circuits" in stats
        assert "logic_circuits" in stats
        assert "chemical_reactions" in stats
        
        assert stats["total_diagrams"] > 0
    
    def test_enrich_lesson(self, loader):
        """Test lesson enrichment with Phase 3 diagrams."""
        manifest = loader.load_phase3_manifest()
        
        # Find a lesson ID
        lesson_id = None
        for category in ["venn_diagrams", "flowcharts"]:
            items = manifest.get(category, [])
            if items:
                lesson_id = items[0].get("lesson_id")
                break
        
        if lesson_id:
            lesson = {"id": lesson_id, "title": "Test Lesson"}
            enriched = loader.enrich_lesson(lesson)
            
            assert "phase3_diagrams" in enriched or "generated_assets" in enriched
            assert "phase3_diagram_count" in enriched or enriched.get("phase3_diagrams")


class TestPhase3GlobalLoader:
    """Test global loader singleton pattern."""
    
    def test_initialize_phase3_loader(self):
        """Test initializing global loader."""
        loader = initialize_phase3_loader()
        assert loader is not None
        assert isinstance(loader, Phase3AssetLoader)
    
    def test_get_phase3_loader(self):
        """Test getting global loader instance."""
        initialize_phase3_loader()
        loader = get_phase3_loader()
        assert loader is not None


class TestPhase3Manifest:
    """Test Phase 3 manifest file integrity."""
    
    def test_manifest_exists(self):
        """Test manifest file exists."""
        manifest_path = Path("generated_assets/phase3_manifest.json")
        assert manifest_path.exists()
    
    def test_manifest_valid_json(self):
        """Test manifest is valid JSON."""
        manifest_path = Path("generated_assets/phase3_manifest.json")
        with manifest_path.open("r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        assert manifest is not None
        assert isinstance(manifest, dict)
    
    def test_manifest_structure(self):
        """Test manifest has correct structure."""
        manifest_path = Path("generated_assets/phase3_manifest.json")
        with manifest_path.open("r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        # Check required categories
        required_categories = [
            "venn_diagrams",
            "flowcharts",
            "timelines",
            "electrical_circuits",
            "logic_circuits",
            "molecular_structures",
            "chemical_reactions",
            "metadata"
        ]
        
        for category in required_categories:
            assert category in manifest, f"Missing category: {category}"
    
    def test_diagram_entries_valid(self):
        """Test all diagram entries have required fields."""
        manifest_path = Path("generated_assets/phase3_manifest.json")
        with manifest_path.open("r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        categories = [k for k in manifest.keys() if k != "metadata"]
        
        for category in categories:
            items = manifest.get(category, [])
            for item in items:
                assert "id" in item
                assert "lesson_id" in item
                assert "type" in item
                assert "path" in item
                assert "title" in item or "subject" in item


class TestPhase3DiagramFiles:
    """Test generated diagram files."""
    
    def test_diagrams_directory_exists(self):
        """Test diagrams directory exists."""
        diagrams_dir = Path("generated_assets")
        assert diagrams_dir.exists()
    
    def test_svg_files_exist(self):
        """Test SVG files referenced in manifest exist."""
        manifest_path = Path("generated_assets/phase3_manifest.json")
        with manifest_path.open("r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        categories = [k for k in manifest.keys() if k != "metadata"]
        missing_files = []
        
        for category in categories:
            items = manifest.get(category, [])
            for item in items[:5]:  # Check first 5 of each type
                path = Path(item["path"])
                if not path.exists():
                    missing_files.append(str(path))
        
        assert len(missing_files) == 0, f"Missing files: {missing_files}"
    
    def test_svg_files_valid(self):
        """Test SVG files contain valid SVG content."""
        manifest_path = Path("generated_assets/phase3_manifest.json")
        with manifest_path.open("r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        # Test first diagram of each type
        for category in ["venn_diagrams", "flowcharts", "electrical_circuits"]:
            items = manifest.get(category, [])
            if items:
                path = Path(items[0]["path"])
                if path.exists():
                    with path.open("r", encoding="utf-8") as f:
                        content = f.read()
                    
                    assert "<svg" in content
                    assert "</svg>" in content
                    assert "xmlns" in content


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PHASE 3 INTEGRATION TESTS")
    print("=" * 70)
    
    # Run with pytest
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])
