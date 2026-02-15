#!/usr/bin/env python3
"""Populate visual.videos for a small batch of lessons using YouTube MCP stub.

Run:
    python add_youtube_suggestions.py --limit 20

Notes:
- Uses youtube_mcp_client.YouTubeMCPClient (stub) to generate mock video entries.
- Only fills lessons where visual.videos is empty or missing.
- Stops after `limit` lessons to validate shape before scaling up.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from youtube_mcp_client import YouTubeMCPClient


CONTENT_PATH = Path("content_data.json")


def load_content(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_content(path: Path, data: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ensure_visual_block(lesson: Dict[str, Any]) -> Dict[str, Any]:
    lo = lesson.get("learning_options")
    if not isinstance(lo, dict):
        lo = {}
        lesson["learning_options"] = lo
    visual = lo.get("visual")
    if not isinstance(visual, dict):
        visual = {}
        lo["visual"] = visual
    visual.setdefault("videos", [])
    return visual


def build_query(lesson: Dict[str, Any]) -> str:
    subject = lesson.get("subject", "")
    topic = lesson.get("topic", "")
    title = lesson.get("title", "")
    return " | ".join([part for part in [subject, topic, title] if part]).strip()


def add_suggestions(limit: int) -> Dict[str, int]:
    if not CONTENT_PATH.exists():
        raise SystemExit(f"Missing {CONTENT_PATH}")

    data = load_content(CONTENT_PATH)
    lessons: List[Dict[str, Any]] = data.get("content", [])

    client = YouTubeMCPClient()
    updated = 0
    processed = 0

    for lesson in lessons:
        if processed >= limit:
            break
        if not isinstance(lesson, dict):
            continue

        visual = ensure_visual_block(lesson)
        videos = visual.get("videos") or []
        if videos:
            continue  # already has videos

        query = build_query(lesson)
        suggestions = client.search_videos(query, limit=3)
        visual["videos"] = suggestions
        visual["video_status"] = "suggested_mcp_stub"

        updated += 1
        processed += 1

    save_content(CONTENT_PATH, data)
    return {"updated": updated, "processed": processed}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20, help="Lessons to update")
    args = parser.parse_args()

    result = add_suggestions(limit=args.limit)
    print(f"Updated videos for {result['updated']} lessons (processed {result['processed']})")


if __name__ == "__main__":
    main()
