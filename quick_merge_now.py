import json
from datetime import datetime

# Load databases
with open("wave3_content_database.json", 'r', encoding='utf-8') as f:
    main_db = json.load(f)

with open("generated_content/wave3_content_database.json", 'r', encoding='utf-8') as f:
    batch4_db = json.load(f)

# Get batch 4 lessons
batch4_lessons = batch4_db.get("lessons", batch4_db.get("content", []))

print(f"Main DB: {len(main_db['content'])} lessons")
print(f"Batch 4: {len(batch4_lessons)} lessons")

# Add batch 4 to main
for lesson in batch4_lessons:
    main_db["content"].append(lesson)

# Update metadata
main_db["metadata"]["total_items"] = len(main_db["content"])
main_db["metadata"]["last_updated"] = datetime.now().isoformat()

# Recount subjects
subjects = {}
for lesson in main_db["content"]:
    subj = lesson.get("subject", "Unknown")
    subjects[subj] = subjects.get(subj, 0) + 1
main_db["metadata"]["statistics"]["by_subject"] = subjects

# Save
with open("wave3_content_database.json", 'w', encoding='utf-8') as f:
    json.dump(main_db, f, indent=2, ensure_ascii=False)

print(f"\n✅ MERGED! Total: {len(main_db['content'])} lessons")
print(f"Subjects: {subjects}")
