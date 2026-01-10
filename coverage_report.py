#!/usr/bin/env python3
"""
Compute curriculum coverage against curriculum_map.json using wave3_content_database.json
- Simple fuzzy match between curriculum topic names and content topics/titles by subject
- Reports per-subject coverage and overall
"""

import json
import re
from collections import defaultdict
from pathlib import Path

MAP = Path("curriculum_map.json")
DB = Path("wave3_content_database.json")


def normalize(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tokens(s: str) -> set:
    return set(normalize(s).split())


def similar(a: str, b: str) -> float:
    A, B = tokens(a), tokens(b)
    if not A or not B:
        return 0.0
    inter = len(A & B)
    union = len(A | B)
    return inter / union


def load_map():
    data = json.loads(MAP.read_text(encoding="utf-8"))
    subjects = {}
    for subj, payload in data.get("subjects", {}).items():
        topics = [t.get("name") for t in payload.get("topics", [])]
        subjects[subj] = topics
    return subjects


def load_db():
    data = json.loads(DB.read_text(encoding="utf-8"))
    items = data.get("content", [])
    by_subject = defaultdict(list)
    for it in items:
        by_subject[it.get("subject", "Unknown")].append(it)
    return by_subject


def main():
    subjects_map = load_map()
    db_by_subject = load_db()

    report = {}
    total_topics = 0
    total_matched = 0

    for subject, topics in subjects_map.items():
        total_topics += len(topics)
        items = db_by_subject.get(subject, [])
        matched = []
        unmatched = []
        for t in topics:
            best = 0.0
            best_item = None
            for it in items:
                cand = it.get("topic") or it.get("title")
                score = max(similar(t, cand), similar(cand, t))
                if score > best:
                    best = score
                    best_item = cand
            if best >= 0.5:
                matched.append((t, best_item, round(best, 2)))
            else:
                unmatched.append(t)
        total_matched += len(matched)
        report[subject] = {
            "topics": len(topics),
            "matched": len(matched),
            "coverage_pct": round(100 * len(matched) / max(1, len(topics)), 1),
            "unmatched_topics": unmatched,
        }

    overall = round(100 * total_matched / max(1, total_topics), 1)

    print("\n=== WAEC Curriculum Coverage (from curriculum_map.json) ===")
    print(f"Overall: {total_matched}/{total_topics} topics → {overall}%\n")
    for subj, info in report.items():
        print(f" - {subj}: {info['matched']}/{info['topics']} ({info['coverage_pct']}%)")
    print("\nSubjects with gaps:")
    for subj, info in report.items():
        if info["unmatched_topics"]:
            print(f"\n * {subj}: {len(info['unmatched_topics'])} missing")
            for t in info['unmatched_topics']:
                print(f"    - {t}")
    
    # Return unmatched for programmatic use
    return report


if __name__ == "__main__":
    main()
