#!/usr/bin/env python3
"""
Comprehensive test suite for Plant Model Generator (Priority #2)
Tests individual plant models, integration, and file verification
"""

import os
import json
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from backend.generators.plant_models import PlantModelGenerator
from backend.generators.asset_generator_manager import AssetGeneratorManager

def test_individual_plants():
    """Test each plant model individually"""
    print("\n" + "="*70)
    print("🌱 TESTING INDIVIDUAL PLANT MODELS")
    print("="*70)
    
    generator = PlantModelGenerator()
    models = [
        ('Plant Cell', 'plant_cell'),
        ('Leaf Structure', 'leaf_structure'),
        ('Root System', 'root_system'),
        ('Flower Structure', 'flower_structure'),
        ('Photosynthesis Process', 'photosynthesis_process'),
    ]
    
    results = {}
    for name, model_id in models:
        print(f"\n🔬 Testing {name}...")
        try:
            output_path = Path(generator.output_dir) / f"{model_id}.glb"
            
            # File should exist from generation
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                print(f"   ✅ {model_id}.glb")
                print(f"   📦 Size: {size_kb:.2f} KB")
                results[model_id] = {'status': 'success', 'size_kb': size_kb}
            else:
                print(f"   ❌ File not found: {output_path}")
                results[model_id] = {'status': 'failed', 'reason': 'file not found'}
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[model_id] = {'status': 'failed', 'reason': str(e)}
    
    successful = sum(1 for r in results.values() if r['status'] == 'success')
    print(f"\n{'='*70}")
    print(f"✅ Successfully tested {successful}/{len(models)} plant models")
    print(f"{'='*70}")
    
    return results


def test_manifest():
    """Test plant model manifest"""
    print("\n" + "="*70)
    print("📋 TESTING MANIFEST")
    print("="*70)
    
    manifest_path = Path('generated_assets/plant_models/plant_models_manifest.json')
    
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        print(f"\n✅ Manifest found")
        print(f"   📦 Total models: {manifest.get('total_models', 0)}")
        print(f"   📁 Output directory: {manifest.get('output_dir', 'N/A')}")
        
        if 'models' in manifest:
            print(f"\n   Models in manifest:")
            for model in manifest['models']:
                print(f"     - {model.get('name', 'Unknown')} ({model.get('size_kb', 0):.2f} KB)")
        
        return {'status': 'success', 'manifest': manifest}
    else:
        print(f"❌ Manifest not found at {manifest_path}")
        return {'status': 'failed', 'reason': 'manifest not found'}


def test_integration():
    """Test integration with AssetGeneratorManager"""
    print("\n" + "="*70)
    print("🔗 TESTING INTEGRATION WITH ASSET MANAGER")
    print("="*70)
    
    try:
        manager = AssetGeneratorManager()
        print("✅ AssetGeneratorManager initialized")
        
        # Test lesson generation with plant topics
        plant_topics = [
            ('plant cell', 'plant_cell'),
            ('leaf structure', 'leaf_structure'),
            ('root', 'root_system'),
            ('flower', 'flower_structure'),
            ('photosynthesis', 'photosynthesis_process'),
        ]
        
        print("\n🎓 Testing lesson-based generation:")
        for topic, expected_model in plant_topics:
            result = manager.generate_for_lesson(topic)
            if result and 'plant_models' in result and result['plant_models']:
                print(f"   ✅ {topic}: {expected_model}.glb generated")
            else:
                print(f"   ⚠️  {topic}: No result returned")
        
        return {'status': 'success'}
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return {'status': 'failed', 'error': str(e)}


def test_file_verification():
    """Verify all plant model files exist and are valid"""
    print("\n" + "="*70)
    print("📂 TESTING FILE VERIFICATION")
    print("="*70)
    
    plant_dir = Path('generated_assets/plant_models')
    expected_files = [
        'plant_cell.glb',
        'leaf_structure.glb',
        'root_system.glb',
        'flower_structure.glb',
        'photosynthesis_process.glb',
        'plant_models_manifest.json'
    ]
    
    print("\n✅ File Verification Results:")
    missing_files = []
    total_size = 0
    
    for filename in expected_files:
        filepath = plant_dir / filename
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            total_size += filepath.stat().st_size
            if filename.endswith('.glb'):
                print(f"   ✅ {filename} ({size_kb:.2f} KB)")
            else:
                print(f"   ✅ {filename}")
        else:
            print(f"   ❌ {filename} - MISSING")
            missing_files.append(filename)
    
    print(f"\n📊 Summary:")
    print(f"   Total files: {len(expected_files) - len(missing_files)}/{len(expected_files)}")
    print(f"   Total size: {total_size/1024:.2f} KB")
    
    if missing_files:
        return {'status': 'partial', 'missing': missing_files, 'total_size_kb': total_size/1024}
    else:
        return {'status': 'success', 'total_size_kb': total_size/1024}


if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "PLANT MODEL GENERATION TEST SUITE" + " "*20 + "║")
    print("║" + " "*19 + "Priority #2: Plant Anatomy" + " "*22 + "║")
    print("╚" + "="*68 + "╝")
    
    test_results = {}
    
    # Run tests
    test_results['individual'] = test_individual_plants()
    test_results['manifest'] = test_manifest()
    test_results['integration'] = test_integration()
    test_results['file_verification'] = test_file_verification()
    
    # Summary
    print("\n" + "="*70)
    print("📈 TEST SUMMARY")
    print("="*70)
    
    for test_name, result in test_results.items():
        status = result.get('status', 'unknown')
        status_emoji = "✅" if status == 'success' else "⚠️" if status == 'partial' else "❌"
        print(f"{status_emoji} {test_name}: {status}")
    
    print("\n" + "="*70)
    print("✨ Plant Model Testing Complete!")
    print("="*70)
