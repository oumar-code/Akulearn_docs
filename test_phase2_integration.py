#!/usr/bin/env python3
"""
Phase 2 Integration Tests

Tests for:
1. Extended asset loader (Phase 1 & 2)
2. Phase 2 graph loading
3. API endpoints for graphs
4. Lesson enrichment with graphs
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.backend.extended_asset_loader import ExtendedAssetLoader
from src.backend.services.lesson_enrichment import LessonEnrichmentService


def test_extended_loader_initialization():
    """Test that extended loader can be initialized."""
    print("TEST 1: Extended Loader Initialization")
    
    try:
        loader = ExtendedAssetLoader("generated_assets")
        print("  ✓ Loader initialized successfully")
        
        # Check manifests exist
        p1_manifest = loader.load_phase1_manifest()
        p2_manifest = loader.load_phase2_manifest()
        
        print(f"  ✓ Phase 1 manifest loaded: {len(p1_manifest.get('ascii_diagrams', []))} ASCII + {len(p1_manifest.get('truth_tables', []))} tables")
        print(f"  ✓ Phase 2 manifest loaded: {sum(len(p2_manifest.get(k, [])) for k in ['function_graphs', 'bar_charts', 'pie_charts', 'line_charts'])} graphs")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_phase2_graph_loading():
    """Test that Phase 2 graphs can be loaded."""
    print("\nTEST 2: Phase 2 Graph Loading")
    
    try:
        loader = ExtendedAssetLoader("generated_assets")
        manifest = loader.load_phase2_manifest()
        
        if not any(manifest.get(k, []) for k in ["function_graphs", "bar_charts", "pie_charts", "line_charts"]):
            print("  ⚠ No graphs found in manifest")
            return False
        
        # Find a lesson with graphs
        for graph_type in ["function_graphs", "bar_charts", "pie_charts", "line_charts"]:
            for graph in manifest.get(graph_type, []):
                lesson_id = graph.get("lesson_id")
                if lesson_id:
                    graphs = loader.get_graphs_for_lesson(lesson_id)
                    print(f"  ✓ Found graphs for lesson {lesson_id}")
                    print(f"    - Function graphs: {len(graphs.get('function_graphs', []))}")
                    print(f"    - Bar charts: {len(graphs.get('bar_charts', []))}")
                    print(f"    - Pie charts: {len(graphs.get('pie_charts', []))}")
                    print(f"    - Line charts: {len(graphs.get('line_charts', []))}")
                    return True
        
        return False
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_graph_svg_retrieval():
    """Test that graph SVG content can be retrieved."""
    print("\nTEST 3: Graph SVG Retrieval")
    
    try:
        loader = ExtendedAssetLoader("generated_assets")
        manifest = loader.load_phase2_manifest()
        
        # Find first graph
        for graph_type in ["function_graphs", "bar_charts", "pie_charts", "line_charts"]:
            for graph in manifest.get(graph_type, []):
                graph_id = graph.get("id")
                svg_content = loader.get_graph_svg(graph_id)
                
                if svg_content:
                    print(f"  ✓ Retrieved SVG for graph {graph_id}")
                    print(f"    - Content length: {len(svg_content)} bytes")
                    print(f"    - Valid SVG: {'<svg' in svg_content.lower()}")
                    return True
        
        print("  ⚠ No graphs found to test")
        return False
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_lesson_enrichment_with_graphs():
    """Test that lessons are enriched with Phase 2 graphs."""
    print("\nTEST 4: Lesson Enrichment with Graphs")
    
    try:
        loader = ExtendedAssetLoader("generated_assets")
        
        # Find a lesson with graphs
        manifest = loader.load_phase2_manifest()
        test_lesson_id = None
        
        for graph_type in manifest.keys():
            for graph in manifest.get(graph_type, []):
                test_lesson_id = graph.get("lesson_id")
                if test_lesson_id:
                    break
            if test_lesson_id:
                break
        
        if not test_lesson_id:
            print("  ⚠ No lesson with graphs found")
            return False
        
        # Create test lesson
        test_lesson = {
            "id": test_lesson_id,
            "title": "Test Lesson",
            "content": "Test content"
        }
        
        # Enrich lesson
        enriched = loader.enrich_lesson(test_lesson)
        
        print(f"  ✓ Enriched lesson {test_lesson_id}")
        
        assets = enriched.get("generated_assets", {})
        if assets.get("graphs"):
            print(f"  ✓ Graphs added to generated_assets")
            print(f"    - Total graphs: {assets['graphs'].get('total_graphs', 0)}")
            print(f"    - Graph types included: {list(assets['graphs'].get('graphs_by_type', {}).keys())}")
            return True
        else:
            print(f"  ⚠ No graphs in enriched lesson")
            return False
            
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_assets_summary():
    """Test that assets summary is generated correctly."""
    print("\nTEST 5: Assets Summary")
    
    try:
        loader = ExtendedAssetLoader("generated_assets")
        summary = loader.get_assets_summary()
        
        print(f"  ✓ Generated assets summary")
        print(f"    Phase 1:")
        print(f"      - ASCII diagrams: {summary['phase1'].get('total_ascii_diagrams', 0)}")
        print(f"      - Truth tables: {summary['phase1'].get('total_truth_tables', 0)}")
        print(f"      - Total: {summary['phase1'].get('total', 0)}")
        print(f"    Phase 2:")
        print(f"      - Function graphs: {summary['phase2'].get('function_graphs', 0)}")
        print(f"      - Bar charts: {summary['phase2'].get('bar_charts', 0)}")
        print(f"      - Pie charts: {summary['phase2'].get('pie_charts', 0)}")
        print(f"      - Line charts: {summary['phase2'].get('line_charts', 0)}")
        print(f"      - Total: {summary['phase2'].get('total', 0)}")
        print(f"    Combined total: {summary.get('combined_total', 0)}")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_multiple_lessons_enrichment():
    """Test enriching multiple lessons."""
    print("\nTEST 6: Multiple Lessons Enrichment")
    
    try:
        loader = ExtendedAssetLoader("generated_assets")
        
        # Create test lessons
        test_lessons = [
            {"id": f"lesson_{i}", "title": f"Lesson {i}", "content": f"Content {i}"}
            for i in range(1, 4)
        ]
        
        # Enrich lessons
        enriched_lessons = loader.enrich_lessons(test_lessons)
        
        enriched_count = sum(
            1 for lesson in enriched_lessons
            if lesson.get("generated_assets") and (
                lesson["generated_assets"].get("ascii_diagram") or
                lesson["generated_assets"].get("truth_table") or
                lesson["generated_assets"].get("graphs")
            )
        )
        
        print(f"  ✓ Enriched {len(test_lessons)} lessons")
        print(f"    - Lessons with generated assets: {enriched_count}")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Phase 2 Integration Tests")
    print("=" * 60)
    
    tests = [
        test_extended_loader_initialization,
        test_phase2_graph_loading,
        test_graph_svg_retrieval,
        test_lesson_enrichment_with_graphs,
        test_assets_summary,
        test_multiple_lessons_enrichment
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
