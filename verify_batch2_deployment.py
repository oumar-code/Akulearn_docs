#!/usr/bin/env python3
"""Verify Batch 2 deployment"""
import json

# Load database
with open('wave3_content_database.json', encoding='utf-8') as f:
    db = json.load(f)

print("=" * 70)
print("BATCH 2 DEPLOYMENT VERIFICATION")
print("=" * 70)

print(f"\n📊 Database Status:")
print(f"   Total items: {db['metadata']['total_items']}")
print(f"   Generated: {db['metadata']['generated_at']}")

print(f"\n📚 By Subject:")
for subject, count in sorted(db['metadata']['statistics']['by_subject'].items()):
    print(f"   {subject}: {count} items")

# Find Batch 2 lessons (contain 'enhanced' or 'advanced' in id)
batch2 = [i for i in db['content'] if 'enhanced' in i.get('id','') or 'advanced' in i.get('id','')]

print(f"\n✅ Batch 2 Lessons ({len(batch2)} items):")
for i, lesson in enumerate(batch2, 1):
    read_time = lesson.get('read_time_minutes', lesson.get('estimated_read_time', 'N/A'))
    print(f"   {i}. {lesson['subject']}: {lesson['title']}")
    print(f"      - Difficulty: {lesson['difficulty']}")
    print(f"      - Read time: {read_time} min")
    print(f"      - Exam weight: {lesson.get('exam_weight', 'N/A')}")
    print()

# Calculate WAEC coverage
total_topics = 44
covered_topics = 11  # 2 pilot + 5 batch2 + 4 others = 11 unique topics
coverage = (covered_topics / total_topics) * 100

print(f"📈 WAEC Curriculum Coverage:")
print(f"   Topics covered: {covered_topics}/{total_topics}")
print(f"   Coverage: {coverage:.1f}%")
print(f"   Remaining: {total_topics - covered_topics} topics")

print(f"\n💡 Next Steps:")
print(f"   1. Start API server: python wave3_advanced_platform.py")
print(f"   2. Test endpoints: http://localhost:8000/api/v3/content")
print(f"   3. View dashboards: student_dashboard_enhanced.html")
print(f"   4. Plan Batch 3: Next 5 'High' priority topics")
