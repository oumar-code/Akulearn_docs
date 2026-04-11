#!/usr/bin/env python3
"""
flashcard_generator.py — Aku Platform Content Pipeline

Generates flashcard decks from textbook chapter JSON files produced by
textbook_generator.py.

For each chapter JSON, produces:
  content/flashcards/<class_level>/<subject_code>/flashcards_chapter_<N>.json

Flashcard JSON format (compatible with Anki, SuperMemo, and AkuTutor):
  {
    "lo_id": "LO:NERDC:MAT:JSS1:T1:001",
    "class_level": "JSS1",
    "subject": "mathematics",
    "chapter": 1,
    "topic": "Place Value and Whole Numbers",
    "cards": [
      {
        "id": "card_001",
        "front": "What does the digit 4 represent in 4,523?",
        "back": "4,000 — four thousands",
        "difficulty": "easy",
        "lo_id": "LO:NERDC:MAT:JSS1:T1:001",
        "tags": ["place_value", "jss1", "mathematics"]
      },
      ...
    ]
  }

Usage:
  python pipeline/flashcard_generator.py \\
      --input-dir content/textbooks/jss1/mathematics \\
      --output-dir content/flashcards/

  python pipeline/flashcard_generator.py --all --input-dir content/textbooks/ \\
      --output-dir content/flashcards/

  # Dry run:
  python pipeline/flashcard_generator.py --all --dry-run

Dependencies:
  pip install openai pydantic   (same as textbook_generator)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False


SYSTEM_PROMPT = (
    "You are an expert Nigerian secondary school teacher creating flashcards "
    "to help students memorise key facts, definitions and formulas. "
    "Flashcard fronts must be concise questions or prompts. "
    "Flashcard backs must be short, memorable answers. "
    "Use Nigerian examples and SI units where relevant."
)


def build_flashcard_prompt(chapter_json: dict[str, Any]) -> str:
    topic = chapter_json.get("topic", "Unknown topic")
    subject = chapter_json.get("subject", "").replace("_", " ").title()
    class_level = chapter_json.get("class_level", "")
    md_content = chapter_json.get("content_md", "")

    # Truncate content to stay within context window
    truncated = md_content[:6000] if len(md_content) > 6000 else md_content

    return f"""Based on this {class_level} {subject} chapter on "{topic}", create exactly 15 flashcards.

Each flashcard must have:
- "front": a concise question or prompt (max 20 words)
- "back": a short, memorable answer (max 40 words)
- "difficulty": one of "easy", "medium", or "hard"
- "tags": a list of 2–4 relevant topic tags (lowercase, underscored)

Mix difficulties: 5 easy, 7 medium, 3 hard.
Focus on: definitions, formulas, key facts, common mistakes, and classification questions.

Return ONLY a valid JSON array of 15 flashcard objects. No markdown, no extra text.

Chapter content (excerpt):
---
{truncated}
---
"""


class FlashcardGenerator:
    def __init__(
        self,
        api_base: str = "http://localhost:8004/v1",
        api_key: str = "local",
        model: str = "llama-3",
        output_dir: Path = Path("content/flashcards"),
        dry_run: bool = False,
    ) -> None:
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.model = model

        if not dry_run and _OPENAI_AVAILABLE:
            self.client: OpenAI | None = OpenAI(base_url=api_base, api_key=api_key)
        else:
            self.client = None

    def _generate_cards_for_chapter(self, chapter_json: dict[str, Any]) -> list[dict[str, Any]]:
        if self.dry_run:
            return [
                {
                    "id": f"card_{i+1:03d}",
                    "front": f"[DRY-RUN] Question {i+1} for {chapter_json.get('topic')}",
                    "back": "[DRY-RUN] Answer",
                    "difficulty": "easy",
                    "lo_id": chapter_json.get("lo_id", ""),
                    "tags": ["dry_run"],
                }
                for i in range(5)
            ]

        if self.client is None:
            print("ERROR: openai package not installed. Run: pip install openai", file=sys.stderr)
            sys.exit(1)

        prompt = build_flashcard_prompt(chapter_json)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=2048,
        )
        raw = response.choices[0].message.content or "[]"

        try:
            cards_raw: list[dict[str, Any]] = json.loads(raw)
        except json.JSONDecodeError:
            print(f"  ⚠️  JSON parse error for {chapter_json.get('topic')}; using empty card list", file=sys.stderr)
            return []

        lo_id = chapter_json.get("lo_id", "")
        for i, card in enumerate(cards_raw):
            card["id"] = f"card_{i+1:03d}"
            card.setdefault("lo_id", lo_id)

        return cards_raw

    def process_chapter_file(self, chapter_file: Path) -> Path | None:
        chapter_json: dict[str, Any] = json.loads(chapter_file.read_text(encoding="utf-8"))

        class_level = chapter_json.get("class_level", "UNKNOWN").lower()
        subject = chapter_json.get("subject", "unknown")
        subject_code = chapter_json.get("subject_code", "UNK")
        chapter_num = chapter_json.get("chapter", 0)
        topic = chapter_json.get("topic", "")

        print(f"  📇 Flashcards: {class_level}/{subject}/chapter_{chapter_num:02d} — {topic}")

        cards = self._generate_cards_for_chapter(chapter_json)

        deck: dict[str, Any] = {
            "lo_id": chapter_json.get("lo_id", ""),
            "class_level": chapter_json.get("class_level", ""),
            "subject": subject,
            "subject_code": subject_code,
            "chapter": chapter_num,
            "topic": topic,
            "language": "en",
            "card_count": len(cards),
            "generated_at": datetime.now(tz=timezone.utc).isoformat(),
            "generator_version": "1.0.0",
            "review_status": "pending",
            "cards": cards,
        }

        out_dir = self.output_dir / class_level / subject
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"flashcards_chapter_{chapter_num:02d}.json"

        if not self.dry_run:
            out_path.write_text(json.dumps(deck, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"    ✅ Written: {out_path} ({len(cards)} cards)")
        else:
            print(f"    [DRY-RUN] Would write: {out_path}")

        return out_path

    def run_directory(self, input_dir: Path) -> list[Path]:
        chapter_files = sorted(input_dir.glob("**/chapter_*.json"))
        if not chapter_files:
            print(f"No chapter JSON files found in {input_dir}")
            return []

        written: list[Path] = []
        for cf in chapter_files:
            result = self.process_chapter_file(cf)
            if result:
                written.append(result)

        return written


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aku Platform Flashcard Generator — auto-generates from textbook chapters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input-dir", required=True, help="Directory containing chapter_*.json files")
    parser.add_argument("--output-dir", default="content/flashcards", help="Output directory for flashcard decks")
    parser.add_argument("--api-base", default=os.getenv("AKUAI_API_BASE", "http://localhost:8004/v1"))
    parser.add_argument("--api-key", default=os.getenv("AKUAI_API_KEY", "local"))
    parser.add_argument("--model", default=os.getenv("AKUAI_MODEL", "llama-3"))
    parser.add_argument("--all", action="store_true", dest="all_chapters", help="Process all chapter JSON files recursively")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    gen = FlashcardGenerator(
        api_base=args.api_base,
        api_key=args.api_key,
        model=args.model,
        output_dir=Path(args.output_dir),
        dry_run=args.dry_run,
    )

    input_path = Path(args.input_dir)
    if not input_path.exists():
        print(f"ERROR: {input_path} does not exist", file=sys.stderr)
        sys.exit(1)

    written = gen.run_directory(input_path)
    print(f"\n✅ Done. {len(written)} flashcard deck(s) {'would be ' if args.dry_run else ''}written.")


if __name__ == "__main__":
    main()
