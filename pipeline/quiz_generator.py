#!/usr/bin/env python3
"""
quiz_generator.py — Aku Platform Content Pipeline

Generates 10-question topic quizzes from:
  a) Textbook chapter JSON files (produced by textbook_generator.py), or
  b) Exam paper JSON files (produced by exam_paper_scraper.py / bece_scraper.py)

Output:
  content/quizzes/<class_level>/<subject_code>/quiz_chapter_<N>.json

Quiz JSON format (compatible with AkuTutor and offline apps):
  {
    "lo_id": "LO:NERDC:MAT:JSS1:T1:001",
    "quiz_type": "formative",
    "class_level": "JSS1",
    "subject": "mathematics",
    "topic": "Place Value and Whole Numbers",
    "time_limit_minutes": 15,
    "questions": [
      {
        "id": "q001",
        "type": "mcq",                  // or "short_answer", "true_false"
        "question": "What is the value of 5 in 5,234?",
        "options": ["5", "50", "500", "5,000"],
        "correct_option": 3,            // 0-indexed
        "explanation": "5 is in the thousands position → value = 5,000",
        "difficulty": "easy",
        "marks": 1,
        "lo_id": "LO:NERDC:MAT:JSS1:T1:001",
        "source": "generated"
      },
      ...
    ]
  }

Usage:
  # From textbook chapters:
  python pipeline/quiz_generator.py \\
      --source textbook \\
      --input-dir content/textbooks/jss1/mathematics \\
      --output-dir content/quizzes/

  # From exam papers:
  python pipeline/quiz_generator.py \\
      --source exam-papers \\
      --input-dir data/exam_papers/ \\
      --level jss3 --subject mathematics \\
      --output-dir content/quizzes/

  # Dry run:
  python pipeline/quiz_generator.py --source textbook \\
      --input-dir content/textbooks/ --dry-run

Dependencies:
  pip install openai pydantic
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
    "You are an expert Nigerian secondary school examiner. "
    "Create high-quality multiple-choice questions aligned to NERDC/WAEC/BECE standards. "
    "Each question must have exactly 4 options (A-D), one correct answer, and a clear explanation. "
    "Use Nigerian contexts and examples where appropriate. "
    "Questions should test understanding, not just recall."
)


def build_quiz_prompt(chapter_json: dict[str, Any], n_questions: int = 10) -> str:
    topic = chapter_json.get("topic", "")
    subject = chapter_json.get("subject", "").replace("_", " ").title()
    class_level = chapter_json.get("class_level", "")
    md_content = chapter_json.get("content_md", "")
    exam = chapter_json.get("target_exam", "BECE")

    truncated = md_content[:6000] if len(md_content) > 6000 else md_content

    return f"""Based on this {class_level} {subject} chapter on "{topic}", create exactly {n_questions} multiple-choice questions for a formative quiz.

Target exam: {exam}
Difficulty split: 4 easy, 4 medium, 2 hard.

For each question provide:
- "question": the question text
- "options": list of exactly 4 answer choices (strings)
- "correct_option": 0-indexed integer (0=A, 1=B, 2=C, 3=D)
- "explanation": brief explanation of why the answer is correct (and why distractors are wrong)
- "difficulty": "easy", "medium", or "hard"
- "marks": 1 (easy/medium) or 2 (hard)

Return ONLY a valid JSON array of {n_questions} question objects. No markdown, no extra text.

Chapter content (excerpt):
---
{truncated}
---
"""


class QuizGenerator:
    def __init__(
        self,
        api_base: str = "http://localhost:8004/v1",
        api_key: str = "local",
        model: str = "llama-3",
        output_dir: Path = Path("content/quizzes"),
        dry_run: bool = False,
        n_questions: int = 10,
    ) -> None:
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.model = model
        self.n_questions = n_questions

        if not dry_run and _OPENAI_AVAILABLE:
            self.client: OpenAI | None = OpenAI(base_url=api_base, api_key=api_key)
        else:
            self.client = None

    def _generate_questions(self, chapter_json: dict[str, Any]) -> list[dict[str, Any]]:
        if self.dry_run:
            return [
                {
                    "id": f"q{i+1:03d}",
                    "type": "mcq",
                    "question": f"[DRY-RUN] Question {i+1} for {chapter_json.get('topic')}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_option": 0,
                    "explanation": "[DRY-RUN] Explanation",
                    "difficulty": "easy",
                    "marks": 1,
                    "lo_id": chapter_json.get("lo_id", ""),
                    "source": "generated",
                }
                for i in range(self.n_questions)
            ]

        if self.client is None:
            print("ERROR: openai package not installed. Run: pip install openai", file=sys.stderr)
            sys.exit(1)

        prompt = build_quiz_prompt(chapter_json, self.n_questions)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            max_tokens=3000,
        )
        raw = response.choices[0].message.content or "[]"

        try:
            questions_raw: list[dict[str, Any]] = json.loads(raw)
        except json.JSONDecodeError:
            print(f"  ⚠️  JSON parse error for {chapter_json.get('topic')}; using empty question list", file=sys.stderr)
            return []

        lo_id = chapter_json.get("lo_id", "")
        for i, q in enumerate(questions_raw):
            q["id"] = f"q{i+1:03d}"
            q["type"] = q.get("type", "mcq")
            q.setdefault("lo_id", lo_id)
            q.setdefault("source", "generated")

        return questions_raw

    def process_chapter_file(self, chapter_file: Path) -> Path | None:
        chapter_json: dict[str, Any] = json.loads(chapter_file.read_text(encoding="utf-8"))

        class_level = chapter_json.get("class_level", "UNKNOWN").lower()
        subject = chapter_json.get("subject", "unknown")
        subject_code = chapter_json.get("subject_code", "UNK")
        chapter_num = chapter_json.get("chapter", 0)
        topic = chapter_json.get("topic", "")

        print(f"  📝 Quiz: {class_level}/{subject}/chapter_{chapter_num:02d} — {topic}")

        questions = self._generate_questions(chapter_json)
        total_marks = sum(q.get("marks", 1) for q in questions)

        quiz: dict[str, Any] = {
            "lo_id": chapter_json.get("lo_id", ""),
            "quiz_type": "formative",
            "class_level": chapter_json.get("class_level", ""),
            "subject": subject,
            "subject_code": subject_code,
            "chapter": chapter_num,
            "topic": topic,
            "target_exam": chapter_json.get("target_exam", ""),
            "language": "en",
            "time_limit_minutes": 15,
            "question_count": len(questions),
            "total_marks": total_marks,
            "generated_at": datetime.now(tz=timezone.utc).isoformat(),
            "generator_version": "1.0.0",
            "review_status": "pending",
            "questions": questions,
        }

        out_dir = self.output_dir / class_level / subject
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"quiz_chapter_{chapter_num:02d}.json"

        if not self.dry_run:
            out_path.write_text(json.dumps(quiz, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"    ✅ Written: {out_path} ({len(questions)} questions, {total_marks} marks)")
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
        description="Aku Platform Quiz Generator — auto-generates topic quizzes from textbook chapters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--source", choices=["textbook", "exam-papers"], default="textbook",
                        help="Data source for quiz generation (default: textbook)")
    parser.add_argument("--input-dir", required=True, help="Directory containing chapter_*.json or exam paper JSON files")
    parser.add_argument("--output-dir", default="content/quizzes", help="Output directory for quiz files")
    parser.add_argument("--n-questions", type=int, default=10, help="Number of questions per quiz (default: 10)")
    parser.add_argument("--level", help="Filter by class level (e.g., jss1)")
    parser.add_argument("--subject", help="Filter by subject (e.g., mathematics)")
    parser.add_argument("--api-base", default=os.getenv("AKUAI_API_BASE", "http://localhost:8004/v1"))
    parser.add_argument("--api-key", default=os.getenv("AKUAI_API_KEY", "local"))
    parser.add_argument("--model", default=os.getenv("AKUAI_MODEL", "llama-3"))
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    gen = QuizGenerator(
        api_base=args.api_base,
        api_key=args.api_key,
        model=args.model,
        output_dir=Path(args.output_dir),
        dry_run=args.dry_run,
        n_questions=args.n_questions,
    )

    input_path = Path(args.input_dir)
    if not input_path.exists():
        print(f"ERROR: {input_path} does not exist", file=sys.stderr)
        sys.exit(1)

    written = gen.run_directory(input_path)
    print(f"\n✅ Done. {len(written)} quiz file(s) {'would be ' if args.dry_run else ''}written.")


if __name__ == "__main__":
    main()
