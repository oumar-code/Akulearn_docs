#!/usr/bin/env python3
"""Enrich lessons with structured learning options and build a visual queue.

Actions:
- Ensure each lesson in content_data.json has learning_options for reading/writing,
  visual, auditory, kinesthetic, and assessment.
- Queue lessons that lack an image in visual_queue.json for later rendering.
- Leave existing fields intact; only fill missing pieces.

Run:
    python enrich_learning_options.py

Outputs:
    content_data.json (updated in place)
    visual_queue.json (new queue file)
"""

import json
import time
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Any


CONTENT_PATH = Path("content_data.json")
VISUAL_QUEUE_PATH = Path("visual_queue.json")


def load_content(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_content(path: Path, data: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_prompt(lesson: Dict[str, Any]) -> str:
    subject = lesson.get("subject", "Lesson")
    topic = lesson.get("topic", lesson.get("title", ""))
    title = lesson.get("title", topic)
    return (
        f"Create an educational illustration for a Nigerian secondary school lesson. "
        f"Subject: {subject}. Topic: {topic}. Lesson: {title}. "
        "Style: clear, bright, student-friendly, high-contrast labels."
    )


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def merge_learning_options(lesson: Dict[str, Any]) -> Dict[str, Any]:
    existing = deepcopy(lesson.get("learning_options", {}))

    def ensure_block(name: str) -> Dict[str, Any]:
        blk = existing.get(name) or {}
        if not isinstance(blk, dict):
            blk = {}
        existing[name] = blk
        return blk

    # Reading/Writing
    rw = ensure_block("reading_writing")
    rw.setdefault(
        "summary",
        f"Summarize the key ideas of '{lesson.get('title', 'this lesson')}' in simple steps."
    )
    rw.setdefault("worksheet", ["List three key ideas", "Write two examples from daily life"])

    # Visual
    visual = ensure_block("visual")
    visual.setdefault("image", None)
    visual.setdefault("videos", [])
    visual.setdefault("slides", None)
    visual.setdefault("video_status", "pending_mcp")
    visual.setdefault("image_status", "queued")

    # Auditory
    aud = ensure_block("auditory")
    aud.setdefault("audio_summary", None)
    aud.setdefault("podcast", None)

    # Kinesthetic
    kin = ensure_block("kinesthetic")
    kin.setdefault("activity", "Hands-on demonstration of the concept using simple materials.")
    kin.setdefault("materials", ["Paper", "Pen", "Household items"])
    kin.setdefault("steps", ["Set up materials", "Perform the demonstration", "Reflect on the outcome"])
    kin.setdefault("duration_minutes", 15)

    # Assessment
    assess = ensure_block("assessment")
    assess.setdefault("checks", ["Explain the concept in your own words", "Give one real-world example"])
    assess.setdefault("exit_ticket", "List one thing you learned and one question you still have.")

    return existing


def main() -> None:
    if not CONTENT_PATH.exists():
        raise SystemExit(f"Missing {CONTENT_PATH}")

    data = load_content(CONTENT_PATH)
    lessons = data.get("content", [])

    visual_queue: List[Dict[str, Any]] = []
    touched = 0

    for lesson in lessons:
        if not isinstance(lesson, dict):
            continue

        merged = merge_learning_options(lesson)
        lesson["learning_options"] = merged
        touched += 1

        # Queue visuals if no image present
        visual = merged.get("visual", {})
        image = visual.get("image")
        if image in (None, "", False):
            visual_queue.append(
                {
                    "id": lesson.get("id"),
                    "subject": lesson.get("subject"),
                    "topic": lesson.get("topic"),
                    "title": lesson.get("title"),
                    "prompt": build_prompt(lesson),
                    "target_file": f"lesson_images_gemini/{lesson.get('id', 'lesson')}.json",
                    "status": "queued",
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                }
            )

    save_content(CONTENT_PATH, data)

    VISUAL_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with VISUAL_QUEUE_PATH.open("w", encoding="utf-8") as f:
        json.dump({"queued": visual_queue, "total": len(visual_queue)}, f, ensure_ascii=False, indent=2)

    print(f"Enriched {touched} lessons")
    print(f"Queued {len(visual_queue)} visuals -> {VISUAL_QUEUE_PATH}")


if __name__ == "__main__":
    main()
