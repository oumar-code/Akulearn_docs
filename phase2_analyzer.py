#!/usr/bin/env python3
"""Phase 2: Mathematical Graphing Engine

Analyzes lessons to identify graphing opportunities:
- Mathematical functions and equations
- Data visualizations (charts, histograms)
- Economic and geographic data representations
- Physics and chemistry diagrams with numerical data
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict
import re


CONTENT_PATH = Path("content_data.json")


GRAPHING_CATEGORIES = {
    "function_graphs": {
        "keywords": ["function", "graph", "plot", "quadratic", "linear", "parabola", "exponential", "logarithm", "polynomial"],
        "subjects": ["Mathematics", "Further Mathematics", "Physics"],
        "tool": "matplotlib/plotly",
        "chart_type": "line/scatter plot",
        "priority": 10
    },
    "coordinate_geometry": {
        "keywords": ["coordinate", "cartesian", "distance", "gradient", "slope", "point", "line equation"],
        "subjects": ["Mathematics", "Further Mathematics"],
        "tool": "matplotlib",
        "chart_type": "scatter plot",
        "priority": 9
    },
    "trigonometric": {
        "keywords": ["trigonometric", "sine", "cosine", "tangent", "radian", "angle", "sin", "cos", "tan"],
        "subjects": ["Mathematics", "Further Mathematics", "Physics"],
        "tool": "matplotlib/plotly",
        "chart_type": "line plot",
        "priority": 9
    },
    "bar_chart": {
        "keywords": ["data", "bar", "comparison", "frequency", "distribution", "statistics", "count"],
        "subjects": ["Economics", "Geography", "Mathematics", "Statistics"],
        "tool": "plotly/matplotlib",
        "chart_type": "bar chart",
        "priority": 8
    },
    "pie_chart": {
        "keywords": ["percentage", "proportion", "pie", "sector", "composition", "share"],
        "subjects": ["Economics", "Geography", "Mathematics"],
        "tool": "plotly/matplotlib",
        "chart_type": "pie chart",
        "priority": 7
    },
    "histogram": {
        "keywords": ["histogram", "frequency distribution", "range", "interval", "class", "bin"],
        "subjects": ["Mathematics", "Economics", "Biology"],
        "tool": "matplotlib/plotly",
        "chart_type": "histogram",
        "priority": 8
    },
    "scatter_plot": {
        "keywords": ["scatter", "correlation", "regression", "relationship", "variable"],
        "subjects": ["Economics", "Geography", "Mathematics"],
        "tool": "plotly/matplotlib",
        "chart_type": "scatter plot",
        "priority": 7
    },
    "area_chart": {
        "keywords": ["area", "cumulative", "stacked", "trend", "growth"],
        "subjects": ["Economics", "Geography"],
        "tool": "plotly/matplotlib",
        "chart_type": "area chart",
        "priority": 6
    },
    "line_chart": {
        "keywords": ["trend", "time series", "change over time", "growth", "decline"],
        "subjects": ["Economics", "Geography", "Biology"],
        "tool": "plotly/matplotlib",
        "chart_type": "line chart",
        "priority": 7
    },
    "surface_plot": {
        "keywords": ["3d", "surface", "multivariable", "gradient", "mesh"],
        "subjects": ["Further Mathematics", "Physics"],
        "tool": "plotly/matplotlib",
        "chart_type": "3D surface",
        "priority": 5
    },
    "vector_field": {
        "keywords": ["vector", "field", "force", "velocity", "acceleration", "direction"],
        "subjects": ["Physics", "Further Mathematics"],
        "tool": "matplotlib",
        "chart_type": "vector field",
        "priority": 6
    },
    "probability_distribution": {
        "keywords": ["probability", "distribution", "normal", "gaussian", "bell curve", "binomial"],
        "subjects": ["Mathematics", "Further Mathematics"],
        "tool": "scipy/matplotlib",
        "chart_type": "histogram with curve",
        "priority": 8
    }
}


def load_content() -> Dict[str, Any]:
    with CONTENT_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_numerical_data(lesson: Dict[str, Any]) -> Dict[str, Any]:
    """Extract numerical data from lesson content."""
    content = lesson.get("content", "")
    title = lesson.get("title", "")
    full_text = f"{title} {content}"
    
    # Find numerical patterns
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', full_text)
    ranges = re.findall(r'(\d+)\s*(?:to|through|-)\s*(\d+)', full_text)
    coordinates = re.findall(r'\(\s*(\d+)\s*,\s*(\d+)\s*\)', full_text)
    
    return {
        "has_numbers": len(numbers) > 0,
        "number_count": len(numbers),
        "has_ranges": len(ranges) > 0,
        "has_coordinates": len(coordinates) > 0,
        "sample_coordinates": coordinates[:5]
    }


def analyze_lesson(lesson: Dict[str, Any]) -> List[str]:
    """Determine which graphing categories apply to a lesson."""
    categories = []
    
    subject = lesson.get("subject", "").lower()
    title = lesson.get("title", "").lower()
    content = lesson.get("content", "").lower()
    objectives = " ".join(lesson.get("learning_objectives", [])).lower()
    
    full_text = f"{title} {content} {objectives}"
    
    for cat_name, cat_info in GRAPHING_CATEGORIES.items():
        # Check subject match
        subject_match = any(s.lower() in subject for s in cat_info["subjects"])
        
        # Check keyword match
        keyword_match = any(kw in full_text for kw in cat_info["keywords"])
        
        if subject_match and keyword_match:
            categories.append(cat_name)
    
    return categories


def main():
    data = load_content()
    lessons = data.get("content", [])
    
    results = defaultdict(list)
    lesson_graphs = {}
    
    print("\n" + "="*70)
    print("PHASE 2: MATHEMATICAL GRAPHING ENGINE ANALYSIS")
    print("="*70 + "\n")
    
    for lesson in lessons:
        if not isinstance(lesson, dict):
            continue
        
        lesson_id = lesson.get("id", "unknown")
        title = lesson.get("title", "Untitled")
        subject = lesson.get("subject", "Unknown")
        
        categories = analyze_lesson(lesson)
        numerical_data = extract_numerical_data(lesson)
        
        if categories:
            lesson_graphs[lesson_id] = {
                "title": title,
                "subject": subject,
                "categories": categories,
                "priority": max([GRAPHING_CATEGORIES[c]["priority"] for c in categories], default=0),
                "numerical_data": numerical_data,
            }
            
            for cat in categories:
                results[cat].append({
                    "id": lesson_id,
                    "title": title[:60],
                    "subject": subject,
                    "priority": GRAPHING_CATEGORIES[cat]["priority"]
                })
    
    # Print summary
    total_graphable = len(lesson_graphs)
    print(f"📊 {total_graphable} of {len(lessons)} lessons can have auto-generated graphs\n")
    
    for cat_name, lessons_list in sorted(results.items(), 
                                         key=lambda x: -GRAPHING_CATEGORIES[x[0]]["priority"]):
        cat_info = GRAPHING_CATEGORIES[cat_name]
        print(f"🎨 {cat_name.replace('_', ' ').title()}: {len(lessons_list)} lessons")
        print(f"   Tool: {cat_info['tool']}")
        print(f"   Type: {cat_info['chart_type']}")
        print(f"   Priority: {cat_info['priority']}/10")
        print(f"   Top lessons:")
        for lesson in sorted(lessons_list, key=lambda x: -x.get("priority", 0))[:2]:
            print(f"     - {lesson['subject']}: {lesson['title']}")
        print()
    
    # High-priority lessons
    print("="*70)
    print("HIGH-PRIORITY LESSONS (Multiple Graph Types)")
    print("="*70 + "\n")
    
    high_priority = sorted(
        [(lid, info) for lid, info in lesson_graphs.items() if len(info["categories"]) >= 2],
        key=lambda x: -x[1]["priority"]
    )
    
    for lesson_id, info in high_priority[:15]:
        print(f"⭐ {info['subject']}: {info['title'][:50]}")
        print(f"   Categories: {', '.join(info['categories'])}")
        print(f"   Has numerical data: {info['numerical_data']['has_numbers']}")
        print(f"   Priority score: {info['priority']}\n")
    
    # Save detailed report
    report_path = Path("graphable_content_report.json")
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "summary": {
                    "total_lessons": len(lessons),
                    "graphable_lessons": total_graphable,
                    "categories": {k: len(v) for k, v in results.items()},
                },
                "by_category": {k: v for k, v in results.items()},
                "high_priority": [
                    {"id": lid, **info} for lid, info in high_priority
                ],
                "graph_types_summary": {
                    cat: {
                        "count": len(results[cat]),
                        "priority": GRAPHING_CATEGORIES[cat]["priority"],
                        "tool": GRAPHING_CATEGORIES[cat]["tool"],
                        "chart_type": GRAPHING_CATEGORIES[cat]["chart_type"]
                    }
                    for cat in results.keys()
                }
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    
    print(f"📄 Detailed report saved to: {report_path}\n")
    
    # Statistics
    print("="*70)
    print("PHASE 2 STATISTICS")
    print("="*70)
    print(f"Total Graphable Lessons: {total_graphable}")
    print(f"Total Graph Types: {len(results)}")
    print(f"Avg Graphs per Lesson: {sum(len(v) for v in results.values()) / max(total_graphable, 1):.1f}")
    
    # By subject
    print("\nBreakdown by Subject:")
    by_subject = defaultdict(int)
    for item in lesson_graphs.values():
        by_subject[item["subject"]] += 1
    
    for subject in sorted(by_subject.keys()):
        print(f"  {subject:25} {by_subject[subject]:2} lessons")


if __name__ == "__main__":
    main()
