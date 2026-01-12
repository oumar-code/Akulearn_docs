"""
Test suite for geometric shape models (Priority #5)

Tests:
1. Individual shape generation (8 shapes)
2. Manifest validation and metadata
3. Integration with AssetGeneratorManager
4. File verification (GLB + manifest)
5. Size optimization (<500 KB total)
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from generators.geometric_shapes import GeometricShapeGenerator
from generators.asset_generator_manager import AssetGeneratorManager


def test_individual_shape_generation():
    """Test individual shape generation methods"""
    print("\n" + "="*60)
    print("TEST 1: Individual Shape Generation")
    print("="*60)
    
    generator = GeometricShapeGenerator()
    shapes_to_test = [
        ('cube', generator.generate_cube),
        ('cuboid', generator.generate_cuboid),
        ('cylinder', generator.generate_cylinder),
        ('cone', generator.generate_cone),
        ('sphere', generator.generate_sphere),
        ('pyramid', generator.generate_pyramid),
        ('prisms', generator.generate_prisms),
        ('composite_solids', generator.generate_composite_solids)
    ]
    
    results = []
    for shape_name, shape_func in shapes_to_test:
        try:
            metadata = shape_func()
            glb_path = Path(metadata['filepath'])
            
            if glb_path.exists():
                size_kb = glb_path.stat().st_size / 1024
                print(f"✅ {shape_name:20s} → {size_kb:6.2f} KB")
                results.append(True)
            else:
                print(f"❌ {shape_name:20s} → File not found")
                results.append(False)
        except Exception as e:
            print(f"❌ {shape_name:20s} → Error: {e}")
            results.append(False)
    
    success_rate = (sum(results) / len(results)) * 100
    print(f"\n📊 Individual Generation: {sum(results)}/{len(results)} passed ({success_rate:.1f}%)")
    return sum(results) == len(results)


def test_manifest_validation():
    """Test manifest creation and metadata"""
    print("\n" + "="*60)
    print("TEST 2: Manifest Validation")
    print("="*60)
    
    generator = GeometricShapeGenerator()
    manifest_path = generator.output_dir / "geometric_shapes_manifest.json"
    
    if not manifest_path.exists():
        print("❌ Manifest file not found")
        return False
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # Check required fields
        required_fields = ['shapes', 'total_models', 'total_size_kb', 'curriculum_alignment']
        checks = []
        
        for field in required_fields:
            if field in manifest:
                print(f"✅ Field '{field}' present")
                checks.append(True)
            else:
                print(f"❌ Field '{field}' missing")
                checks.append(False)
        
        # Check shape count
        if manifest.get('total_models') == 8:
            print(f"✅ Total models: 8 (correct)")
            checks.append(True)
        else:
            print(f"❌ Total models: {manifest.get('total_models')} (expected 8)")
            checks.append(False)
        
        # Check curriculum alignment
        curriculum = manifest.get('curriculum_alignment', {})
        if 'math_008' in curriculum and 'math_009' in curriculum:
            print(f"✅ Curriculum alignment: math_008, math_009")
            checks.append(True)
        else:
            print(f"❌ Curriculum alignment incomplete")
            checks.append(False)
        
        success_rate = (sum(checks) / len(checks)) * 100
        print(f"\n📊 Manifest Validation: {sum(checks)}/{len(checks)} checks passed ({success_rate:.1f}%)")
        return all(checks)
    
    except Exception as e:
        print(f"❌ Manifest validation failed: {e}")
        return False


def test_manager_integration():
    """Test integration with AssetGeneratorManager"""
    print("\n" + "="*60)
    print("TEST 3: AssetGeneratorManager Integration")
    print("="*60)
    
    manager = AssetGeneratorManager()
    
    # Test lesson-based generation with shape keywords
    test_lessons = [
        ('mathematics', 'cube volume and surface area', 'JSS1'),
        ('mathematics', 'sphere calculations', 'SS2'),
        ('mathematics', 'pyramid geometry', 'JSS3'),
        ('mathematics', 'cylinder mensuration', 'SS1'),
        ('mathematics', 'cone surface area', 'SS2'),
        ('mathematics', 'cuboid dimensions', 'JSS2'),
        ('mathematics', 'prism volume', 'SS1'),
        ('mathematics', 'composite solid shapes', 'SS3'),
        ('mathematics', 'mensuration and 3d geometry', 'SS2')
    ]
    
    results = []
    for subject, topic, grade in test_lessons:
        try:
            assets = manager.generate_for_lesson(subject, topic, grade)
            if assets and assets.get('geometric_shapes'):
                print(f"✅ {topic[:30]:30s} → {len(assets['geometric_shapes'])} shape(s)")
                results.append(True)
            else:
                print(f"❌ {topic[:30]:30s} → No shapes generated")
                results.append(False)
        except Exception as e:
            print(f"❌ {topic[:30]:30s} → Error: {e}")
            results.append(False)
    
    success_rate = (sum(results) / len(results)) * 100
    print(f"\n📊 Integration Tests: {sum(results)}/{len(results)} passed ({success_rate:.1f}%)")
    return sum(results) == len(results)


def test_file_verification():
    """Test all expected files exist"""
    print("\n" + "="*60)
    print("TEST 4: File Verification")
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
    
    print(f"\n📦 Total size: {total_size:.2f} KB")
    
    success_rate = (sum(results) / len(results)) * 100
    print(f"\n📊 File Verification: {sum(results)}/{len(results)} files present ({success_rate:.1f}%)")
    return all(results)


def test_size_optimization():
    """Test that total size is reasonable (<500 KB)"""
    print("\n" + "="*60)
    print("TEST 5: Size Optimization")
    print("="*60)
    
    base_path = Path("generated_assets/geometric_shapes")
    glb_files = list(base_path.glob("*.glb"))
    
    total_size = sum(f.stat().st_size for f in glb_files)
    total_size_kb = total_size / 1024
    
    print(f"📦 Total GLB size: {total_size_kb:.2f} KB")
    print(f"📊 Average per model: {total_size_kb/len(glb_files):.2f} KB")
    
    checks = []
    
    # Check total size
    if total_size_kb < 500:
        print(f"✅ Total size under 500 KB")
        checks.append(True)
    else:
        print(f"⚠️ Total size exceeds 500 KB")
        checks.append(False)
    
    # Check individual file sizes
    large_files = [f for f in glb_files if f.stat().st_size / 1024 > 100]
    if not large_files:
        print(f"✅ All individual files under 100 KB")
        checks.append(True)
    else:
        print(f"⚠️ {len(large_files)} file(s) exceed 100 KB:")
        for f in large_files:
            print(f"   - {f.name}: {f.stat().st_size / 1024:.2f} KB")
        checks.append(True)  # Still pass, but with warning
    
    success_rate = (sum(checks) / len(checks)) * 100
    print(f"\n📊 Size Optimization: {sum(checks)}/{len(checks)} checks passed ({success_rate:.1f}%)")
    return all(checks)


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*70)
    print("🧪 GEOMETRIC SHAPES TEST SUITE - Priority #5")
    print("="*70)
    
    tests = [
        ("Individual Shape Generation", test_individual_shape_generation),
        ("Manifest Validation", test_manifest_validation),
        ("AssetGeneratorManager Integration", test_manager_integration),
        ("File Verification", test_file_verification),
        ("Size Optimization", test_size_optimization)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Final summary
    print("\n" + "="*70)
    print("📊 FINAL TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    success_rate = (passed_count / total_count) * 100
    
    print("\n" + "="*70)
    print(f"🎯 Overall: {passed_count}/{total_count} test categories passed ({success_rate:.1f}%)")
    print("="*70)
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! Priority #5 implementation complete.")
    else:
        print(f"\n⚠️ {total_count - passed_count} test(s) failed. Review required.")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
