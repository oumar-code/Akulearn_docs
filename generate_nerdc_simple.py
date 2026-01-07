#!/usr/bin/env python3
"""Generate core NERDC topics without MCP - simpler and faster"""

import json
from datetime import datetime
from enhanced_content_generator import EnhancedContentGenerator

# 25 high-priority NERDC topics (reduced from 50 for speed)
NERDC_TOPICS = [
    # Mathematics (5)
    ("Mathematics", "SS1", "Indices and Logarithms", "intermediate"),
    ("Mathematics", "SS2", "Quadratic Equations", "intermediate"),
    ("Mathematics", "SS3", "Calculus Basics", "advanced"),
    ("Mathematics", "SS1", "Basic Statistics", "intermediate"),
    ("Mathematics", "SS2", "Trigonometry", "intermediate"),
    
    # Physics (5)
    ("Physics", "SS1", "Motion in a Straight Line", "intermediate"),
    ("Physics", "SS2", "Electricity and Magnetism", "intermediate"),
    ("Physics", "SS3", "Wave Motion", "advanced"),
    ("Physics", "SS1", "Force and Pressure", "intermediate"),
    ("Physics", "SS2", "Energy and Work", "intermediate"),
    
    # Chemistry (5)
    ("Chemistry", "SS1", "Atomic Structure", "intermediate"),
    ("Chemistry", "SS2", "Chemical Bonding", "intermediate"),
    ("Chemistry", "SS3", "Organic Chemistry", "advanced"),
    ("Chemistry", "SS1", "Acids and Bases", "intermediate"),
    ("Chemistry", "SS2", "Redox Reactions", "intermediate"),
    
    # Biology (5)
    ("Biology", "SS1", "Cell Biology", "intermediate"),
    ("Biology", "SS2", "Genetics", "intermediate"),
    ("Biology", "SS3", "Evolution", "advanced"),
    ("Biology", "SS1", "Human Anatomy", "intermediate"),
    ("Biology", "SS2", "Ecology", "intermediate"),
    
    # English Language (5)
    ("English Language", "SS1", "Reading Comprehension", "intermediate"),
    ("English Language", "SS2", "Writing Skills", "intermediate"),
    ("English Language", "SS3", "Literature Analysis", "advanced"),
    ("English Language", "SS1", "Grammar Fundamentals", "intermediate"),
    ("English Language", "SS2", "Oral Communication", "intermediate"),
]

def main():
    with open("connected_stack/backend/content_data.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    generator = EnhancedContentGenerator(use_mcp=False)
    
    print("\n=== Generating 25 Core NERDC Topics (No MCP) ===\n")
    
    success_count = 0
    for subject, level, topic, difficulty in NERDC_TOPICS:
        print(f"[GEN] {subject} {level}: {topic}...", end=" ", flush=True)
        try:
            lesson = generator.generate(
                subject=subject,
                topic=f"{level} - {topic}",
                difficulty=difficulty,
                use_mcp=False,
                include_nigerian_context=True
            )
            lesson["id"] = f"nerdc_{level.lower()}_{subject.lower().replace(' ','_')}_{topic.lower().replace(' ','_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            lesson["curriculum"] = "NERDC"
            lesson["level"] = level
            lesson["content_type"] = "study_guide"
            db["content"].append(lesson)
            success_count += 1
            print("OK")
        except Exception as e:
            print(f"ERROR: {str(e)[:40]}")
    
    # Update metadata if it exists
    if "metadata" not in db:
        db["metadata"] = {}
    db["metadata"]["total_items"] = len(db["content"])
    db["metadata"]["last_updated"] = datetime.now().isoformat()
    
    with open("connected_stack/backend/content_data.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    print(f"\nGenerated {success_count}/25 topics. Total NERDC items: {len(db['content'])}\n")

if __name__ == "__main__":
    main()
