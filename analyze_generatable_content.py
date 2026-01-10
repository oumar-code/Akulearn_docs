#!/usr/bin/env python3
"""Analyze lessons to identify those suitable for programmatic visual generation.

Categorizes lessons by what can be auto-generated:
- Venn diagrams (set theory)
- Truth tables (logic)
- Mathematical graphs (functions, equations)
- Chemistry structures (molecular diagrams)
- Circuit diagrams (physics)
- Data visualizations (statistics, economics)
- Interactive simulations (games, experiments)
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


CONTENT_PATH = Path("content_data.json")


GENERATION_CATEGORIES = {
    "venn_diagrams": {
        "keywords": ["set", "venn", "union", "intersection", "complement"],
        "subjects": ["Further Mathematics", "Mathematics"],
        "tool": "matplotlib/pillow",
    },
    "truth_tables": {
        "keywords": ["logic", "truth table", "proposition", "boolean"],
        "subjects": ["Further Mathematics", "Mathematics", "Computer Science"],
        "tool": "HTML table generator",
    },
    "math_graphs": {
        "keywords": ["graph", "function", "equation", "plot", "quadratic", "linear", "parabola", "coordinates"],
        "subjects": ["Mathematics", "Further Mathematics", "Physics"],
        "tool": "matplotlib/plotly",
    },
    "chemistry_diagrams": {
        "keywords": ["molecule", "compound", "bond", "structure", "reaction", "electron", "atomic"],
        "subjects": ["Chemistry"],
        "tool": "RDKit/ChemDraw alternatives",
    },
    "circuit_diagrams": {
        "keywords": ["circuit", "resistor", "capacitor", "voltage", "current", "ohm"],
        "subjects": ["Physics"],
        "tool": "schemdraw/circuitikz",
    },
    "data_viz": {
        "keywords": ["data", "statistics", "chart", "bar", "pie", "histogram", "distribution"],
        "subjects": ["Economics", "Geography", "Mathematics"],
        "tool": "matplotlib/plotly",
    },
    "interactive_games": {
        "keywords": ["practice", "quiz", "game", "interactive", "simulation", "experiment"],
        "subjects": ["all"],
        "tool": "HTML5/JavaScript",
    },
    "ascii_diagrams": {
        "keywords": ["diagram", "flow", "process", "structure", "hierarchy"],
        "subjects": ["all"],
        "tool": "ASCII art generator",
    },
}


def load_content() -> Dict[str, Any]:
    with CONTENT_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def analyze_lesson(lesson: Dict[str, Any]) -> List[str]:
    """Determine which generation categories apply to a lesson."""
    categories = []
    
    subject = lesson.get("subject", "").lower()
    title = lesson.get("title", "").lower()
    content = lesson.get("content", "").lower()
    objectives = " ".join(lesson.get("learning_objectives", [])).lower()
    
    full_text = f"{title} {content} {objectives}"
    
    for cat_name, cat_info in GENERATION_CATEGORIES.items():
        # Check subject match
        subject_match = (
            "all" in cat_info["subjects"] or
            any(s.lower() in subject for s in cat_info["subjects"])
        )
        
        # Check keyword match
        keyword_match = any(kw in full_text for kw in cat_info["keywords"])
        
        if subject_match and keyword_match:
            categories.append(cat_name)
    
    return categories


def main():
    data = load_content()
    lessons = data.get("content", [])
    
    results = defaultdict(list)
    lesson_categories = {}
    
    for lesson in lessons:
        if not isinstance(lesson, dict):
            continue
        
        lesson_id = lesson.get("id", "unknown")
        title = lesson.get("title", "Untitled")
        subject = lesson.get("subject", "Unknown")
        
        categories = analyze_lesson(lesson)
        
        if categories:
            lesson_categories[lesson_id] = {
                "title": title,
                "subject": subject,
                "categories": categories,
                "priority": len(categories),  # More categories = higher priority
            }
            
            for cat in categories:
                results[cat].append({
                    "id": lesson_id,
                    "title": title[:60],
                    "subject": subject,
                })
    
    # Print summary
    print("\n" + "="*70)
    print("PROGRAMMATIC CONTENT GENERATION ANALYSIS")
    print("="*70 + "\n")
    
    total_generatable = len(lesson_categories)
    print(f"📊 {total_generatable} of {len(lessons)} lessons can have auto-generated visuals\n")
    
    for cat_name, lessons_list in sorted(results.items(), key=lambda x: -len(x[1])):
        cat_info = GENERATION_CATEGORIES[cat_name]
        print(f"🎨 {cat_name.replace('_', ' ').title()}: {len(lessons_list)} lessons")
        print(f"   Tool: {cat_info['tool']}")
        print(f"   Top lessons:")
        for lesson in lessons_list[:3]:
            print(f"     - {lesson['subject']}: {lesson['title']}")
        print()
    
    # High-priority lessons (multiple categories)
    print("\n" + "="*70)
    print("HIGH-PRIORITY LESSONS (Multiple Generation Options)")
    print("="*70 + "\n")
    
    high_priority = sorted(
        [(lid, info) for lid, info in lesson_categories.items() if info["priority"] >= 2],
        key=lambda x: -x[1]["priority"]
    )
    
    for lesson_id, info in high_priority[:10]:
        print(f"✨ {info['subject']}: {info['title'][:50]}")
        print(f"   Categories: {', '.join(info['categories'])}")
        print(f"   ID: {lesson_id}\n")
    
    # Save detailed report
    report_path = Path("generatable_content_report.json")
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "summary": {
                    "total_lessons": len(lessons),
                    "generatable_lessons": total_generatable,
                    "categories": {k: len(v) for k, v in results.items()},
                },
                "by_category": results,
                "high_priority": [
                    {"id": lid, **info} for lid, info in high_priority
                ],
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    
    print(f"📄 Detailed report saved to: {report_path}\n")


if __name__ == "__main__":
    main()
