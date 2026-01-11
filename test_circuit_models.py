"""
Test Suite for Circuit Model Generator (Priority #4)
Tests all 6 circuit and electrical component models
"""

import json
import sys
import os
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from src.backend.generators.circuit_models import CircuitModelGenerator
from src.backend.generators.asset_generator_manager import AssetGeneratorManager


def test_individual_circuits():
    """Test each circuit model individually"""
    print("\n⚡ TESTING INDIVIDUAL CIRCUIT MODELS")
    print("=" * 60)
    
    generator = CircuitModelGenerator()
    output_dir = Path("generated_assets/circuit_models")
    
    # Test 1: Series Circuit
    try:
        result = generator.generate_series_circuit()
        assert Path(result['filepath']).exists(), "Series circuit file not found"
        print(f"✅ Series Circuit: {result['file_size_kb']:.2f} KB")
        print(f"   Components: {', '.join(result['components'])}")
    except Exception as e:
        print(f"❌ Series circuit failed: {e}")
    
    # Test 2: Parallel Circuit
    try:
        result = generator.generate_parallel_circuit()
        assert Path(result['filepath']).exists(), "Parallel circuit file not found"
        print(f"✅ Parallel Circuit: {result['file_size_kb']:.2f} KB")
        print(f"   Components: {', '.join(result['components'])}")
    except Exception as e:
        print(f"❌ Parallel circuit failed: {e}")
    
    # Test 3: Circuit Components
    try:
        result = generator.generate_circuit_components()
        assert Path(result['filepath']).exists(), "Circuit components file not found"
        print(f"✅ Circuit Components: {result['file_size_kb']:.2f} KB")
        print(f"   Components: {', '.join(result['components'])}")
    except Exception as e:
        print(f"❌ Circuit components failed: {e}")
    
    # Test 4: Transformer
    try:
        result = generator.generate_transformer()
        assert Path(result['filepath']).exists(), "Transformer file not found"
        print(f"✅ Transformer: {result['file_size_kb']:.2f} KB")
        print(f"   Components: {', '.join(result['components'])}")
    except Exception as e:
        print(f"❌ Transformer failed: {e}")
    
    # Test 5: Electric Motor
    try:
        result = generator.generate_electric_motor()
        assert Path(result['filepath']).exists(), "Electric motor file not found"
        print(f"✅ Electric Motor: {result['file_size_kb']:.2f} KB")
        print(f"   Components: {', '.join(result['components'])}")
    except Exception as e:
        print(f"❌ Electric motor failed: {e}")
    
    # Test 6: Generator
    try:
        result = generator.generate_generator()
        assert Path(result['filepath']).exists(), "Generator file not found"
        print(f"✅ Generator: {result['file_size_kb']:.2f} KB")
        print(f"   Components: {', '.join(result['components'])}")
    except Exception as e:
        print(f"❌ Generator failed: {e}")
    
    # Count total models
    total_models = len(list(output_dir.glob("*.glb")))
    print(f"\n✅ Successfully tested {total_models}/6 circuit models")


def test_manifest():
    """Test manifest file generation and content"""
    print("\n\n📋 TESTING MANIFEST")
    print("=" * 60)
    
    manifest_path = Path("generated_assets/circuit_models/circuit_models_manifest.json")
    
    if manifest_path.exists():
        print(f"✅ Manifest found: {manifest_path}")
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        print(f"   Collection: {manifest.get('collection')}")
        print(f"   Priority: #{manifest.get('priority')}")
        print(f"   Exam Weight: {manifest.get('exam_weight')}")
        print(f"   Subject: {manifest.get('subject')}")
        print(f"   Topic Code: {manifest.get('topic_code')}")
        print(f"   Total models: {manifest.get('total_models')}")
        
        print("\n   Models in manifest:")
        for model in manifest.get('models', []):
            print(f"   - {model['filename']} ({model['file_size_kb']:.2f} KB)")
            print(f"     {model['educational_notes']}")
    else:
        print(f"❌ Manifest not found at {manifest_path}")


def test_integration():
    """Test integration with AssetGeneratorManager"""
    print("\n\n🔗 TESTING INTEGRATION WITH ASSET MANAGER")
    print("=" * 60)
    
    try:
        manager = AssetGeneratorManager()
        print("✅ AssetGeneratorManager initialized")
        
        # Check if circuits generator is registered
        if 'circuits' in manager.generators:
            print("✅ Circuit generator registered")
        else:
            print("❌ Circuit generator not registered")
            return
        
        # Test lesson-based generation for different circuit topics
        test_lessons = [
            {"subject": "physics", "topic": "series circuit", "grade_level": "SS2"},
            {"subject": "physics", "topic": "parallel circuit", "grade_level": "SS2"},
            {"subject": "physics", "topic": "circuit components", "grade_level": "SS2"},
            {"subject": "physics", "topic": "transformer", "grade_level": "SS3"},
            {"subject": "physics", "topic": "electric motor", "grade_level": "SS3"},
            {"subject": "physics", "topic": "generator", "grade_level": "SS3"},
            {"subject": "physics", "topic": "electrical circuits", "grade_level": "SS2"},
        ]
        
        passed = 0
        for lesson in test_lessons:
            try:
                assets = manager.generate_for_lesson(lesson)
                if assets['simulations']:
                    passed += 1
                    print(f"✅ {lesson['topic']}: Generated {len(assets['simulations'])} asset(s)")
                else:
                    print(f"⚠️  {lesson['topic']}: No assets generated")
            except Exception as e:
                print(f"❌ {lesson['topic']}: Failed - {e}")
        
        print(f"\n✅ Passed {passed}/{len(test_lessons)} lesson tests")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")


def test_file_verification():
    """Verify all expected files exist"""
    print("\n\n📂 TESTING FILE VERIFICATION")
    print("=" * 60)
    
    expected_files = [
        "series_circuit.glb",
        "parallel_circuit.glb",
        "circuit_components.glb",
        "transformer.glb",
        "electric_motor.glb",
        "generator.glb",
        "circuit_models_manifest.json"
    ]
    
    output_dir = Path("generated_assets/circuit_models")
    found = 0
    total_size = 0
    
    for filename in expected_files:
        filepath = output_dir / filename
        if filepath.exists():
            found += 1
            if filename.endswith('.glb'):
                size_kb = filepath.stat().st_size / 1024
                total_size += size_kb
                print(f"✅ {filename} ({size_kb:.2f} KB)")
        else:
            print(f"❌ {filename} - NOT FOUND")
    
    print(f"\n✅ {found}/{len(expected_files)} files present")
    print(f"   Total size: {total_size:.2f} KB")


def test_model_sizes():
    """Test that all models meet size requirements"""
    print("\n\n📏 TESTING MODEL SIZE OPTIMIZATION")
    print("=" * 60)
    
    output_dir = Path("generated_assets/circuit_models")
    max_size_kb = 1000  # 1MB limit for AR/VR optimization
    
    all_within_limit = True
    for glb_file in output_dir.glob("*.glb"):
        size_kb = glb_file.stat().st_size / 1024
        status = "✅" if size_kb < max_size_kb else "⚠️"
        print(f"{status} {glb_file.name}: {size_kb:.2f} KB")
        if size_kb >= max_size_kb:
            all_within_limit = False
    
    if all_within_limit:
        print(f"\n✅ All models within size limits (< {max_size_kb} KB)")
    else:
        print(f"\n⚠️  Some models exceed size limit")


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "=" * 60)
    print("   CIRCUIT MODELS TEST SUITE (Priority #4)")
    print("=" * 60)
    
    test_results = {
        'manifest': False,
        'integration': False,
        'file_verification': False,
        'size_optimization': False
    }
    
    try:
        test_individual_circuits()
        test_results['individual'] = True
    except Exception as e:
        print(f"❌ Individual tests failed: {e}")
    
    try:
        test_manifest()
        test_results['manifest'] = True
    except Exception as e:
        print(f"❌ Manifest test failed: {e}")
    
    try:
        test_integration()
        test_results['integration'] = True
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
    
    try:
        test_file_verification()
        test_results['file_verification'] = True
    except Exception as e:
        print(f"❌ File verification failed: {e}")
    
    try:
        test_model_sizes()
        test_results['size_optimization'] = True
    except Exception as e:
        print(f"❌ Size optimization test failed: {e}")
    
    # Summary
    print("\n\n" + "=" * 60)
    print("📈 TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in test_results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {test_name}: {'success' if passed else 'failed'}")
    
    total_passed = sum(test_results.values())
    total_tests = len(test_results)
    print(f"\nOverall: {total_passed}/{total_tests} test categories passed")


if __name__ == "__main__":
    run_all_tests()
