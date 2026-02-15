#!/usr/bin/env python3
"""
Generate NERDC content for all missing topics across SS1-SS3 to reach full coverage.
Uses EnhancedContentGenerator with MCP research.
"""

import json
from datetime import datetime
from pathlib import Path
from enhanced_content_generator import EnhancedContentGenerator

# Map of subject to [SS1 topics, SS2 topics, SS3 topics]
NERDC_TOPICS = {
    "Mathematics": {
        "SS1": [
            "Number and Numeration",
            "Algebraic Expressions",
            "Linear Equations",
            "Simultaneous Linear Equations",
            "Quadratic Equations",
            "Indices and Logarithms",
            "Sequences and Series",
            "Geometry - Angles and Shapes",
            "Trigonometry",
            "Statistics and Probability"
        ],
        "SS2": [
            "Quadratic Functions",
            "Polynomial Functions",
            "Rational Functions",
            "Exponential and Logarithmic Functions",
            "Trigonometric Functions",
            "Coordinate Geometry",
            "Circle Geometry",
            "Mensuration",
            "Statistics",
            "Probability"
        ],
        "SS3": [
            "Calculus - Limits and Continuity",
            "Differentiation",
            "Integration",
            "Vectors",
            "Complex Numbers",
            "Matrices and Determinants",
            "Linear Inequalities",
            "Mathematical Reasoning"
        ]
    },
    "Physics": {
        "SS1": [
            "Measurement and Units",
            "Mechanics - Motion",
            "Mechanics - Forces",
            "Mechanics - Equilibrium",
            "Work, Energy and Power",
            "Simple Machines",
            "Heat and Temperature",
            "Gases and Kinetic Theory",
            "Waves and Oscillations"
        ],
        "SS2": [
            "Electricity and Magnetism",
            "Electromagnetic Induction",
            "Optics and Light",
            "Sound Waves",
            "Electrical Circuits",
            "Effects of Electric Current",
            "Magnetic Fields",
            "Thermal Physics"
        ],
        "SS3": [
            "Modern Physics - Quantum Theory",
            "Nuclear Physics",
            "Atomic Structure",
            "Semiconductor Physics",
            "Communication and Electronics",
            "X-rays",
            "Radioactivity",
            "Photon Theory"
        ]
    },
    "Chemistry": {
        "SS1": [
            "Atomic Structure",
            "Bonding and Structure",
            "Periodic Table",
            "Chemical Equations",
            "Stoichiometry",
            "Acids, Bases and Salts",
            "Oxidation and Reduction"
        ],
        "SS2": [
            "Rate of Reactions",
            "Chemical Equilibrium",
            "Energy Changes in Reactions",
            "Electrochemistry",
            "Organic Chemistry - Hydrocarbons",
            "Organic Chemistry - Functional Groups",
            "Polymers"
        ],
        "SS3": [
            "Advanced Organic Chemistry",
            "Analytical Chemistry",
            "Industrial Chemistry",
            "Pharmaceutical Chemistry",
            "Environmental Chemistry",
            "Biochemistry"
        ]
    },
    "Biology": {
        "SS1": [
            "Cell Biology",
            "Plant Nutrition and Photosynthesis",
            "Animal Nutrition and Digestion",
            "Transport in Plants",
            "Transport in Animals",
            "Excretion and Osmoregulation",
            "Coordination and Control"
        ],
        "SS2": [
            "Reproduction in Plants",
            "Reproduction in Animals",
            "Growth and Development",
            "Genetics and Heredity",
            "Variation and Mutation",
            "Evolution",
            "Ecology and Ecosystems"
        ],
        "SS3": [
            "Immunology and Disease",
            "Homeostasis",
            "Nervous System and Behavior",
            "Endocrine System",
            "Muscles and Movement",
            "Conservation and Biodiversity"
        ]
    },
    "English Language": {
        "SS1": [
            "Comprehension and Summary",
            "Grammar and Usage",
            "Vocabulary and Spelling",
            "Essay Writing",
            "Letter Writing"
        ],
        "SS2": [
            "Advanced Comprehension",
            "Syntax and Sentence Structure",
            "Stylistics and Literary Analysis",
            "Report Writing",
            "Speech and Oral Communication"
        ],
        "SS3": [
            "Critical Analysis",
            "Poetry Analysis",
            "Prose Analysis",
            "Drama Analysis",
            "Advanced Writing Skills"
        ]
    }
}

def get_difficulty(ss_level):
    return "basic" if ss_level == "SS1" else "intermediate" if ss_level == "SS2" else "advanced"


def main():
    print("\n" + "="*70)
    print("GENERATING NERDC MISSING TOPICS FOR 100% COVERAGE")
    print("="*70)
    
    # Load backend database
    db_path = Path("connected_stack/backend/content_data.json")
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    existing_ids = {item.get("id") for item in db.get("content", [])}
    
    # Initialize generator
    generator = EnhancedContentGenerator(use_mcp=True)
    
    generated = 0
    skipped = 0
    
    for subject, levels_data in NERDC_TOPICS.items():
        for level, topics in levels_data.items():
            for topic in topics:
                lesson_id = f"nerdc_{subject.lower().replace(' ','_')}_{level}_{topic.lower().replace(' ','_').replace('-','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                if lesson_id in existing_ids:
                    skipped += 1
                    continue
                
                print(f"[GEN] {subject} {level} > {topic}...", end=" ", flush=True)
                
                try:
                    lesson = generator.generate(
                        subject=subject,
                        topic=topic,
                        difficulty=get_difficulty(level),
                        use_mcp=True,
                        include_nigerian_context=True
                    )
                    
                    lesson["id"] = lesson_id
                    lesson["level"] = level
                    lesson["curriculum_framework"] = "NERDC"
                    lesson["content_type"] = "study_guide"
                    
                    db["content"].append(lesson)
                    generated += 1
                    print("✅")
                
                except Exception as e:
                    print(f"❌ {str(e)[:40]}")
    
    # Update metadata
    db["metadata"] = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "total_items": len(db["content"]),
        "curriculum_framework": "NERDC",
        "levels": ["SS1", "SS2", "SS3"]
    }
    
    # Save
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"Generated: {generated} new NERDC topics")
    print(f"Skipped: {skipped} (already exist)")
    print(f"Total in DB: {len(db['content'])} items")
    print(f"Saved to: {db_path}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
