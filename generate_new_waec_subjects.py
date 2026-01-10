#!/usr/bin/env python3
"""
Generate lessons for new WAEC subjects (Government, Commerce, Accounting, 
Agricultural Science, Literature in English).
"""

import json
from datetime import datetime
from pathlib import Path
from enhanced_content_generator import EnhancedContentGenerator

NEW_SUBJECTS = ["Government", "Commerce", "Accounting", "Agricultural Science", "Literature in English"]

ROOT = Path(__file__).parent
WAEC_DB = ROOT / "wave3_content_database.json"
CURR_PATH = ROOT / "curriculum_map.json"


def main():
    curriculum = json.load(open(CURR_PATH, "r", encoding="utf-8"))
    db = json.load(open(WAEC_DB, "r", encoding="utf-8"))
    subjects = curriculum["subjects"]

    generator = EnhancedContentGenerator(use_mcp=False)

    print("\n=== Generating WAEC Lessons for New Subjects ===\n")
    total_created = 0

    for subject in NEW_SUBJECTS:
        if subject not in subjects:
            print(f"Skipping {subject}: not found in curriculum map")
            continue

        topics = subjects[subject].get("topics", [])
        print(f"\n{subject}: generating {len(topics)} topics")

        for topic_obj in topics:
            topic_name = topic_obj.get("name", "Unknown")
            print(f"  [GEN] {topic_name}...", end=" ")
            try:
                lesson = generator.generate(
                    subject=subject,
                    topic=topic_name,
                    difficulty=topic_obj.get("difficulty", "intermediate"),
                    use_mcp=False,
                    include_nigerian_context=True
                )
                lesson["id"] = f"waec_{subject.lower().replace(' ','_')}_{topic_name.lower().replace(' ','_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                lesson["exam_board"] = "WAEC"
                lesson["content_type"] = "study_guide"
                db["content"].append(lesson)
                total_created += 1
                print("OK")
            except Exception as e:
                print(f"ERROR: {str(e)[:50]}")

    # Update metadata
    meta = db.setdefault("metadata", {})
    meta["total_items"] = len(db["content"])
    meta["last_updated"] = datetime.now().isoformat()

    # Save
    json.dump(db, open(WAEC_DB, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\nCreated {total_created} WAEC lessons. Total items: {len(db['content'])}")


if __name__ == "__main__":
    main()
