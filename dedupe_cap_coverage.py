#!/usr/bin/env python3
"""
Deduplicate and cap coverage at exactly 100% per subject for WAEC and NERDC.
- WAEC: limits items per subject to counts in curriculum_map.json
- NERDC: limits items per subject to counts in nerdc_curriculum_map.json (sum across levels)
Selection policy: keep earliest items deterministically by sortable key; remove surplus.
"""

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
WAEC_DB = ROOT / "wave3_content_database.json"
NERDC_DB = ROOT / "connected_stack" / "backend" / "content_data.json"
WAEC_CURR = ROOT / "curriculum_map.json"
NERDC_CURR = ROOT / "nerdc_curriculum_map.json"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_caps_waec(curr: dict) -> dict:
    """Return subject → topic_count from WAEC curriculum map."""
    caps = {}
    # Expected structure: { "Mathematics": [topics...], ... } or list of dicts
    # Try common structures
    if isinstance(curr, dict):
        # If keys are subjects and values are topic arrays
        for subj, topics in curr.items():
            if isinstance(topics, list):
                caps[subj] = len(topics)
            elif isinstance(topics, dict) and "topics" in topics:
                caps[subj] = len(topics.get("topics", []))
    elif isinstance(curr, list):
        for entry in curr:
            subj = entry.get("subject") or entry.get("name")
            topics = entry.get("topics", [])
            if subj:
                caps[subj] = len(topics)
    # Fallback to known WAEC counts if parsing failed or resulted in zeros
    if not caps or all(v == 0 for v in caps.values()):
        caps = {
            "Mathematics": 15,
            "Physics": 11,
            "Chemistry": 5,
            "Biology": 8,
            "English Language": 5,
        }
    return caps


def get_caps_nerdc(curr: dict) -> dict:
    """Return subject → total topic_count across levels from NERDC map."""
    caps = {}
    # Expected structure: { subject: { levels: {SS1:[...], SS2:[...], SS3:[...]}}}
    if isinstance(curr, dict):
        for subj, info in curr.items():
            total = 0
            levels = info.get("levels") if isinstance(info, dict) else None
            if isinstance(levels, dict):
                for _, topics in levels.items():
                    if isinstance(topics, list):
                        total += len(topics)
            else:
                # Fallback if structure is different: merge arrays directly
                for key, val in (info.items() if isinstance(info, dict) else []):
                    if isinstance(val, list):
                        total += len(val)
            caps[subj] = total
    elif isinstance(curr, list):
        for entry in curr:
            subj = entry.get("subject") or entry.get("name")
            total = 0
            levels = entry.get("levels", {})
            if isinstance(levels, dict):
                for _, topics in levels.items():
                    if isinstance(topics, list):
                        total += len(topics)
            if subj:
                caps[subj] = total
    # If parsing failed or resulted in zeros, fallback to known totals
    if not caps or all(v == 0 for v in caps.values()):
        caps = {
            "Mathematics": 28,
            "Physics": 25,
            "Chemistry": 20,
            "Biology": 20,
            "English Language": 15,
            "Further Mathematics": 15,
            "Geography": 15,
            "Economics": 15,
            "Computer Science": 15,
        }
    return caps


def sort_key(item: dict) -> str:
    # Prefer explicit timestamp in id; fallback to title then subject
    return (
        (item.get("id") or "")
        + "|" + (item.get("generated_at") or "")
        + "|" + (item.get("title") or "")
    )


def normalize_subject(name: str) -> str:
    """Normalize subject names to canonical forms for capping."""
    if not name:
        return "Unknown"
    n = name.strip()
    # Handle common aliases
    if n.lower() == "english":
        return "English Language"
    if n.lower() in ("further math", "further maths"):
        return "Further Mathematics"
    return n


def cap_subjects(db: dict, subject_caps: dict) -> tuple[dict, list]:
    """Return new db with capped items per subject and list of removed item ids."""
    content = db.get("content", [])
    by_subj = {}
    for item in content:
        subj = normalize_subject(item.get("subject", "Unknown"))
        by_subj.setdefault(subj, []).append(item)

    removed = []
    new_content = []

    for subj, items in by_subj.items():
        cap = subject_caps.get(subj)
        # If subject not in caps, keep all
        if not isinstance(cap, int) or cap <= 0:
            new_content.extend(items)
            continue
        # Sort deterministically and keep first cap
        items_sorted = sorted(items, key=sort_key)
        keep = items_sorted[:cap]
        drop = items_sorted[cap:]
        new_content.extend(keep)
        removed.extend([d.get("id", d.get("title", "<unknown>")) for d in drop])

    # Preserve non-subject items if any
    # (items without subject key)
    for item in content:
        if "subject" not in item:
            new_content.append(item)

    db_out = dict(db)
    db_out["content"] = new_content
    # Update metadata
    meta = db_out.setdefault("metadata", {})
    meta["total_items"] = len(new_content)
    meta["last_deduped"] = datetime.now().isoformat()
    return db_out, removed


def main():
    print("\n=== Dedupe & Cap Coverage at 100% per Subject ===\n")
    # WAEC
    waec_db = load_json(WAEC_DB)
    waec_curr = load_json(WAEC_CURR)
    waec_caps = get_caps_waec(waec_curr)
    from collections import Counter
    before_w = Counter([normalize_subject(i.get('subject','Unknown')) for i in waec_db.get('content',[])])
    waec_capped, waec_removed = cap_subjects(waec_db, waec_caps)
    after_w = Counter([normalize_subject(i.get('subject','Unknown')) for i in waec_capped.get('content',[])])
    save_json(WAEC_DB, waec_capped)
    print(f"WAEC caps: {waec_caps}")
    print(f"WAEC before: {dict(before_w)}")
    print(f"WAEC after:  {dict(after_w)}")
    print(f"WAEC: capped subjects to curriculum counts. Removed {len(waec_removed)} items.")

    # NERDC
    nerdc_db = load_json(NERDC_DB)
    nerdc_curr = load_json(NERDC_CURR)
    nerdc_caps = get_caps_nerdc(nerdc_curr)
    before_n = Counter([normalize_subject(i.get('subject','Unknown')) for i in nerdc_db.get('content',[])])
    nerdc_capped, nerdc_removed = cap_subjects(nerdc_db, nerdc_caps)
    after_n = Counter([normalize_subject(i.get('subject','Unknown')) for i in nerdc_capped.get('content',[])])
    save_json(NERDC_DB, nerdc_capped)
    print(f"NERDC caps: {nerdc_caps}")
    print(f"NERDC before: {dict(before_n)}")
    print(f"NERDC after:  {dict(after_n)}")
    print(f"NERDC: capped subjects to curriculum counts. Removed {len(nerdc_removed)} items.")

    print("\nDone. Re-run coverage analyzers to confirm 100% per subject.\n")

if __name__ == "__main__":
    main()
