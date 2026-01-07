#!/usr/bin/env python3
"""
Analyze NERDC curriculum coverage from connected_stack/backend/content_data.json
against nerdc_curriculum_map.json
"""

import json
from pathlib import Path

MAP = Path("nerdc_curriculum_map.json")
BACKEND_DB = Path("connected_stack/backend/content_data.json")


def normalize(s):
    return (s or "").lower().replace(" ", "").replace("-", "")


def tokens(s):
    return set(normalize(s).split())


def similarity(a, b):
    A, B = tokens(a), tokens(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def main():
    # Load map
    map_data = json.loads(MAP.read_text(encoding="utf-8"))
    
    # Load backend
    backend_data = json.loads(BACKEND_DB.read_text(encoding="utf-8"))
    items = backend_data.get("content", [])
    
    # Group by subject
    by_subject = {}
    for item in items:
        subj = item.get("subject", "Unknown")
        if subj not in by_subject:
            by_subject[subj] = []
        by_subject[subj].append(item)
    
    print("\n=== NERDC CURRICULUM COVERAGE ANALYSIS ===\n")
    
    total_topics = 0
    total_covered = 0
    gaps_by_subject = {}
    
    for subject, levels_data in map_data.get("subjects", {}).items():
        all_topics = []
        for level in ["SS1", "SS2", "SS3"]:
            all_topics.extend(levels_data.get(level, []))
        
        total_topics += len(all_topics)
        items_for_subject = by_subject.get(subject, [])
        
        covered = len(items_for_subject)
        total_covered += covered
        coverage_pct = round(100 * covered / max(1, len(all_topics)), 1)
        
        print(f"{subject}:")
        print(f"  Topics in curriculum: {len(all_topics)}")
        print(f"  Generated items: {covered}")
        print(f"  Coverage: {coverage_pct}%")
        
        if covered < len(all_topics):
            gaps_by_subject[subject] = {
                "total": len(all_topics),
                "covered": covered,
                "missing": len(all_topics) - covered,
                "topics": all_topics[:5]  # Show first 5
            }
            print(f"  Missing: {gaps_by_subject[subject]['missing']} topics")
        
        print()
    
    overall = round(100 * total_covered / max(1, total_topics), 1)
    print(f"OVERALL: {total_covered}/{total_topics} topics → {overall}% coverage\n")
    
    if gaps_by_subject:
        print(f"Subjects needing more content:")
        for subj in sorted(gaps_by_subject.keys(), key=lambda x: -gaps_by_subject[x]["missing"]):
            gap = gaps_by_subject[subj]
            print(f"  - {subj}: {gap['missing']} more needed (have {gap['covered']}/{gap['total']})")
    else:
        print("✅ 100% NERDC coverage achieved!")


if __name__ == "__main__":
    main()
