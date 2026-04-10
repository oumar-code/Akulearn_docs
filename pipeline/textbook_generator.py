#!/usr/bin/env python3
"""
textbook_generator.py — Aku Platform Content Pipeline

Generates structured textbook chapter bundles (JSON + Markdown) for
JSS1–SS3 subjects aligned to the NERDC/WAEC curriculum.

The generator can use:
  - A local/API LLM (AkuAI / LLaMA) via OpenAI-compatible API
  - OpenAI / Anthropic API (for speed during initial seeding)

Output per chapter:
  content/textbooks/<class_level>/<subject_code>/chapter_<N>.json
  content/textbooks/<class_level>/<subject_code>/chapter_<N>.md

Each chapter JSON is tagged with LO IDs following docs/LO_TAGGING_SCHEMA.md.

Usage:
  python pipeline/textbook_generator.py \\
      --level jss1 --subject mathematics --term 1 \\
      --api-base http://localhost:8004/v1 \\
      --output-dir content/textbooks/

  # Generate all JSS levels and P1 subjects:
  python pipeline/textbook_generator.py --all-jss --output-dir content/textbooks/

  # Dry run (print prompts without calling LLM):
  python pipeline/textbook_generator.py --level ss1 --subject biology --dry-run

Dependencies:
  pip install openai pydantic
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False

# ---------------------------------------------------------------------------
# Curriculum map — NERDC JSS1–SS3
# Priority: P1 = compulsory core; P2 = compulsory elective; P3 = optional
# ---------------------------------------------------------------------------

CURRICULUM: dict[str, dict[str, Any]] = {
    "jss1": {
        "subjects": {
            "mathematics":      {"code": "MAT", "priority": "P1", "terms": 3},
            "english_language": {"code": "ENG", "priority": "P1", "terms": 3},
            "basic_science":    {"code": "BSC", "priority": "P1", "terms": 3},
            "social_studies":   {"code": "SST", "priority": "P2", "terms": 3},
            "basic_technology": {"code": "BTH", "priority": "P2", "terms": 3},
            "civic_education":  {"code": "CIV", "priority": "P2", "terms": 3},
            "agricultural_science": {"code": "AGR", "priority": "P3", "terms": 3},
            "home_economics":   {"code": "HEC", "priority": "P3", "terms": 3},
            "french":           {"code": "FRN", "priority": "P3", "terms": 3},
        },
        "exam": "BECE / National Assessment",
    },
    "jss2": {
        "subjects": {
            "mathematics":      {"code": "MAT", "priority": "P1", "terms": 3},
            "english_language": {"code": "ENG", "priority": "P1", "terms": 3},
            "basic_science":    {"code": "BSC", "priority": "P1", "terms": 3},
            "social_studies":   {"code": "SST", "priority": "P2", "terms": 3},
            "basic_technology": {"code": "BTH", "priority": "P2", "terms": 3},
            "civic_education":  {"code": "CIV", "priority": "P2", "terms": 3},
            "agricultural_science": {"code": "AGR", "priority": "P3", "terms": 3},
            "home_economics":   {"code": "HEC", "priority": "P3", "terms": 3},
        },
        "exam": "BECE / National Assessment",
    },
    "jss3": {
        "subjects": {
            "mathematics":      {"code": "MAT", "priority": "P1", "terms": 3},
            "english_language": {"code": "ENG", "priority": "P1", "terms": 3},
            "basic_science":    {"code": "BSC", "priority": "P1", "terms": 3},
            "social_studies":   {"code": "SST", "priority": "P2", "terms": 3},
            "basic_technology": {"code": "BTH", "priority": "P2", "terms": 3},
            "civic_education":  {"code": "CIV", "priority": "P2", "terms": 3},
        },
        "exam": "BECE / Common Entrance",
    },
    "ss1": {
        "subjects": {
            "mathematics":      {"code": "MAT", "priority": "P1", "terms": 3},
            "english_language": {"code": "ENG", "priority": "P1", "terms": 3},
            "physics":          {"code": "PHY", "priority": "P1", "terms": 3},
            "chemistry":        {"code": "CHE", "priority": "P1", "terms": 3},
            "biology":          {"code": "BIO", "priority": "P1", "terms": 3},
            "economics":        {"code": "ECO", "priority": "P2", "terms": 3},
            "government":       {"code": "GOV", "priority": "P2", "terms": 3},
            "geography":        {"code": "GEO", "priority": "P2", "terms": 3},
            "further_mathematics": {"code": "FMA", "priority": "P3", "terms": 3},
            "accounts":         {"code": "ACC", "priority": "P3", "terms": 3},
            "commerce":         {"code": "COM", "priority": "P3", "terms": 3},
        },
        "exam": "WAEC / NECO / JAMB",
    },
    "ss2": {
        "subjects": {
            "mathematics":      {"code": "MAT", "priority": "P1", "terms": 3},
            "english_language": {"code": "ENG", "priority": "P1", "terms": 3},
            "physics":          {"code": "PHY", "priority": "P1", "terms": 3},
            "chemistry":        {"code": "CHE", "priority": "P1", "terms": 3},
            "biology":          {"code": "BIO", "priority": "P1", "terms": 3},
            "economics":        {"code": "ECO", "priority": "P2", "terms": 3},
            "government":       {"code": "GOV", "priority": "P2", "terms": 3},
            "geography":        {"code": "GEO", "priority": "P2", "terms": 3},
        },
        "exam": "WAEC / NECO / JAMB",
    },
    "ss3": {
        "subjects": {
            "mathematics":      {"code": "MAT", "priority": "P1", "terms": 3},
            "english_language": {"code": "ENG", "priority": "P1", "terms": 3},
            "physics":          {"code": "PHY", "priority": "P1", "terms": 3},
            "chemistry":        {"code": "CHE", "priority": "P1", "terms": 3},
            "biology":          {"code": "BIO", "priority": "P1", "terms": 3},
            "economics":        {"code": "ECO", "priority": "P2", "terms": 3},
            "government":       {"code": "GOV", "priority": "P2", "terms": 3},
        },
        "exam": "WAEC / NECO / JAMB",
    },
}

# Topics per class+subject (Term 1, Chapter 1) — extend as needed
CHAPTER_TOPICS: dict[str, dict[str, list[str]]] = {
    "jss1": {
        "mathematics": [
            "Place Value and Whole Numbers",
            "BODMAS and Order of Operations",
            "Fractions, Decimals and Percentages",
            "Introduction to Algebra",
            "Factors, Multiples, HCF and LCM",
        ],
        "english_language": [
            "Parts of Speech",
            "Simple Tenses",
            "Reading Comprehension",
            "Formal and Informal Letter Writing",
            "Punctuation and Spelling",
        ],
        "basic_science": [
            "Characteristics of Living Things (MRS GREN)",
            "Classification of Living Things",
            "States of Matter",
            "Mixtures and Separation Techniques",
            "Safety in the Laboratory",
        ],
        "social_studies": [
            "The Family",
            "The Community",
            "Socialisation",
            "Basic Needs of Society",
            "Cultural Heritage",
        ],
        "basic_technology": [
            "Introduction to Technology",
            "Tools and Their Uses",
            "Simple Machines",
            "Technical Drawing Basics",
            "Safety in the Workshop",
        ],
        "civic_education": [
            "Citizenship",
            "Values and Norms",
            "Rights and Duties of a Citizen",
            "National Symbols of Nigeria",
            "Democratic Governance",
        ],
    },
    "jss2": {
        "mathematics": [
            "Directed Numbers and Integers",
            "Algebraic Expressions and Equations",
            "Plane Shapes — Area and Perimeter",
            "Statistics — Mean, Median, Mode",
            "Indices and Standard Form",
        ],
        "english_language": [
            "Pronouns — Types and Usage",
            "Adjectives and Degrees of Comparison",
            "Direct and Indirect Speech",
            "Paragraph and Essay Writing",
            "Oral English — Vowel Sounds",
        ],
        "basic_science": [
            "Forms of Energy and Energy Transfer",
            "Simple Machines and Mechanical Advantage",
            "Acids, Bases and the pH Scale",
            "The Human Digestive System",
            "Reproduction in Plants",
        ],
    },
    "jss3": {
        "mathematics": [
            "Quadratic Equations",
            "Pythagoras' Theorem and Trigonometry",
            "Mensuration — Volumes and Surface Areas",
            "Probability",
            "Direct and Inverse Variation",
        ],
        "english_language": [
            "Advanced Essay Writing for BECE",
            "Complex Sentences and Clauses",
            "Comprehension — Advanced Strategies",
            "Concord and Conditional Sentences",
            "BECE Oral English — Stress and Intonation",
        ],
        "basic_science": [
            "Genetics and Heredity",
            "Ecology and Food Chains",
            "Carbon Compounds — Introduction",
            "Electricity and Circuits",
            "Human Reproductive System",
        ],
    },
}


# ---------------------------------------------------------------------------
# LO ID generator
# ---------------------------------------------------------------------------

def make_lo_id(curriculum: str, subject_code: str, class_level: str, topic_index: int) -> str:
    """Return a canonical LO ID as defined in docs/LO_TAGGING_SCHEMA.md."""
    cls = class_level.upper()
    seq = str(topic_index + 1).zfill(3)
    topic_code = f"T{topic_index + 1}"
    return f"LO:{curriculum}:{subject_code}:{cls}:{topic_code}:{seq}"


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are an expert Nigerian secondary school curriculum writer. "
    "You produce clear, accurate, age-appropriate educational content "
    "aligned to the NERDC curriculum and WAEC/BECE examination standards. "
    "All content should be written in plain British English suitable for "
    "Nigerian students. Use Nigerian examples and contexts where relevant."
)


def build_chapter_prompt(
    class_level: str,
    subject: str,
    topic: str,
    term: int,
    chapter_number: int,
    exam: str,
) -> str:
    level_label = class_level.upper()
    return f"""Write a comprehensive textbook chapter for {level_label} {subject.replace('_', ' ').title()}.

Chapter {chapter_number} — Term {term}: {topic}

Target audience: Nigerian {level_label} students (age ~{_age_range(class_level)})
Target exams: {exam}
Curriculum: NERDC / FME

Include all of the following sections:
1. **Learning Objectives** (5 bullet points — what students will be able to do after this chapter)
2. **Introduction** (2–3 paragraphs setting context, relevance to daily life in Nigeria)
3. **Key Concepts** (4–5 concepts, each with:
   - Definition
   - Detailed explanation
   - Examples with Nigerian context
   - Worked examples / diagrams where applicable)
4. **Worked Examples** (3 problems with full step-by-step solutions)
5. **Common Mistakes and Misconceptions** (table format: mistake | correction | explanation)
6. **Summary** (bullet point recap of all key concepts)
7. **Practice Questions** (10 questions: 6 multiple-choice + 4 structured, with answers at end)
8. **Key Terms Glossary** (all bolded terms in the chapter)

Format: Markdown with clear heading hierarchy (## for sections, ### for sub-concepts).
Tone: Clear, encouraging, suitable for a 12–15 year old Nigerian student.
Length: 1,500–2,500 words.
"""


def _age_range(class_level: str) -> str:
    ages = {
        "jss1": "12–13",
        "jss2": "13–14",
        "jss3": "14–15",
        "ss1": "15–16",
        "ss2": "16–17",
        "ss3": "17–18",
    }
    return ages.get(class_level, "12–18")


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class TextbookGenerator:
    def __init__(
        self,
        api_base: str = "http://localhost:8004/v1",
        api_key: str = "local",
        model: str = "llama-3",
        output_dir: Path = Path("content/textbooks"),
        dry_run: bool = False,
    ) -> None:
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.model = model

        if not dry_run and _OPENAI_AVAILABLE:
            self.client: OpenAI | None = OpenAI(base_url=api_base, api_key=api_key)
        else:
            self.client = None

    def generate_chapter(
        self,
        class_level: str,
        subject: str,
        topic: str,
        topic_index: int,
        term: int,
        chapter_number: int,
        exam: str,
        subject_code: str,
    ) -> dict[str, Any]:
        prompt = build_chapter_prompt(class_level, subject, topic, term, chapter_number, exam)

        if self.dry_run:
            print(f"\n[DRY-RUN] Would generate: {class_level}/{subject}/chapter_{chapter_number}.md")
            print(f"  Topic: {topic}")
            print(f"  Prompt length: {len(prompt)} chars")
            md_content = f"# {topic}\n\n> DRY-RUN: LLM call skipped.\n"
        else:
            if self.client is None:
                print("ERROR: openai package not installed. Run: pip install openai", file=sys.stderr)
                sys.exit(1)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=4096,
            )
            md_content = response.choices[0].message.content or ""

        lo_id = make_lo_id("NERDC", subject_code, class_level, topic_index)

        chapter_json: dict[str, Any] = {
            "lo_id": lo_id,
            "curriculum": "NERDC",
            "subject": subject,
            "subject_code": subject_code,
            "class_level": class_level.upper(),
            "term": term,
            "chapter": chapter_number,
            "topic": topic,
            "target_exam": exam,
            "language": "en",
            "generated_at": datetime.now(tz=timezone.utc).isoformat(),
            "generator_version": "1.0.0",
            "content_md": md_content,
            "review_status": "pending",
        }
        return chapter_json

    def run(
        self,
        class_level: str,
        subject: str,
        term: int = 1,
        priority_filter: str | None = None,
    ) -> list[Path]:
        level_data = CURRICULUM.get(class_level)
        if level_data is None:
            print(f"ERROR: Unknown class level '{class_level}'. Choose from: {list(CURRICULUM)}", file=sys.stderr)
            sys.exit(1)

        subject_data = level_data["subjects"].get(subject)
        if subject_data is None:
            print(f"ERROR: '{subject}' not in {class_level} curriculum. Available: {list(level_data['subjects'])}", file=sys.stderr)
            sys.exit(1)

        if priority_filter and subject_data["priority"] != priority_filter:
            print(f"Skipping {class_level}/{subject} (priority={subject_data['priority']}, filter={priority_filter})")
            return []

        topics = CHAPTER_TOPICS.get(class_level, {}).get(subject, [f"Topic {i+1}" for i in range(5)])
        subject_code = subject_data["code"]
        exam = level_data["exam"]

        out_dir = self.output_dir / class_level / subject
        out_dir.mkdir(parents=True, exist_ok=True)

        written: list[Path] = []
        for idx, topic in enumerate(topics):
            chapter_number = idx + 1
            chapter = self.generate_chapter(
                class_level=class_level,
                subject=subject,
                topic=topic,
                topic_index=idx,
                term=term,
                chapter_number=chapter_number,
                exam=exam,
                subject_code=subject_code,
            )

            json_path = out_dir / f"chapter_{chapter_number:02d}.json"
            md_path = out_dir / f"chapter_{chapter_number:02d}.md"

            if not self.dry_run:
                json_path.write_text(json.dumps(chapter, indent=2, ensure_ascii=False), encoding="utf-8")
                md_path.write_text(chapter["content_md"], encoding="utf-8")
                print(f"  ✅ Written: {json_path} and {md_path}")

            written.extend([json_path, md_path])

        return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aku Platform Textbook Generator — JSS1–SS3 / NERDC curriculum",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--level", choices=list(CURRICULUM), help="Class level (e.g., jss1, ss2)")
    parser.add_argument("--subject", help="Subject name (e.g., mathematics, basic_science)")
    parser.add_argument("--term", type=int, default=1, choices=[1, 2, 3], help="School term (default: 1)")
    parser.add_argument("--priority", choices=["P1", "P2", "P3"], help="Only generate subjects of this priority")
    parser.add_argument("--all-jss", action="store_true", help="Generate all JSS1–JSS3 P1 subjects")
    parser.add_argument("--all-ss", action="store_true", help="Generate all SS1–SS3 P1 subjects")
    parser.add_argument("--api-base", default=os.getenv("AKUAI_API_BASE", "http://localhost:8004/v1"), help="OpenAI-compatible API base URL")
    parser.add_argument("--api-key", default=os.getenv("AKUAI_API_KEY", "local"), help="API key")
    parser.add_argument("--model", default=os.getenv("AKUAI_MODEL", "llama-3"), help="LLM model name")
    parser.add_argument("--output-dir", default="content/textbooks", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview without calling LLM")

    args = parser.parse_args()

    gen = TextbookGenerator(
        api_base=args.api_base,
        api_key=args.api_key,
        model=args.model,
        output_dir=Path(args.output_dir),
        dry_run=args.dry_run,
    )

    levels_to_run: list[tuple[str, str]] = []

    if args.all_jss:
        for lvl in ["jss1", "jss2", "jss3"]:
            for subj, meta in CURRICULUM[lvl]["subjects"].items():
                if meta["priority"] == "P1":
                    levels_to_run.append((lvl, subj))
    elif args.all_ss:
        for lvl in ["ss1", "ss2", "ss3"]:
            for subj, meta in CURRICULUM[lvl]["subjects"].items():
                if meta["priority"] == "P1":
                    levels_to_run.append((lvl, subj))
    elif args.level and args.subject:
        levels_to_run.append((args.level, args.subject))
    elif args.level:
        for subj in CURRICULUM[args.level]["subjects"]:
            levels_to_run.append((args.level, subj))
    else:
        parser.print_help()
        sys.exit(1)

    total_written = 0
    for level, subject in levels_to_run:
        print(f"\n📚 Generating: {level.upper()} / {subject.replace('_', ' ').title()} / Term {args.term}")
        written = gen.run(level, subject, term=args.term, priority_filter=args.priority)
        total_written += len(written)

    print(f"\n✅ Done. {total_written} files {'would be ' if args.dry_run else ''}written.")


if __name__ == "__main__":
    main()
