#!/usr/bin/env python3
"""Simple batch generation test"""

import os
import json
from pathlib import Path

# Check what batch files exist
batch_dir = Path("generated_content")
print("📂 Batch files in generated_content:")
for f in batch_dir.glob("batch*.json"):
    size_kb = f.stat().st_size / 1024
    print(f"  ✅ {f.name} ({size_kb:.1f} KB)")

# Check expansion report
exp_report = batch_dir / "expansion_report.json"
if exp_report.exists():
    with open(exp_report, 'r') as f:
        data = json.load(f)
    
    print(f"\n📊 Expansion Report Summary:")
    print(f"  Coverage: {data['current_state']['overall_coverage']}")
    print(f"  Total lessons: {data['current_state']['total_lessons']}")
    print(f"  Phase 1 topics: {len(data['phases'][0]['topics']) if 'phases' in data else 'N/A'}")

# Try to run test batch generation directly
print(f"\n🚀 Testing batch generation...")

try:
    from enhanced_content_generator import EnhancedContentGenerator
    
    gen = EnhancedContentGenerator(use_mcp=False)
    
    # Generate test batch with just 1 topic
    test_topics = [("Mathematics", "Quadratic Equations and Functions", "Intermediate")]
    
    lessons = gen.generate_batch(topics=test_topics)
    print(f"✅ Generated {len(lessons)} test lessons")
    
    if lessons:
        lesson = lessons[0]
        print(f"\n📚 Sample Generated Lesson:")
        print(f"  ID: {lesson.get('id')}")
        print(f"  Title: {lesson.get('title')}")
        print(f"  Subject: {lesson.get('subject')}")
        print(f"  Objectives: {len(lesson.get('learningObjectives', []))}")
        print(f"  Sections: {len(lesson.get('sections', []))}")
        
        # Save test output
        gen.save_to_file(lessons, "test_batch_output.json")
        print(f"✅ Saved to test_batch_output.json")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
