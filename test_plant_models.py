"""
Comprehensive test for plant model generation
Tests Priority #2: Plant Anatomy and Photosynthesis
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src' / 'backend'))

from generators.plant_models import PlantModelGenerator
from generators.asset_generator_manager import AssetGeneratorManager

def test_individual_plants():
    """Test each plant model individually"""
    print("="*70)
    print("🌱 TESTING INDIVIDUAL PLANT MODELS")
    print("="*70)
    
    generator = PlantModelGenerator()
    
    models = [
        ('Plant Cell', generator.generate_plant_cell),
        ('Leaf Structure', generator.generate_leaf_structure),
        ('Root System', generator.generate_root_system),
        ('Flower Structure', generator.generate_flower_structure),
        ('Photosynthesis', generator.generate_photosynthesis_process)
    ]
    
    results = []
    for name, func in models:
        try:
            print(f"\n🔬 Testing {name}...")
            metadata = func()
            results.append(metadata)
            print(f"   ✅ {metadata['filename']}")
            print(f"   📦 Size: {metadata['file_size_kb']} KB")
            print(f"    🔺 Vertices: {metadata['vertices']:,}")
            print(f"   📐 Faces: {metadata['faces']:,}")
            print(f"   🎓 Topics: {', '.join(metadata['exam_topics'])}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("\n" + "="*70)
    print(f"✅ Successfully generated {len(results)}/5 plant models")
    print("="*70)
    
    return results


def test_comprehensive_generation():
    """Test comprehensive generation with plants"""
    print("\n\n" + "="*70)
    print("🎨 TESTING COMPREHENSIVE GENERATION (ALL CATEGORIES)")
    print("="*70)
    
    import matplotlib
    matplotlib.use('Agg')  # Headless backend
    
    manager = AssetGeneratorManager()
    
    try:
        results = manager.generate_all_priority_assets()
        
        print("\n📊 UPDATED GENERATION SUMMARY:")
        print("="*70)
        
        math_count = len(results.get('math_diagrams', {}))
        shapes_count = len(results.get('geometric_shapes', []))
        chem_results = results.get('chemistry_molecules', {})
        chem_count = sum(len(v) for v in chem_results.values())
        physics_count = len(results.get('physics_simulations', []))
        biology_count = len(results.get('biology_models', []))
        plant_count = len(results.get('plant_models', []))
        
        print(f"📐 Mathematical Diagrams: {math_count}")
        print(f"🎲 3D Geometric Shapes: {shapes_count}")
        print(f"⚗️ Chemistry Molecules: {chem_count}")
        print(f"🔬 Physics Simulations: {physics_count}")
        print(f"🧬 Biology Body Systems: {biology_count}")
        print(f"🌱 Plant Models: {plant_count} ⭐ NEW!")
        
        total = math_count + shapes_count + chem_count + physics_count + biology_count + plant_count
        
        print("="*70)
        print(f"✅ TOTAL ASSETS GENERATED: {total}")
        print("="*70)
        
        # Verify plant models
        if plant_count == 5:
            print("\n✅ All 5 plant models successfully generated!")
            print("\n🌱 Plant Models Generated:")
            for model in results['plant_models']:
                print(f"   • {model['model']}: {model['filename']} ({model['file_size_kb']} KB)")
        elif plant_count > 0:
            print(f"\n⚠️ Partial success: {plant_count}/5 plant models generated")
        else:
            print("\n❌ No plant models generated")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Comprehensive generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_lesson_generation():
    """Test lesson-based generation for plant topics"""
    print("\n\n" + "="*70)
    print("📚 TESTING LESSON-BASED PLANT GENERATION")
    print("="*70)
    
    manager = AssetGeneratorManager()
    
    lessons = [
        {'subject': 'Biology', 'topic': 'plant cell', 'grade_level': 'JSS3'},
        {'subject': 'Biology', 'topic': 'leaf structure and photosynthesis', 'grade_level': 'SS1'},
        {'subject': 'Biology', 'topic': 'root systems', 'grade_level': 'JSS3'},
        {'subject': 'Biology', 'topic': 'plant anatomy', 'grade_level': 'SS1'}
    ]
    
    for lesson in lessons:
        print(f"\n📚 Testing: {lesson['topic']}")
        try:
            assets = manager.generate_for_lesson(lesson)
            plant_models = assets.get('plant_models', [])
            if plant_models:
                print(f"   ✅ Generated {len(plant_models)} plant model(s)")
                for model in plant_models:
                    print(f"      📄 {Path(model).name}")
            else:
                print(f"   ⓘ No plant models (may use different keywords)")
        except Exception as e:
            print(f"   ❌ Failed: {e}")


def verify_files():
    """Verify generated plant model files"""
    print("\n\n" + "="*70)
    print("📁 VERIFYING GENERATED PLANT FILES")
    print("="*70)
    
    plant_dir = Path("generated_assets/plant_models")
    
    if not plant_dir.exists():
        print(f"❌ Directory not found: {plant_dir}")
        return False
    
    expected_files = [
        "plant_cell.glb",
        "leaf_structure.glb",
        "root_system.glb",
        "flower_structure.glb",
        "photosynthesis_process.glb",
        "plant_models_manifest.json"
    ]
    
    found = 0
    total_size = 0
    
    for filename in expected_files:
        filepath = plant_dir / filename
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
    print("║" + " "*12 + "PLANT MODEL GENERATION TEST SUITE" + " "*23 + "║")
    print("║" + " "*14 + "Priority #2: Plant Anatomy" + " "*28 + "║")
    print("╚" + "="*68 + "╝\n")
    
    test_results = {}
    
    # Test 1: Individual plants
    test_results['individual'] = test_individual_plants()
    
    # Test 2: Comprehensive generation
    test_results['comprehensive'] = test_comprehensive_generation()
    
    # Test 3: Lesson generation
    test_lesson_generation()
    
    # Test 4: File verification
    test_results['verification'] = verify_files()
    
    # Final summary
    print("\n\n" + "╔" + "="*68 + "╗")
    print("║" + " "*24 + "FINAL SUMMARY" + " "*31 + "║")
    print("╚" + "="*68 + "╝")
    
    print(f"\n✅ Individual Plant Tests: {len(test_results['individual'])}/5 passed")
    print(f"✅ Comprehensive Generation: {'PASSED' if test_results['comprehensive'] else 'FAILED'}")
    print(f"✅ File Verification: {'PASSED' if test_results['verification'] else 'FAILED'}")
    
    if all([
        len(test_results['individual']) == 5,
        test_results['comprehensive'],
        test_results['verification']
    ]):
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED! Plant models fully functional!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("⚠️ Some tests failed. Review output above for details.")
        print("="*70)
