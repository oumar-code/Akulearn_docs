#!/usr/bin/env python3
"""
Generate seed lessons for newly added NERDC subjects based on nerdc_curriculum_map.json.
Subjects: Government, Commerce, Accounting, Agricultural Science, Literature in English
"""

import json
from datetime import datetime
from pathlib import Path
from enhanced_content_generator import EnhancedContentGenerator

NEW_SUBJECTS = [
    "Government",
    "Commerce",
    "Accounting",
    "Agricultural Science",
    "Literature in English",
]

ROOT = Path(__file__).parent
MAP_PATH = ROOT / "nerdc_curriculum_map.json"
DB_PATH = ROOT / "connected_stack" / "backend" / "content_data.json"


def main():
    # Load curriculum map and database
    curriculum = json.load(open(MAP_PATH, "r", encoding="utf-8"))
    db = json.load(open(DB_PATH, "r", encoding="utf-8"))
    subjects = curriculum["subjects"]

    generator = EnhancedContentGenerator(use_mcp=False)

    print("\n=== Generating Seed Lessons for New NERDC Subjects ===\n")
    total_created = 0

    for subject in NEW_SUBJECTS:
        if subject not in subjects:
            print(f"Skipping {subject}: not found in curriculum map")
            continue
        print(f"\nSubject: {subject}")
        # Iterate levels
        for level in ["SS1", "SS2", "SS3"]:
            topics = subjects[subject].get(level, [])
            for topic in topics:
                title = f"{level} - {topic}"
                print(f"  [GEN] {title}...", end=" ")
                try:
                    lesson = generator.generate(
                        subject=subject,
                        topic=title,
                        difficulty="intermediate" if level in ("SS1", "SS2") else "advanced",
                        use_mcp=False,
                        include_nigerian_context=True
                    )
                    lesson["id"] = f"nerdc_{level.lower()}_{subject.lower().replace(' ','_')}_{topic.lower().replace(' ','_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    lesson["curriculum"] = "NERDC"
                    lesson["level"] = level
                    lesson["content_type"] = "study_guide"
                    db["content"].append(lesson)
                    total_created += 1
                    print("OK")
                except Exception as e:
                    print(f"ERROR: {str(e)[:60]}")

    # Update metadata
    meta = db.setdefault("metadata", {})
    meta["total_items"] = len(db["content"])
    meta["last_updated"] = datetime.now().isoformat()

    # Save
    json.dump(db, open(DB_PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\nCreated {total_created} lessons across new subjects. Total items: {len(db['content'])}")

if __name__ == "__main__":
    main()
