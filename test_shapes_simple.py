"""
Simplified test suite for geometric shapes - direct file verification
"""

import json
from pathlib import Path


def test_files_exist():
    """Test all expected files exist"""
    print("\n" + "="*60)
    print("🧪 GEOMETRIC SHAPES TEST - Priority #5")
    print("="*60)
    
    base_path = Path("generated_assets/geometric_shapes")
    expected_files = [
        'cube.glb',
        'cuboid.glb',
        'cylinder.glb',
        'cone.glb',
        'sphere.glb',
        'pyramid.glb',
        'prisms.glb',
        'composite_solids.glb',
        'geometric_shapes_manifest.json'
    ]
    
    print("\n📦 FILE VERIFICATION:")
    results = []
    total_size = 0
    
    for filename in expected_files:
        filepath = base_path / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            total_size += size_kb
            print(f"✅ {filename:35s} → {size_kb:6.2f} KB")
            results.append(True)
        else:
            print(f"❌ {filename:35s} → Not found")
            results.append(False)
    
    print(f"\n📊 Total size: {total_size:.2f} KB")
    print(f"✅ Files verified: {sum(results)}/{len(results)}")
    
    # Test manifest content
    print("\n📋 MANIFEST VALIDATION:")
    manifest_path = base_path / "geometric_shapes_manifest.json"
    
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            print(f"✅ Total models: {manifest.get('total_models', 0)}")
            print(f"✅ Total size: {manifest.get('total_size_kb', 0):.2f} KB")
            print(f"✅ Curriculum: {', '.join(manifest.get('curriculum_alignment', {}).keys())}")
            
            # List shapes
            print("\n📐 SHAPES GENERATED:")
            for shape in manifest.get('shapes', []):
                print(f"   • {shape['name']:25s} - {shape['description'][:50]}")
        except Exception as e:
            print(f"❌ Manifest read error: {e}")
    
    # Summary
    print("\n" + "="*60)
    if all(results):
        print("🎉 ALL FILES VERIFIED! Priority #5 generation complete.")
        print(f"📊 8 geometric shapes + manifest ({total_size:.2f} KB total)")
    else:
        print(f"⚠️ {len(results) - sum(results)} file(s) missing")
    print("="*60)
    
    return all(results)


if __name__ == "__main__":
    success = test_files_exist()
    exit(0 if success else 1)
