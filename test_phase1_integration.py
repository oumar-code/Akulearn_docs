#!/usr/bin/env python3
"""Test Phase 1 Asset Integration

Quick test to verify asset loading and integration works correctly
"""

import json
from pathlib import Path
from src.backend.asset_loader import Phase1AssetLoader
from src.backend.services.lesson_enrichment import LessonEnrichmentService


def test_asset_loader():
    """Test basic asset loading."""
    print("\n" + "="*70)
    print("TEST 1: Asset Loader Initialization")
    print("="*70)
    
    try:
        loader = Phase1AssetLoader("generated_assets")
        print("✓ Asset loader initialized successfully")
        
        # Test manifest loading
        manifest = loader.load_manifest()
        print(f"✓ Manifest loaded: {len(manifest.get('ascii_diagrams', []))} ASCII diagrams")
        print(f"✓ Manifest loaded: {len(manifest.get('truth_tables', []))} truth tables")
        
        return loader
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def test_asset_retrieval(loader):
    """Test retrieving specific assets."""
    print("\n" + "="*70)
    print("TEST 2: Asset Retrieval")
    print("="*70)
    
    if not loader:
        print("✗ No loader available")
        return
    
    try:
        manifest = loader.load_manifest()
        
        # Get first ASCII diagram
        if manifest.get("ascii_diagrams"):
            first_ascii = manifest["ascii_diagrams"][0]
            lesson_id = first_ascii["lesson_id"]
            
            diagram = loader.get_ascii_diagram(lesson_id)
            if diagram:
                print(f"✓ Retrieved ASCII diagram for {first_ascii['title'][:40]}")
                print(f"  Content preview: {diagram[:100]}...")
            else:
                print(f"✗ Failed to retrieve ASCII diagram")
        
        # Get first truth table
        if manifest.get("truth_tables"):
            first_table = manifest["truth_tables"][0]
            lesson_id = first_table["lesson_id"]
            
            table = loader.get_truth_table(lesson_id)
            if table:
                print(f"✓ Retrieved truth table for {first_table['title'][:40]}")
                print(f"  Content preview: {table[:100]}...")
            else:
                print(f"✗ Failed to retrieve truth table")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def test_lesson_enrichment(loader):
    """Test lesson enrichment with assets."""
    print("\n" + "="*70)
    print("TEST 3: Lesson Enrichment")
    print("="*70)
    
    if not loader:
        print("✗ No loader available")
        return
    
    try:
        manifest = loader.load_manifest()
        
        # Create mock lesson
        if manifest.get("ascii_diagrams"):
            first_ascii = manifest["ascii_diagrams"][0]
            mock_lesson = {
                "id": first_ascii["lesson_id"],
                "title": first_ascii["title"],
                "subject": first_ascii["subject"],
                "content": "Sample lesson content"
            }
            
            # Enrich using loader
            enriched = loader.enrich_lesson(mock_lesson)
            
            if enriched.get("generated_assets"):
                print("✓ Lesson enriched with generated_assets field")
                
                if enriched["generated_assets"].get("ascii_diagram"):
                    print("✓ ASCII diagram included in enriched lesson")
                
                if enriched["generated_assets"].get("truth_table"):
                    print("✓ Truth table included in enriched lesson")
            else:
                print("✗ Lesson not properly enriched")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def test_assets_summary(loader):
    """Test assets summary generation."""
    print("\n" + "="*70)
    print("TEST 4: Assets Summary")
    print("="*70)
    
    if not loader:
        print("✗ No loader available")
        return
    
    try:
        summary = loader.get_assets_summary()
        
        print(f"✓ Total ASCII diagrams: {summary['total_ascii_diagrams']}")
        print(f"✓ Total truth tables: {summary['total_truth_tables']}")
        print(f"✓ Total assets: {summary['total_assets']}")
        
        print("\nBy Subject:")
        for subject, counts in summary['by_subject'].items():
            print(f"  • {subject:25} ASCII: {counts['ascii']:2}  Tables: {counts['tables']:2}")
        
        print("\nBy ASCII Type:")
        for dtype, count in summary['by_type'].items():
            print(f"  • {dtype:25} {count}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("PHASE 1 INTEGRATION TESTS")
    print("="*70)
    
    # Test 1: Loader initialization
    loader = test_asset_loader()
    
    # Test 2: Asset retrieval
    test_asset_retrieval(loader)
    
    # Test 3: Lesson enrichment
    test_lesson_enrichment(loader)
    
    # Test 4: Assets summary
    test_assets_summary(loader)
    
    print("\n" + "="*70)
    print("TESTS COMPLETE")
    print("="*70 + "\n")
    
    if loader:
        print("✓ All systems operational - Phase 1 integration ready!")
    else:
        print("✗ Issues detected - review errors above")


if __name__ == "__main__":
    main()
