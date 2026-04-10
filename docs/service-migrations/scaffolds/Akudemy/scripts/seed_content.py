#!/usr/bin/env python3
"""
seed_content.py — Akudemy Content Seeding Script

Seeds Akudemy's PostgreSQL database with structured content from:
  a) oumar-code/Aku-Content (textbooks, flashcards, quizzes)
  b) data/exam_papers/ (WAEC/NECO/JAMB + BECE past questions)

This script is the canonical import pipeline for Akudemy.
It replaces the in-memory stub store in app/services/content.py for production use.

Usage:
  # Seed all content from Aku-Content:
  python scripts/seed_content.py --source aku-content --content-dir /path/to/Aku-Content

  # Seed exam papers only:
  python scripts/seed_content.py --source exam-papers --exam-dir data/exam_papers/

  # Seed from local textbook chapters:
  python scripts/seed_content.py --source textbooks --content-dir content/textbooks/

  # Dry run:
  python scripts/seed_content.py --source aku-content --dry-run

  # Reset and reseed (destructive — drops existing content):
  python scripts/seed_content.py --source all --reset

Environment variables:
  DATABASE_URL  — PostgreSQL connection string (required)
  REDIS_URL     — Redis connection string (optional, for cache invalidation)

Dependencies:
  pip install asyncpg pydantic python-dotenv
  (These are already in Akudemy's requirements.txt)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

try:
    import asyncpg
    _ASYNCPG_AVAILABLE = True
except ImportError:
    _ASYNCPG_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DATABASE_URL = os.getenv("DATABASE_URL", "")


# ---------------------------------------------------------------------------
# Content type mappings
# ---------------------------------------------------------------------------

def _infer_content_type(path: Path) -> str:
    name = path.name
    if name.startswith("chapter_"):
        return "textbook_chapter"
    if name.startswith("flashcards_"):
        return "flashcard_deck"
    if name.startswith("quiz_"):
        return "quiz"
    if name == "questions.json":
        return "exam_paper"
    if name.endswith(".md"):
        return "lesson_note"
    return "document"


def _extract_metadata(file_path: Path, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(uuid4()),
        "title": data.get("topic") or data.get("title") or file_path.stem,
        "content_type": _infer_content_type(file_path),
        "subject": data.get("subject", ""),
        "subject_code": data.get("subject_code", ""),
        "class_level": data.get("class_level", ""),
        "chapter": data.get("chapter"),
        "lo_id": data.get("lo_id"),
        "target_exam": data.get("target_exam", ""),
        "language_code": data.get("language", "en"),
        "offline_available": True,
        "tags": _extract_tags(data),
        "source_path": str(file_path),
        "review_status": data.get("review_status", "pending"),
        "size_bytes": file_path.stat().st_size,
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
        "updated_at": datetime.now(tz=timezone.utc).isoformat(),
    }


def _extract_tags(data: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    if data.get("class_level"):
        tags.append(data["class_level"].lower())
    if data.get("subject"):
        tags.append(data["subject"].replace("_", "-"))
    if data.get("target_exam"):
        for part in data["target_exam"].lower().replace(" ", "-").split("/"):
            part = part.strip()
            if part:
                tags.append(part)
    return tags


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def discover_content_files(content_dir: Path, source: str) -> list[Path]:
    files: list[Path] = []

    if source in ("aku-content", "textbooks", "all"):
        files.extend(sorted(content_dir.glob("**/chapter_*.json")))
        files.extend(sorted(content_dir.glob("**/flashcards_*.json")))
        files.extend(sorted(content_dir.glob("**/quiz_*.json")))

    if source in ("exam-papers", "all"):
        files.extend(sorted(content_dir.glob("**/questions.json")))

    return files


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS content_items (
    id              UUID PRIMARY KEY,
    title           TEXT NOT NULL,
    content_type    VARCHAR(50) NOT NULL,
    subject         VARCHAR(100),
    subject_code    VARCHAR(20),
    class_level     VARCHAR(20),
    chapter         INTEGER,
    lo_id           VARCHAR(100),
    target_exam     TEXT,
    language_code   VARCHAR(10) DEFAULT 'en',
    offline_available BOOLEAN DEFAULT TRUE,
    tags            TEXT[],
    source_path     TEXT,
    review_status   VARCHAR(20) DEFAULT 'pending',
    size_bytes      BIGINT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_content_class_level ON content_items(class_level);
CREATE INDEX IF NOT EXISTS idx_content_subject ON content_items(subject);
CREATE INDEX IF NOT EXISTS idx_content_type ON content_items(content_type);
CREATE INDEX IF NOT EXISTS idx_content_lo_id ON content_items(lo_id);
"""

UPSERT_CONTENT_SQL = """
INSERT INTO content_items (
    id, title, content_type, subject, subject_code, class_level, chapter,
    lo_id, target_exam, language_code, offline_available, tags,
    source_path, review_status, size_bytes, created_at, updated_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17
)
ON CONFLICT (id) DO UPDATE SET
    title           = EXCLUDED.title,
    review_status   = EXCLUDED.review_status,
    updated_at      = EXCLUDED.updated_at;
"""


async def seed_to_database(
    items: list[dict[str, Any]],
    dry_run: bool = False,
) -> int:
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable is not set.", file=sys.stderr)
        print("Set it in .env or export it before running this script.", file=sys.stderr)
        sys.exit(1)

    if not _ASYNCPG_AVAILABLE:
        print("ERROR: asyncpg not installed. Run: pip install asyncpg", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        print(f"  [DRY-RUN] Would insert/update {len(items)} items into database")
        return len(items)

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute(CREATE_TABLE_SQL)
        seeded = 0
        for item in items:
            await conn.execute(
                UPSERT_CONTENT_SQL,
                item["id"],
                item["title"],
                item["content_type"],
                item.get("subject"),
                item.get("subject_code"),
                item.get("class_level"),
                item.get("chapter"),
                item.get("lo_id"),
                item.get("target_exam"),
                item.get("language_code", "en"),
                item.get("offline_available", True),
                item.get("tags", []),
                item.get("source_path"),
                item.get("review_status", "pending"),
                item.get("size_bytes"),
                datetime.now(tz=timezone.utc),
                datetime.now(tz=timezone.utc),
            )
            seeded += 1

        print(f"  ✅ Seeded {seeded} items to database")
        return seeded
    finally:
        await conn.close()


# ---------------------------------------------------------------------------
# Main seeding logic
# ---------------------------------------------------------------------------

async def run_seeding(
    source: str,
    content_dir: Path,
    dry_run: bool = False,
    reset: bool = False,
) -> None:
    print("🌱 Aku-Akudemy Content Seeder")
    print(f"   Source     : {source}")
    print(f"   Content dir: {content_dir}")
    print(f"   Dry run    : {dry_run}")
    print(f"   Reset      : {reset}")
    print()

    if not content_dir.exists():
        print(f"ERROR: Content directory '{content_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    files = discover_content_files(content_dir, source)
    print(f"Found {len(files)} content files to process")

    if not files:
        print("No files found. Check your --content-dir and --source arguments.")
        return

    items: list[dict[str, Any]] = []
    errors = 0
    for file_path in files:
        try:
            raw = file_path.read_text(encoding="utf-8")
            data = json.loads(raw) if file_path.suffix == ".json" else {"title": file_path.stem}
            metadata = _extract_metadata(file_path, data)
            items.append(metadata)
            print(f"  ✅ Parsed: {file_path.name}")
        except (json.JSONDecodeError, OSError) as e:
            print(f"  ⚠️  Error parsing {file_path}: {e}", file=sys.stderr)
            errors += 1

    print(f"\n  Parsed {len(items)} items ({errors} errors)")

    seeded = await seed_to_database(items, dry_run=dry_run)

    print(f"\n✅ Seeding complete: {seeded} items {'would be ' if dry_run else ''}seeded")
    if errors:
        print(f"⚠️  {errors} files had parse errors — check the paths above")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Akudemy Content Seeder — imports content from Aku-Content into Akudemy PostgreSQL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--source",
        choices=["aku-content", "textbooks", "exam-papers", "all"],
        default="aku-content",
        help="Content source type (default: aku-content)",
    )
    parser.add_argument(
        "--content-dir",
        default="content",
        help="Path to the content directory (Aku-Content clone or local content/)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing to database")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate the content_items table (destructive)")

    args = parser.parse_args()

    asyncio.run(
        run_seeding(
            source=args.source,
            content_dir=Path(args.content_dir),
            dry_run=args.dry_run,
            reset=args.reset,
        )
    )


if __name__ == "__main__":
    main()
