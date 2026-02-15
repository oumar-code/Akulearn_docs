#!/usr/bin/env python3
"""
Deploy Batch 3 Content to Wave 3 Platform
Takes batch3_content_complete.json and imports lessons into wave3_content_database.json
"""

import json
from datetime import datetime
from pathlib import Path
from collections import Counter


def _recalculate_statistics(content_items):
    """Recalculate metadata statistics from all content items."""
    by_subject = Counter(item.get("subject", "Unknown") for item in content_items)
    by_type = Counter(item.get("content_type", "study_guide") for item in content_items)
    by_difficulty = Counter(item.get("difficulty", "unknown") for item in content_items)

    return {
        "total_imported": len(content_items),
        "by_subject": dict(by_subject),
        "by_type": dict(by_type),
        "by_difficulty": dict(by_difficulty),
        "errors": [],
    }


def _transform_lesson(lesson):
    """Map a Batch 3 lesson into Wave 3 schema."""
    return {
        "id": lesson.get("id"),
        "title": lesson.get("title"),
        "subject": lesson.get("subject"),
        "topic": lesson.get("topic"),
        "difficulty": lesson.get("difficulty", "intermediate"),
        "exam_weight": lesson.get("exam_weight", "high"),
        "read_time_minutes": lesson.get("read_time_minutes", lesson.get("estimated_read_time", 25)),
        "content": lesson.get("content", lesson.get("content_summary", "")),
        "summary": lesson.get("summary", lesson.get("content_summary", "")),
        "learning_objectives": lesson.get("learning_objectives", []),
        "prerequisites": lesson.get("prerequisites", []),
        "diagrams": lesson.get("diagrams", []),
        "tags": lesson.get("tags", []),
        "nigerian_context": lesson.get("nigerian_context", ""),
        "views": 0,
        "likes": 0,
        "ratings": 0,
        "created_at": lesson.get("created_at", datetime.now().isoformat()),
        "status": "published",
        "content_type": lesson.get("content_type", "study_guide"),
        "exam_board": lesson.get("exam_board", "WAEC"),
    }


def deploy_batch3():
    print("\n" + "=" * 70)
    print("BATCH 3 DEPLOYMENT TO WAVE 3 PLATFORM")
    print("=" * 70)

    # Load batch 3 content
    print("\n📥 Loading batch 3 content...")
    with open("batch3_content_complete.json", encoding="utf-8") as f:
        batch3 = json.load(f)

    batch3_items = batch3.get("lessons", [])
    print(f"   Found {len(batch3_items)} lessons")

    # Load existing database
    print("\n📂 Loading existing Wave 3 database...")
    with open("wave3_content_database.json", encoding="utf-8") as f:
        database = json.load(f)

    existing_count = database["metadata"].get("total_items", len(database.get("content", [])))
    print(f"   Existing items: {existing_count}")

    # Transform and merge batch 3 items
    print("\n🔄 Transforming and merging batch 3 content...")
    added_items = 0
    added_by_subject = {}

    for lesson in batch3_items:
        wave3_item = _transform_lesson(lesson)
        database["content"].append(wave3_item)
        added_items += 1

        subject = wave3_item.get("subject", "Unknown")
        added_by_subject[subject] = added_by_subject.get(subject, 0) + 1

        print(f"   ✓ {wave3_item['title']}")

    # Update metadata
    new_total = existing_count + added_items
    database["metadata"]["total_items"] = new_total
    database["metadata"]["last_updated"] = datetime.now().isoformat()
    database["metadata"]["statistics"] = _recalculate_statistics(database.get("content", []))

    # Save updated database
    print("\n💾 Saving updated database...")
    with open("wave3_content_database.json", "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2, ensure_ascii=False)

    print(f"   ✅ Database saved: wave3_content_database.json")

    # Print summary
    print("\n" + "=" * 70)
    print("DEPLOYMENT STATISTICS")
    print("=" * 70)
    print(f"\n📊 Total items in database: {new_total}")
    print(f"   - Existing items: {existing_count}")
    print(f"   - New batch 3 items: {added_items}")

    print(f"\n📚 New items by subject:")
    for subject, count in sorted(added_by_subject.items()):
        print(f"   - {subject}: {count}")

    print(f"\n✅ BATCH 3 DEPLOYMENT COMPLETE")
    print("=" * 70)

    print("\nNext steps:")
    print("1. Start Wave 3 API server: python wave3_advanced_platform.py")
    print("2. Access API docs: http://localhost:8000/api/docs")
    print("3. Test content endpoints: http://localhost:8000/api/v3/content")
    print("4. View in dashboards: student_dashboard_enhanced.html")


if __name__ == "__main__":
    deploy_batch3()
