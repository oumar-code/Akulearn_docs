#!/usr/bin/env python3
"""Normalize WAEC subjects: map 'English' → 'English Language' and drop non-WAEC subjects."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
WAEC_DB = ROOT / "wave3_content_database.json"

WAEC_SUBJECTS = {"Mathematics", "Physics", "Chemistry", "Biology", "English Language"}

with open(WAEC_DB, "r", encoding="utf-8") as f:
    db = json.load(f)

normalized = []
removed = []
for item in db.get("content", []):
    subj = item.get("subject", "Unknown")
    if subj == "English":
        item["subject"] = "English Language"
        subj = item["subject"]
    if subj in WAEC_SUBJECTS:
        normalized.append(item)
    else:
        removed.append(item.get("id", item.get("title", "<unknown>")))

print(f"Normalized {len(normalized)} items; removed {len(removed)} non-WAEC items.")

# Save back
db["content"] = normalized
# Update metadata
meta = db.setdefault("metadata", {})
meta["total_items"] = len(normalized)

with open(WAEC_DB, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
