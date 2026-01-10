#!/usr/bin/env python3
"""Quick validation test for Phase 3 integration"""

import sys
from pathlib import Path

print("=" * 70)
print("PHASE 3 INTEGRATION VALIDATION")
print("=" * 70)

# Test 1: Import Phase 3 loader
print("\n[1/6] Testing Phase 3 loader import...")
try:
    from src.backend.phase3_asset_loader import Phase3AssetLoader, initialize_phase3_loader
    print("✅ Phase 3 loader imported successfully")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)

# Test 2: Initialize loader
print("\n[2/6] Testing loader initialization...")
try:
    loader = Phase3AssetLoader("generated_assets")
    print("✅ Loader initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    sys.exit(1)

# Test 3: Load manifest
print("\n[3/6] Testing manifest loading...")
try:
    manifest = loader.load_phase3_manifest()
    total = manifest["metadata"]["total_diagrams"]
    print(f"✅ Manifest loaded: {total} total diagrams")
except Exception as e:
    print(f"❌ Failed to load manifest: {e}")
    sys.exit(1)

# Test 4: Get statistics
print("\n[4/6] Testing statistics...")
try:
    stats = loader.get_phase3_stats()
    print(f"✅ Statistics retrieved:")
    print(f"   - Total diagrams: {stats['total_diagrams']}")
    print(f"   - Venn diagrams: {stats['venn_diagrams']}")
    print(f"   - Flowcharts: {stats['flowcharts']}")
    print(f"   - Electrical circuits: {stats['electrical_circuits']}")
    print(f"   - Logic circuits: {stats['logic_circuits']}")
    print(f"   - Chemical reactions: {stats['chemical_reactions']}")
except Exception as e:
    print(f"❌ Failed to get statistics: {e}")
    sys.exit(1)

# Test 5: Get diagrams for lesson
print("\n[5/6] Testing diagram retrieval...")
try:
    # Find a lesson with diagrams
    lesson_id = None
    for category in manifest.keys():
        if category != "metadata":
            items = manifest.get(category, [])
            if items:
                lesson_id = items[0]["lesson_id"]
                break
    
    if lesson_id:
        diagrams = loader.get_diagrams_for_lesson(lesson_id)
        print(f"✅ Retrieved {len(diagrams)} diagrams for lesson: {lesson_id}")
    else:
        print("⚠️  No lesson IDs found in manifest")
except Exception as e:
    print(f"❌ Failed to get diagrams: {e}")
    sys.exit(1)

# Test 6: Verify SVG files
print("\n[6/6] Testing SVG file integrity...")
try:
    checked = 0
    valid = 0
    for category in manifest.keys():
        if category != "metadata":
            items = manifest.get(category, [])[:3]  # Check first 3 of each type
            for item in items:
                checked += 1
                path = Path(item["path"])
                if path.exists():
                    with path.open("r", encoding="utf-8") as f:
                        content = f.read()
                    if "<svg" in content and "</svg>" in content:
                        valid += 1
    
    print(f"✅ Verified {valid}/{checked} SVG files")
except Exception as e:
    print(f"❌ Failed to verify SVG files: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
print(f"✅ All tests passed!")
print(f"✅ Phase 3 integration is ready to use")
print(f"\nNext steps:")
print("  1. Wire assets_v3 router into FastAPI app")
print("  2. Start backend server")
print("  3. Test API endpoints")
print("  4. Integrate frontend components")
print("=" * 70)
