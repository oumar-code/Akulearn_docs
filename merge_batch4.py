#!/usr/bin/env python3
"""
Merge Batch 4 into main database
"""

import json
from datetime import datetime

print("\n" + "="*60)
print("📦 MERGING BATCH 4 INTO MAIN DATABASE")
print("="*60 + "\n")

# Load main database
print("📂 Loading main database...")
with open("wave3_content_database.json", 'r', encoding='utf-8') as f:
    main_db = json.load(f)

print(f"   Current lessons: {main_db['metadata']['total_items']}")

# Load Batch 4
print("\n📂 Loading Batch 4...")
with open("generated_content/wave3_content_database.json", 'r', encoding='utf-8') as f:
    batch4_db = json.load(f)

batch4_lessons = batch4_db.get("lessons", [])
print(f"   Batch 4 lessons: {len(batch4_lessons)}")

# Show Batch 4 content
print("\n📚 Batch 4 Lessons:")
for lesson in batch4_lessons:
    print(f"   • {lesson.get('subject')} - {lesson.get('title')}")

# Merge
print(f"\n🔄 Merging...")
main_db["lessons"].extend(batch4_lessons)

# Update metadata
main_db["metadata"]["total_items"] = len(main_db["lessons"])
main_db["metadata"]["last_updated"] = datetime.now().isoformat()
main_db["metadata"]["batch4_added"] = datetime.now().isoformat()

# Count by subject
from collections import Counter
subjects = Counter(lesson.get("subject") for lesson in main_db["lessons"])
main_db["metadata"]["statistics"]["by_subject"] = dict(subjects)

print(f"   New total: {main_db['metadata']['total_items']} lessons")

# Save
print(f"\n💾 Saving merged database...")
with open("wave3_content_database.json", 'w', encoding='utf-8') as f:
    json.dump(main_db, f, indent=2, ensure_ascii=False)

print("✅ Merge complete!")

print("\n📊 Final Statistics:")
print(f"   Total lessons: {main_db['metadata']['total_items']}")
print(f"   By subject:")
for subject, count in sorted(main_db["metadata"]["statistics"]["by_subject"].items()):
    print(f"      {subject}: {count}")

print("\n" + "="*60)
print("✅ DATABASE UPDATED SUCCESSFULLY")
print("="*60 + "\n")
