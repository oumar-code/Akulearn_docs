#!/usr/bin/env python3
"""
Build a queued list of NERDC content items to generate images for.
Does not call any image API. Safe to run on free tier.
Outputs: image_queue/nerdc_queue.json
"""

import json
from pathlib import Path
from datetime import datetime

BACKEND_CONTENT = Path("connected_stack/backend/content_data.json")
QUEUE_DIR = Path("image_queue")
QUEUE_FILE = QUEUE_DIR / "nerdc_queue.json"

SUBJECTS = {"Mathematics","Physics","Chemistry","Biology","English Language",
            "Further Mathematics","Geography","Economics","Computer Science"}

def build_prompt(item):
    title = item.get("title","Lesson")
    subject = item.get("subject","General")
    level = item.get("level","SS")
    return (
        f"Educational diagram showing {title} for NERDC {subject} {level}, "
        f"clear labels, classroom suitable, high contrast, informative"
    )

def main():
    QUEUE_DIR.mkdir(exist_ok=True)

    with BACKEND_CONTENT.open("r", encoding="utf-8") as f:
        data = json.load(f)

    existing = []
    if QUEUE_FILE.exists():
        try:
            existing = json.load(QUEUE_FILE.open("r", encoding="utf-8"))
        except Exception:
            existing = []
    existing_ids = {x.get("id") for x in existing}

    queue = []
    for item in data.get("content", []):
        if item.get("subject") not in SUBJECTS:
            continue
        if item.get("curriculum_framework","NERDC").lower().find("nerdc") == -1:
            continue
        if item.get("image"):
            continue
        if item.get("id") in existing_ids:
            continue
        prompt = build_prompt(item)
        queue.append({
            "id": item.get("id"),
            "subject": item.get("subject"),
            "title": item.get("title"),
            "level": item.get("level"),
            "prompt": prompt,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        })

    # Merge with existing and save
    merged = existing + queue
    with QUEUE_FILE.open("w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"Queued {len(queue)} new NERDC items (total in queue: {len(merged)})")

if __name__ == "__main__":
    main()
