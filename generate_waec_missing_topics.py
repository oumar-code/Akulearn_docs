#!/usr/bin/env python3
"""
Generate WAEC content for specific missing topics to reach 100% coverage.
Uses EnhancedContentGenerator with MCP research (Brave + Wikipedia).
"""

import json
from datetime import datetime
from pathlib import Path
from enhanced_content_generator import EnhancedContentGenerator

# Topics to fill based on curriculum_map.json gaps
WAEC_TOPICS_TO_GENERATE = [
    # Mathematics (if missing)
    ("Mathematics", "Number Bases", "intermediate"),
    ("Mathematics", "Modular Arithmetic", "intermediate"),
    ("Mathematics", "Binary Operations", "advanced"),
    ("Mathematics", "Circle Theorems", "advanced"),
    ("Mathematics", "Differentiation", "advanced"),
    ("Mathematics", "Integration", "advanced"),
    ("Mathematics", "Statistics", "intermediate"),
    ("Mathematics", "Probability", "intermediate"),
    
    # Physics (if missing)
    ("Physics", "Motion", "intermediate"),
    ("Physics", "Simple Machines", "basic"),
    ("Physics", "Gas Laws", "advanced"),
    ("Physics", "Static Electricity", "intermediate"),
    ("Physics", "Electrical Energy and Power", "intermediate"),
    
    # Chemistry (if missing)
    ("Chemistry", "Rates of Chemical Reactions", "intermediate"),
    ("Chemistry", "Organic Chemistry - Hydrocarbons", "advanced"),
    
    # Biology (if missing)
    ("Biology", "Excretory System", "intermediate"),
    
    # English (if missing)
    ("English Language", "Oral English", "intermediate"),
]

def main():
    print("\n" + "="*70)
    print("GENERATING WAEC MISSING TOPICS FOR 100% COVERAGE")
    print("="*70)
    
    # Load existing database
    with open("wave3_content_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    existing_ids = {item.get("id") for item in db.get("content", [])}
    
    # Initialize generator
    generator = EnhancedContentGenerator(use_mcp=True)
    
    generated = 0
    skipped = 0
    
    for subject, topic, difficulty in WAEC_TOPICS_TO_GENERATE:
        lesson_id = f"waec_{subject.lower().replace(' ','_')}_{topic.lower().replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if lesson_id in existing_ids:
            print(f"[SKIP] {subject} > {topic} (already exists)")
            skipped += 1
            continue
        
        print(f"[GEN] {subject} > {topic}...", end=" ", flush=True)
        
        try:
            lesson = generator.generate(
                subject=subject,
                topic=topic,
                difficulty=difficulty,
                use_mcp=True,
                include_nigerian_context=True
            )
            
            lesson["id"] = lesson_id
            lesson["exam_board"] = "WAEC"
            lesson["content_type"] = "study_guide"
            
            db["content"].append(lesson)
            generated += 1
            print("✅")
        
        except Exception as e:
            print(f"❌ {str(e)[:50]}")
    
    # Update metadata
    db["metadata"]["last_updated"] = datetime.now().isoformat()
    db["metadata"]["total_items"] = len(db["content"])
    
    # Save
    with open("wave3_content_database.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"Generated: {generated} new topics")
    print(f"Skipped: {skipped} (already exist)")
    print(f"Total in DB: {len(db['content'])} items")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
