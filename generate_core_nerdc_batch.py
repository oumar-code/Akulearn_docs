#!/usr/bin/env python3
"""
Generate a focused batch of 50 core NERDC topics across all subjects and levels
Priority: SS1 foundational topics first, then key SS2/SS3 topics
"""

import json
from datetime import datetime
from pathlib import Path
import sys

# Add path for imports
sys.path.insert(0, str(Path(__file__).parent))
from enhanced_content_generator import EnhancedContentGenerator

# Curated list of 50 most important NERDC topics
CORE_NERDC_TOPICS = [
    # Mathematics SS1 (5)
    ("Mathematics", "Number and Numeration", "SS1", "basic"),
    ("Mathematics", "Algebraic Expressions", "SS1", "basic"),
    ("Mathematics", "Linear Equations", "SS1", "basic"),
    ("Mathematics", "Geometry - Angles and Shapes", "SS1", "basic"),
    ("Mathematics", "Statistics and Probability", "SS1", "intermediate"),
    
    # Mathematics SS2 (3)
    ("Mathematics", "Quadratic Functions", "SS2", "intermediate"),
    ("Mathematics", "Trigonometric Functions", "SS2", "intermediate"),
    ("Mathematics", "Coordinate Geometry", "SS2", "intermediate"),
    
    # Mathematics SS3 (2)
    ("Mathematics", "Differentiation", "SS3", "advanced"),
    ("Mathematics", "Integration", "SS3", "advanced"),
    
    # Physics SS1 (5)
    ("Physics", "Measurement and Units", "SS1", "basic"),
    ("Physics", "Mechanics - Motion", "SS1", "basic"),
    ("Physics", "Mechanics - Forces", "SS1", "basic"),
    ("Physics", "Work, Energy and Power", "SS1", "intermediate"),
    ("Physics", "Heat and Temperature", "SS1", "intermediate"),
    
    # Physics SS2 (3)
    ("Physics", "Electricity and Magnetism", "SS2", "intermediate"),
    ("Physics", "Optics and Light", "SS2", "intermediate"),
    ("Physics", "Electrical Circuits", "SS2", "intermediate"),
    
    # Physics SS3 (2)
    ("Physics", "Modern Physics - Quantum Theory", "SS3", "advanced"),
    ("Physics", "Nuclear Physics", "SS3", "advanced"),
    
    # Chemistry SS1 (4)
    ("Chemistry", "Atomic Structure", "SS1", "basic"),
    ("Chemistry", "Bonding and Structure", "SS1", "basic"),
    ("Chemistry", "Periodic Table", "SS1", "intermediate"),
    ("Chemistry", "Acids, Bases and Salts", "SS1", "intermediate"),
    
    # Chemistry SS2 (3)
    ("Chemistry", "Rate of Reactions", "SS2", "intermediate"),
    ("Chemistry", "Chemical Equilibrium", "SS2", "intermediate"),
    ("Chemistry", "Organic Chemistry - Hydrocarbons", "SS2", "advanced"),
    
    # Chemistry SS3 (2)
    ("Chemistry", "Industrial Chemistry", "SS3", "advanced"),
    ("Chemistry", "Environmental Chemistry", "SS3", "advanced"),
    
    # Biology SS1 (4)
    ("Biology", "Cell Biology", "SS1", "basic"),
    ("Biology", "Plant Nutrition and Photosynthesis", "SS1", "basic"),
    ("Biology", "Animal Nutrition and Digestion", "SS1", "intermediate"),
    ("Biology", "Transport in Animals", "SS1", "intermediate"),
    
    # Biology SS2 (3)
    ("Biology", "Reproduction in Plants", "SS2", "intermediate"),
    ("Biology", "Genetics and Heredity", "SS2", "intermediate"),
    ("Biology", "Evolution", "SS2", "advanced"),
    
    # Biology SS3 (2)
    ("Biology", "Immunology and Disease", "SS3", "advanced"),
    ("Biology", "Conservation and Biodiversity", "SS3", "advanced"),
    
    # English Language (5 total)
    ("English Language", "Comprehension and Summary", "SS1", "intermediate"),
    ("English Language", "Grammar and Usage", "SS1", "intermediate"),
    ("English Language", "Syntax and Sentence Structure", "SS2", "intermediate"),
    ("English Language", "Poetry Analysis", "SS3", "advanced"),
    ("English Language", "Essay Writing", "SS1", "intermediate"),
    
    # Further Mathematics (3)
    ("Further Mathematics", "Set Theory", "SS1", "intermediate"),
    ("Further Mathematics", "Permutations and Combinations", "SS2", "advanced"),
    ("Further Mathematics", "Linear Programming", "SS3", "advanced"),
    
    # Geography (3)
    ("Geography", "Map Reading and Interpretation", "SS1", "basic"),
    ("Geography", "Climate and Weather", "SS1", "intermediate"),
    ("Geography", "Economic Geography", "SS3", "advanced"),
    
    # Economics (3)
    ("Economics", "Basic Economic Concepts", "SS1", "basic"),
    ("Economics", "Perfect Competition", "SS2", "intermediate"),
    ("Economics", "Macroeconomics - National Income", "SS3", "advanced"),
    
    # Computer Science (3)
    ("Computer Science", "Computer Hardware and Components", "SS1", "basic"),
    ("Computer Science", "Data Structures", "SS2", "intermediate"),
    ("Computer Science", "Database Management", "SS3", "advanced"),
]

def main():
    print("\n" + "="*70)
    print("GENERATING 50 CORE NERDC TOPICS")
    print("="*70)
    
    db_path = Path("connected_stack/backend/content_data.json")
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    generator = EnhancedContentGenerator(use_mcp=True)
    
    generated = 0
    failed = 0
    
    for idx, (subject, topic, level, difficulty) in enumerate(CORE_NERDC_TOPICS, 1):
        print(f"[{idx:2d}/50] {subject} {level} > {topic[:30]}...", end=" ", flush=True)
        
        try:
            lesson = generator.generate(
                subject=subject,
                topic=topic,
                difficulty=difficulty,
                use_mcp=True,
                include_nigerian_context=True
            )
            
            lesson_id = f"nerdc_{subject.lower().replace(' ','_')}_{level}_{topic.lower().replace(' ','_').replace('-','_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            lesson["id"] = lesson_id
            lesson["level"] = level
            lesson["curriculum_framework"] = "NERDC Senior Secondary School"
            lesson["content_type"] = "study_guide"
            
            db["content"].append(lesson)
            generated += 1
            print("✅")
            
        except Exception as e:
            print(f"❌ {str(e)[:30]}")
            failed += 1
    
    # Update metadata
    db["metadata"] = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "total_items": len(db["content"]),
        "framework": "NERDC",
        "batch": "Core 50 topics"
    }
    
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"✅ Generated: {generated}/{len(CORE_NERDC_TOPICS)}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total in DB: {len(db['content'])} items")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
