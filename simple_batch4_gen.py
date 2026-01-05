#!/usr/bin/env python3
"""
Simple Batch 4 Generator - No hang, direct execution
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from enhanced_content_generator import EnhancedContentGenerator

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Batch 4 topics
BATCH_4_TOPICS = [
    ("Mathematics", "Quadratic Equations and Functions", "Intermediate"),
    ("Mathematics", "Coordinate Geometry", "Intermediate"),
    ("Physics", "Electricity and Magnetism", "Intermediate"),
    ("Physics", "Waves and Oscillations", "Beginner"),
    ("Chemistry", "Atomic Structure and Bonding", "Beginner"),
    ("Biology", "Cell Structure and Function", "Beginner"),
    ("Economics", "Microeconomics Principles", "Intermediate"),
    ("Geography", "Geomorphology and Ecosystems", "Beginner")
]

def main():
    logger.info("\n" + "="*60)
    logger.info("🚀 BATCH 4 GENERATION - SIMPLIFIED")
    logger.info("="*60 + "\n")
    
    # Step 1: Generate lessons
    logger.info("📚 Generating 8 Batch 4 lessons...")
    generator = EnhancedContentGenerator(use_mcp=False)
    lessons = generator.generate_batch(topics=BATCH_4_TOPICS)
    
    logger.info(f"✅ Generated {len(lessons)} lessons")
    logger.info(f"   Total duration: {generator.total_duration} minutes\n")
    
    # Step 2: Save to file
    output_file = "generated_content/batch4_content_complete.json"
    Path("generated_content").mkdir(exist_ok=True)
    
    batch_data = {
        "metadata": {
            "batch": "Batch 4",
            "generatedAt": datetime.now().isoformat(),
            "count": len(lessons),
            "totalDuration": generator.total_duration,
            "topics": [f"{s} - {t}" for s, t, _ in BATCH_4_TOPICS]
        },
        "lessons": lessons
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(batch_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ Saved to: {output_file}")
    
    # Step 3: Show sample
    if lessons:
        sample = lessons[0]
        logger.info(f"\n📖 Sample Lesson:")
        logger.info(f"   Title: {sample['title']}")
        logger.info(f"   Subject: {sample['subject']}")
        logger.info(f"   Duration: {sample['duration_minutes']} min")
        logger.info(f"   Objectives: {len(sample['learningObjectives'])}")
        logger.info(f"   Sections: {len(sample['sections'])}")
    
    logger.info("\n" + "="*60)
    logger.info("✅ BATCH 4 GENERATION COMPLETE!")
    logger.info("="*60)
    logger.info(f"\nNext: Merge into wave3_content_database.json manually")
    logger.info(f"File: {output_file}\n")

if __name__ == "__main__":
    main()
