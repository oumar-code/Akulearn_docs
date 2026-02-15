#!/usr/bin/env python3
import json

# Load curriculum map
with open('curriculum_map.json', encoding='utf-8') as f:
    map_data = json.load(f)

# Load database
with open('wave3_content_database.json', encoding='utf-8') as f:
    db_data = json.load(f)

db_items = db_data.get('content', [])
map_subjects = map_data.get('subjects', {})

print("\n=== WAEC CURRICULUM COVERAGE ANALYSIS ===\n")
print(f"Database total items: {len(db_items)}\n")

# Group DB items by subject
db_by_subject = {}
for item in db_items:
    subj = item.get('subject', 'Unknown')
    if subj not in db_by_subject:
        db_by_subject[subj] = []
    db_by_subject[subj].append(item)

# Compare
total_topics = 0
total_covered = 0
gaps = {}

for subj, map_data_subj in map_subjects.items():
    topics = map_data_subj.get('topics', [])
    total_topics += len(topics)
    db_items_subj = db_by_subject.get(subj, [])
    
    covered = len(db_items_subj)
    total_covered += covered
    
    coverage_pct = round(100 * covered / max(1, len(topics)), 1)
    print(f"{subj}:")
    print(f"  Curriculum topics: {len(topics)}")
    print(f"  Generated items: {covered}")
    print(f"  Coverage: {coverage_pct}%")
    
    if covered < len(topics):
        gaps[subj] = len(topics) - covered
        topic_names = [t.get('name') for t in topics]
        print(f"  Missing: {gaps[subj]} topics")
        print(f"    {topic_names}\n")
    else:
        print()

overall = round(100 * total_covered / max(1, total_topics), 1)
print(f"OVERALL: {total_covered}/{total_topics} topics → {overall}% coverage\n")

if gaps:
    print(f"Total missing topics to reach 100%: {sum(gaps.values())}")
    for subj, count in sorted(gaps.items(), key=lambda x: -x[1]):
        print(f"  - {subj}: {count} missing")
else:
    print("✅ 100% WAEC coverage achieved!")
