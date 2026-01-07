#!/usr/bin/env python3
"""Generate the 5 missing WAEC English Language topics quickly"""

import json
from datetime import datetime
from enhanced_content_generator import EnhancedContentGenerator

ENGLISH_TOPICS = [
    ("English Language", "Comprehension and Summary", "intermediate"),
    ("English Language", "Grammar and Usage", "intermediate"),
    ("English Language", "Essay Writing", "intermediate"),
    ("English Language", "Oral English", "intermediate"),
    ("English Language", "Literature", "intermediate"),
]

def main():
    with open("wave3_content_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    generator = EnhancedContentGenerator(use_mcp=True)
    
    print("\n=== Generating 5 WAEC English Language Topics ===\n")
    
    for subject, topic, difficulty in ENGLISH_TOPICS:
        print(f"[GEN] {topic}...", end=" ", flush=True)
        try:
            lesson = generator.generate(
                subject=subject,
                topic=topic,
                difficulty=difficulty,
                use_mcp=False,  # Disable MCP due to wrapper issues
                include_nigerian_context=True
            )
            lesson["id"] = f"waec_english_{topic.lower().replace(' ','_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            lesson["exam_board"] = "WAEC"
            lesson["content_type"] = "study_guide"
            db["content"].append(lesson)
            print("OK")
        except Exception as e:
            print(f"ERROR: {str(e)[:40]}")
    
    db["metadata"]["total_items"] = len(db["content"])
    db["metadata"]["last_updated"] = datetime.now().isoformat()
    
    with open("wave3_content_database.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    print(f"\nGenerated English topics. Total: {len(db['content'])} items\n")

if __name__ == "__main__":
    main()
