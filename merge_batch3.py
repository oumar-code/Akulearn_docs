#!/usr/bin/env python3
"""
Merge Batch 3 content: 5 lessons into single batch3_content_complete.json
"""

import json
from pathlib import Path

def merge_batch3():
    """Merge all batch 3 lessons into complete file"""
    print("\n" + "=" * 70)
    print("MERGING BATCH 3 CONTENT")
    print("=" * 70)
    
    # Load batch3_content.json (5 generated lessons)
    with open("generated_content/batch3_content.json", "r", encoding='utf-8') as f:
        batch3_data = json.load(f)
    
    lessons = batch3_data["content"]
    total_time = batch3_data["metadata"]["total_read_time_minutes"]
    
    print(f"\n✅ Loaded {len(lessons)} lessons from generated_content/batch3_content.json")
    
    # Create complete file
    complete_data = {
        "metadata": {
            "version": "3.0",
            "batch": "3",
            "total_items": len(lessons),
            "generator": "Batch3ContentMerger",
            "total_read_time_minutes": total_time,
            "exam_board": "WAEC"
        },
        "lessons": lessons
    }
    
    # Save
    output_path = Path("batch3_content_complete.json")
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(complete_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Merged successfully!")
    print(f"   Total lessons: {len(lessons)}")
    print(f"   Total read time: {total_time} minutes")
    print(f"   Subjects:")
    subjects = {}
    for lesson in lessons:
        subject = lesson["subject"]
        subjects[subject] = subjects.get(subject, 0) + 1
    for subject, count in sorted(subjects.items()):
        print(f"      - {subject}: {count}")
    print(f"\n💾 Saved to: {output_path}")
    print("\nNext: Deploy to Wave 3 database")

if __name__ == "__main__":
    merge_batch3()
