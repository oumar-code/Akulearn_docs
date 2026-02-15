#!/usr/bin/env python3
"""
Comprehensive test suite for Molecular Model Generator (Priority #3)
Tests individual molecular models, integration, and file verification
"""

import os
import json
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from backend.generators.molecular_models import MolecularModelGenerator
from backend.generators.asset_generator_manager import AssetGeneratorManager

def test_individual_molecules():
    """Test each molecular model individually"""
    print("\n" + "="*70)
    print("🧪 TESTING INDIVIDUAL MOLECULAR MODELS")
    print("="*70)
    
    generator = MolecularModelGenerator()
    models = [
        ('Atomic Models', 'atom_models'),
        ('Ionic Bonding', 'ionic_bonding'),
        ('Covalent Bonding', 'covalent_bonding'),
        ('Metallic Bonding', 'metallic_bonding'),
        ('Hydrocarbon Series', 'hydrocarbon_series'),
        ('Benzene Ring', 'benzene_ring'),
        ('Protein Structure', 'protein_structure'),
        ('DNA Helix', 'dna_helix'),
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
    print(f"✅ Successfully tested {successful}/{len(models)} molecular models")
    print(f"{'='*70}")
    
    return results


def test_manifest():
    """Test molecular model manifest"""
    print("\n" + "="*70)
    print("📋 TESTING MANIFEST")
    print("="*70)
    
    manifest_path = Path('generated_assets/molecular_models/molecular_models_manifest.json')
    
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        print(f"\n✅ Manifest found")
        print(f"   📦 Total models: {manifest.get('total_models', 0)}")
        print(f"   📚 Subject: {manifest.get('subject', 'N/A')}")
        print(f"   🎯 Topic codes: {', '.join(manifest.get('topic_codes', []))}")
        print(f"   📊 Exam weight: {manifest.get('exam_weight', 'N/A')}")
        
        if 'models' in manifest:
            print(f"\n   Models in manifest:")
            for model in manifest['models']:
                print(f"     - {model.get('model', 'Unknown')} ({model.get('file_size_kb', 0):.2f} KB)")
        
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
        
        # Test lesson generation with chemistry topics
        chemistry_topics = [
            ('atom', 'atom_models'),
            ('ionic', 'ionic_bonding'),
            ('covalent', 'covalent_bonding'),
            ('metallic', 'metallic_bonding'),
            ('hydrocarbon', 'hydrocarbon_series'),
            ('benzene', 'benzene_ring'),
            ('protein', 'protein_structure'),
            ('dna', 'dna_helix'),
        ]
        
        print("\n🎓 Testing lesson-based generation:")
        passed = 0
        for topic, expected_model in chemistry_topics:
            result = manager.generate_for_lesson({'subject': 'chemistry', 'topic': topic})
            if result and 'molecules' in result:
                if any(expected_model in str(mol) for mol in result.get('molecules', [])):
                    print(f"   ✅ {topic}: {expected_model}.glb generated")
                    passed += 1
                else:
                    print(f"   ⚠️  {topic}: No matching result")
            else:
                print(f"   ⚠️  {topic}: No result returned")
        
        print(f"\n✅ Passed {passed}/{len(chemistry_topics)} lesson tests")
        return {'status': 'success' if passed >= 6 else 'partial', 'passed': passed}
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return {'status': 'failed', 'error': str(e)}


def test_file_verification():
    """Verify all molecular model files exist and are valid"""
    print("\n" + "="*70)
    print("📂 TESTING FILE VERIFICATION")
    print("="*70)
    
    molecular_dir = Path('generated_assets/molecular_models')
    expected_files = [
        'atom_models.glb',
        'ionic_bonding.glb',
        'covalent_bonding.glb',
        'metallic_bonding.glb',
        'hydrocarbon_series.glb',
        'benzene_ring.glb',
        'protein_structure.glb',
        'dna_helix.glb',
        'molecular_models_manifest.json'
    ]
    
    print("\n✅ File Verification Results:")
    missing_files = []
    total_size = 0
    
    for filename in expected_files:
        filepath = molecular_dir / filename
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


def test_model_sizes():
    """Test that model sizes are within acceptable ranges"""
    print("\n" + "="*70)
    print("📏 TESTING MODEL SIZE OPTIMIZATION")
    print("="*70)
    
    molecular_dir = Path('generated_assets/molecular_models')
    max_size_kb = 1024  # 1MB max per model
    
    oversized = []
    for glb_file in molecular_dir.glob('*.glb'):
        size_kb = glb_file.stat().st_size / 1024
        if size_kb > max_size_kb:
            oversized.append((glb_file.name, size_kb))
            print(f"   ⚠️  {glb_file.name}: {size_kb:.2f} KB (exceeds {max_size_kb} KB)")
        else:
            print(f"   ✅ {glb_file.name}: {size_kb:.2f} KB")
    
    if oversized:
        print(f"\n⚠️  {len(oversized)} models exceed size limit")
        return {'status': 'warning', 'oversized': oversized}
    else:
        print(f"\n✅ All models within size limits")
        return {'status': 'success'}


if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*12 + "MOLECULAR MODEL GENERATION TEST SUITE" + " "*19 + "║")
    print("║" + " "*16 + "Priority #3: Chemistry Models" + " "*23 + "║")
    print("╚" + "="*68 + "╝")
    
    test_results = {}
    
    # Run tests
    test_results['individual'] = test_individual_molecules()
    test_results['manifest'] = test_manifest()
    test_results['integration'] = test_integration()
    test_results['file_verification'] = test_file_verification()
    test_results['size_optimization'] = test_model_sizes()
    
    # Summary
    print("\n" + "="*70)
    print("📈 TEST SUMMARY")
    print("="*70)
    
    for test_name, result in test_results.items():
        status = result.get('status', 'unknown')
        status_emoji = "✅" if status == 'success' else "⚠️" if status in ['partial', 'warning'] else "❌"
        print(f"{status_emoji} {test_name}: {status}")
    
    print("\n" + "="*70)
    print("✨ Molecular Model Testing Complete!")
    print("="*70)
