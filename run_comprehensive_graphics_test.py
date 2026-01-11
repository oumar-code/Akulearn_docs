#!/usr/bin/env python
"""Comprehensive test of graphics generation system"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

print("="*70)
print("🎨 COMPREHENSIVE GRAPHICS GENERATION TEST")
print("="*70)

# Test Asset Manager
print("\n📊 Testing Asset Manager Full Generation...")
print("-"*70)

try:
    from src.backend.generators.asset_generator_manager import AssetGeneratorManager
    
    manager = AssetGeneratorManager()
    
    # Generate all priority assets
    results = manager.generate_all_priority_assets()
    
    # Summary
    print("\n✅ GENERATION SUMMARY:")
    print(f"   📊 Math Diagrams: {len(results['math_diagrams'])} generated")
    print(f"   🎲 3D Shapes: {len(results['geometric_shapes'])} generated")
    print(f"   ⚗️ Chemistry Molecules: {sum(len(v) for v in results['chemistry_molecules'].values())} generated")
    print(f"   🔬 Physics Simulations: {len(results['physics_simulations'])} generated")
    
    # Show manifest
    print(f"\n📄 Manifest Location: {manager.manifest_path}")
    print(f"   Total Assets: {manager.manifest['total_assets']}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test Lesson-specific Generation
print("\n\n📖 Testing Lesson-Specific Generation...")
print("-"*70)

try:
    # Mathematics lesson
    lesson = {
        "subject": "Mathematics",
        "topic": "Trigonometry",
        "grade_level": "SS2"
    }
    
    assets = manager.generate_for_lesson(lesson)
    print(f"✅ {lesson['subject']} - {lesson['topic']} ({lesson['grade_level']})")
    for category, files in assets.items():
        if files:
            print(f"   {category}: {len(files)} files")
    
    # Physics lesson
    lesson = {
        "subject": "Physics",
        "topic": "Simple Harmonic Motion",
        "grade_level": "SS3"
    }
    
    assets = manager.generate_for_lesson(lesson)
    print(f"\n✅ {lesson['subject']} - {lesson['topic']} ({lesson['grade_level']})")
    for category, files in assets.items():
        if files:
            print(f"   {category}: {len(files)} files")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test Subject Pack Generation
print("\n\n📚 Testing Subject Pack Generation...")
print("-"*70)

try:
    pack = manager.generate_subject_pack("Mathematics", "SS2")
    print(f"✅ Math Pack for SS2")
    print(f"   Categories: {len(pack['assets'])}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

# List Generated Files
print("\n\n📁 GENERATED FILES OVERVIEW:")
print("-"*70)

try:
    generated_dir = Path("generated_assets")
    
    for category_dir in generated_dir.iterdir():
        if category_dir.is_dir():
            files = list(category_dir.glob("*"))
            print(f"\n📂 {category_dir.name}/ ({len(files)} items)")
            for file in sorted(files)[:5]:  # Show first 5
                size_kb = file.stat().st_size / 1024 if file.is_file() else 0
                size_str = f"{size_kb:.1f}KB" if size_kb > 0 else "DIR"
                print(f"   ├─ {file.name:<40} ({size_str})")
            if len(files) > 5:
                print(f"   └─ ... and {len(files)-5} more")
    
except Exception as e:
    print(f"❌ Error listing files: {e}")

# Statistics
print("\n\n📊 STATISTICS:")
print("-"*70)

try:
    stats = manager.get_statistics()
    print(f"Total Generators: {stats['total_generators']}")
    print(f"Registered: {', '.join(stats['generators'])}")
    print(f"Total Assets Generated: {stats['manifest']['total_assets']}")
    
except Exception as e:
    print(f"❌ Error getting stats: {e}")

print("\n" + "="*70)
print("✅ COMPREHENSIVE TEST COMPLETED")
print("="*70)
