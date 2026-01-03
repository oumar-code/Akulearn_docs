#!/usr/bin/env python3
"""Merge batch2 existing 2 lessons with new 3 lessons"""
import json

# Load existing 2 lessons
with open('generated_content/batch2_content.json', encoding='utf-8') as f:
    batch2_original = json.load(f)

# Load new 3 lessons
with open('generated_content/batch2_extension.json', encoding='utf-8') as f:
    batch2_extension = json.load(f)

# Merge
batch2_original['content'].extend(batch2_extension['content'])

# Update metadata
batch2_original['metadata']['total_items'] = len(batch2_original['content'])
# Calculate read time (old lessons use 'estimated_read_time', new use 'read_time_minutes')
total_time = 0
for lesson in batch2_original['content']:
    if 'read_time_minutes' in lesson:
        total_time += lesson['read_time_minutes']
    elif 'estimated_read_time' in lesson:
        total_time += lesson['estimated_read_time']
batch2_original['metadata']['total_read_time_minutes'] = total_time

# Save complete batch
with open('batch2_content_complete.json', 'w') as f:
    json.dump(batch2_original, f, indent=2)

print(f"✅ Merged successfully!")
print(f"   Total lessons: {batch2_original['metadata']['total_items']}")
print(f"   Total read time: {batch2_original['metadata']['total_read_time_minutes']} minutes")
print(f"   Subjects:")
for lesson in batch2_original['content']:
    read_time = lesson.get('read_time_minutes', lesson.get('estimated_read_time', 'N/A'))
    print(f"      - {lesson['subject']}: {lesson['title']} ({read_time} min)")
