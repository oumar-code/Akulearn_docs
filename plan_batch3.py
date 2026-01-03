#!/usr/bin/env python3
"""Plan Batch 3: Identify next 5 high-priority topics"""
import json

# Load curriculum map
with open('curriculum_map.json', encoding='utf-8') as f:
    curriculum = json.load(f)

# Load current database to see what's covered
with open('wave3_content_database.json', encoding='utf-8') as f:
    database = json.load(f)

# Extract all topics by priority
all_topics = []
for subject_name, subject_data in curriculum['subjects'].items():
    for topic in subject_data['topics']:
        all_topics.append({
            'subject': subject_name,
            'topic_id': topic['id'],
            'topic_name': topic['name'],
            'exam_weight': topic.get('exam_weight', ''),
            'difficulty': topic.get('difficulty', ''),
            'subtopics': topic.get('subtopics', []),
            'prerequisites': topic.get('prerequisites', [])
        })

# Get covered topics
covered_topics = set()
for item in database['content']:
    # Match by topic name
    covered_topics.add(item.get('topic', '').lower())

print("=" * 80)
print("BATCH 3 PLANNING: NEXT 5 HIGH-PRIORITY TOPICS")
print("=" * 80)

print("\n📚 Currently Covered Topics (37 items):")
for i, topic in enumerate(sorted(covered_topics), 1):
    print(f"   {i}. {topic.title()}")

# Filter high-priority topics not yet covered
high_priority = [t for t in all_topics if t['exam_weight'] == 'high']
uncovered_high = [t for t in high_priority if t['topic_name'].lower() not in covered_topics]

print(f"\n🎯 High-Priority Topics Available: {len(uncovered_high)}")
print("\nTop 10 High-Priority Uncovered Topics:")
for i, topic in enumerate(uncovered_high[:10], 1):
    print(f"\n{i}. {topic['subject']}: {topic['topic_name']}")
    print(f"   - Difficulty: {topic['difficulty']}")
    print(f"   - Exam Weight: {topic['exam_weight']}")
    print(f"   - Subtopics: {', '.join(topic['subtopics'][:3])}{'...' if len(topic['subtopics']) > 3 else ''}")

print("\n" + "=" * 80)
print("BATCH 3 RECOMMENDED SELECTION (5 Topics)")
print("=" * 80)

# Select diverse batch 3 topics
batch3_candidates = uncovered_high[:10]

# Try to get diverse subjects
selected = []
subjects_used = set()

# First pass: One from each subject
for topic in batch3_candidates:
    if topic['subject'] not in subjects_used and len(selected) < 5:
        selected.append(topic)
        subjects_used.add(topic['subject'])

# Second pass: Fill remaining slots
for topic in batch3_candidates:
    if topic not in selected and len(selected) < 5:
        selected.append(topic)

print("\n🎓 BATCH 3 FINAL SELECTION:\n")
total_subtopics = 0
for i, topic in enumerate(selected, 1):
    print(f"{i}. {topic['subject']}: {topic['topic_name']}")
    print(f"   - Difficulty: {topic['difficulty']}")
    print(f"   - Exam Weight: {topic['exam_weight']}")
    print(f"   - Subtopics ({len(topic['subtopics'])}): {', '.join(topic['subtopics'])}")
    print(f"   - Prerequisites: {', '.join(topic['prerequisites'])}")
    total_subtopics += len(topic['subtopics'])
    print()

print("=" * 80)
print("BATCH 3 STATISTICS")
print("=" * 80)
print(f"\n📊 Content Scope:")
print(f"   - Lessons: 5")
print(f"   - Total Subtopics: {total_subtopics}")
print(f"   - Estimated Read Time: 125-150 minutes (25-30 min each)")
print(f"   - Difficulty Distribution:")
difficulty_dist = {}
for t in selected:
    difficulty_dist[t['difficulty']] = difficulty_dist.get(t['difficulty'], 0) + 1
for diff, count in sorted(difficulty_dist.items()):
    print(f"     * {diff.title()}: {count} lessons")

print(f"\n📈 Progress Impact:")
print(f"   - Current Coverage: 11/44 topics (25%)")
print(f"   - After Batch 3: 16/44 topics (36%)")
print(f"   - Database Items: 37 → 42 items")

print(f"\n🎯 Subject Balance After Batch 3:")
subject_counts = {'Mathematics': 8, 'Physics': 9, 'Chemistry': 4, 'Biology': 4, 'English': 2, 'Economics': 1, 'Geography': 1}
for topic in selected:
    subject_counts[topic['subject']] = subject_counts.get(topic['subject'], 0) + 1
for subject, count in sorted(subject_counts.items(), key=lambda x: -x[1]):
    print(f"   - {subject}: {count} items")

print("\n💡 Next Steps:")
print("   1. Review Batch 3 selection above")
print("   2. Generate Nigerian context for each topic using nigerian_context_research.json")
print("   3. Create batch3_content_generator.py similar to batch2_extension_generator.py")
print("   4. Generate all 5 lessons (estimated 30-40 minutes)")
print("   5. Deploy to Wave 3 database")
print("   6. Commit to Git")
