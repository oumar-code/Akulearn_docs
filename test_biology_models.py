"""
Comprehensive test for biology 3D model generation
Tests Priority #1: Human Body Systems Collection
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'backend'))

from generators.biology_models import BiologyModelGenerator
from generators.asset_generator_manager import AssetGeneratorManager

def test_individual_systems():
    """Test each body system individually"""
    print("="*70)
    print("🧬 TESTING INDIVIDUAL BODY SYSTEMS")
    print("="*70)
    
    generator = BiologyModelGenerator()
    
    # Test each system
    systems = [
        ('Digestive', generator.generate_digestive_system),
        ('Respiratory', generator.generate_respiratory_system),
        ('Circulatory', generator.generate_circulatory_system),
        ('Excretory', generator.generate_excretory_system),
        ('Skeletal', generator.generate_skeletal_system),
        ('Nervous', generator.generate_nervous_system),
        ('Muscular', generator.generate_muscular_system)
    ]
    
    results = []
    for name, func in systems:
        try:
            print(f"\n🔬 Testing {name} System...")
            metadata = func()
            results.append(metadata)
            print(f"   ✅ {metadata['filename']}")
            print(f"   📦 Size: {metadata['file_size_kb']} KB")
            print(f"   🔺 Vertices: {metadata['vertices']:,}")
            print(f"   📐 Faces: {metadata['faces']:,}")
            print(f"   🎓 Topics: {', '.join(metadata['exam_topics'])}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("\n" + "="*70)
    print(f"✅ Successfully generated {len(results)}/7 body systems")
    print("="*70)
    
    return results


def test_asset_manager_integration():
    """Test integration with AssetGeneratorManager"""
    print("\n\n" + "="*70)
    print("🔌 TESTING ASSET MANAGER INTEGRATION")
    print("="*70)
    
    manager = AssetGeneratorManager()
    
    # Check biology generator is registered
    if 'biology' in manager.generators:
        print("✅ Biology generator registered in AssetGeneratorManager")
    else:
        print("❌ Biology generator NOT registered")
        return False
    
    # Test lesson-based generation for biology topics
    test_lessons = [
        {
            'subject': 'Biology',
            'topic': 'digestive system',
            'grade_level': 'SS2'
        },
        {
            'subject': 'Biology',
            'topic': 'body systems and anatomy',
            'grade_level': 'SS1'
        }
    ]
    
    for lesson in test_lessons:
        print(f"\n📚 Testing lesson: {lesson['topic']}")
        try:
            assets = manager.generate_for_lesson(lesson)
            bio_models = assets.get('biology_models', [])
            print(f"   ✅ Generated {len(bio_models)} biology model(s)")
            for model in bio_models:
                print(f"      📄 {Path(model).name}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    return True


def test_comprehensive_generation():
    """Test full comprehensive generation including biology"""
    print("\n\n" + "="*70)
    print("🎨 TESTING COMPREHENSIVE GENERATION (ALL CATEGORIES)")
    print("="*70)
    
    manager = AssetGeneratorManager()
    
    try:
        results = manager.generate_all_priority_assets()
        
        print("\n📊 GENERATION SUMMARY:")
        print("="*70)
        
        # Math diagrams
        math_count = len(results.get('math_diagrams', {}))
        print(f"📐 Mathematical Diagrams: {math_count}")
        
        # 3D shapes
        shapes_count = len(results.get('geometric_shapes', []))
        print(f"🎲 3D Geometric Shapes: {shapes_count}")
        
        # Chemistry
        chem_results = results.get('chemistry_molecules', {})
        chem_count = sum(len(v) for v in chem_results.values())
        print(f"⚗️ Chemistry Molecules: {chem_count}")
        
        # Physics
        physics_count = len(results.get('physics_simulations', []))
        print(f"🔬 Physics Simulations: {physics_count}")
        
        # Biology (NEW!)
        biology_count = len(results.get('biology_models', []))
        print(f"🧬 Biology Body Systems: {biology_count}")
        
        total = math_count + shapes_count + chem_count + physics_count + biology_count
        
        print("="*70)
        print(f"✅ TOTAL ASSETS GENERATED: {total}")
        print("="*70)
        
        # Verify biology models
        if biology_count == 7:
            print("\n✅ All 7 body systems successfully generated!")
            print("\n🧬 Biology Models Generated:")
            for model in results['biology_models']:
                print(f"   • {model['system']}: {model['filename']} ({model['file_size_kb']} KB)")
        elif biology_count > 0:
            print(f"\n⚠️ Partial success: {biology_count}/7 body systems generated")
        else:
            print("\n❌ No biology models generated")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Comprehensive generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def verify_files():
    """Verify generated files exist"""
    print("\n\n" + "="*70)
    print("📁 VERIFYING GENERATED FILES")
    print("="*70)
    
    bio_dir = Path("generated_assets/biology_models")
    
    if not bio_dir.exists():
        print(f"❌ Directory not found: {bio_dir}")
        return False
    
    expected_files = [
        "digestive_system.glb",
        "respiratory_system.glb",
        "circulatory_system.glb",
        "excretory_system.glb",
        "skeletal_system.glb",
        "nervous_system.glb",
        "muscular_system.glb",
        "biology_models_manifest.json"
    ]
    
    found = 0
    total_size = 0
    
    for filename in expected_files:
        filepath = bio_dir / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            total_size += size_kb
            print(f"✅ {filename} ({size_kb:.2f} KB)")
            found += 1
        else:
            print(f"❌ {filename} - NOT FOUND")
    
    print("="*70)
    print(f"✅ Found {found}/{len(expected_files)} expected files")
    print(f"📦 Total size: {total_size:.2f} KB")
    print("="*70)
    
    return found == len(expected_files)


if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*10 + "BIOLOGY 3D MODEL GENERATION TEST SUITE" + " "*20 + "║")
    print("║" + " "*15 + "Priority #1: Human Body Systems" + " "*22 + "║")
    print("╚" + "="*68 + "╝\n")
    
    # Run tests
    test_results = {}
    
    # Test 1: Individual systems
    test_results['individual'] = test_individual_systems()
    
    # Test 2: Asset manager integration
    test_results['integration'] = test_asset_manager_integration()
    
    # Test 3: Comprehensive generation
    test_results['comprehensive'] = test_comprehensive_generation()
    
    # Test 4: File verification
    test_results['verification'] = verify_files()
    
    # Final summary
    print("\n\n" + "╔" + "="*68 + "╗")
    print("║" + " "*24 + "FINAL SUMMARY" + " "*31 + "║")
    print("╚" + "="*68 + "╝")
    
    print(f"\n✅ Individual System Tests: {len(test_results['individual'])}/7 passed")
    print(f"✅ Integration Tests: {'PASSED' if test_results['integration'] else 'FAILED'}")
    print(f"✅ Comprehensive Generation: {'PASSED' if test_results['comprehensive'] else 'FAILED'}")
    print(f"✅ File Verification: {'PASSED' if test_results['verification'] else 'FAILED'}")
    
    if all([
        len(test_results['individual']) == 7,
        test_results['integration'],
        test_results['comprehensive'],
        test_results['verification']
    ]):
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED! Biology 3D models fully functional!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("⚠️ Some tests failed. Review output above for details.")
        print("="*70)
