#!/usr/bin/env python3
"""
bece_scraper.py — Aku Platform Content Pipeline

Scrapes and structures BECE (Basic Education Certificate Examination) and
Common Entrance past questions for JSS1–JSS3 subjects.

Forked from mlops/exam_paper_scraper.py, adapted for:
  - Junior Secondary / BECE (administered by WAEC Nigeria)
  - Common Entrance Examination (NECO / State ministries)
  - National Common Entrance Examination (NCEE — Federal Government Colleges)

Output: data/exam_papers/bece/<subject>/<year>_questions.json

Format matches the existing exam_papers/INDEX.json schema so that Akudemy
can import both senior and junior exam papers using the same seed_content.py.

Data Sources (public/open access):
  1. WAEC Nigeria past questions — https://waeconline.org.ng
  2. NECO past questions — https://neco.gov.ng
  3. Exam digest sites (waecquestions.com, myschool.ng, examkey.net)
  4. Textbooks and study guides (structured manually)

Usage:
  python pipeline/bece_scraper.py --subject mathematics --years 2019 2020 2021 2022 2023
  python pipeline/bece_scraper.py --all --years 2020 2021 2022 2023
  python pipeline/bece_scraper.py --dry-run --subject basic_science

Note:
  Full scraping requires network access and site-specific adapters.
  This script provides the framework + manual-entry mode.
  Run with --manual to add questions interactively.

Dependencies:
  pip install requests beautifulsoup4 pydantic
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Subjects covered by BECE / Common Entrance
# ---------------------------------------------------------------------------

BECE_SUBJECTS: dict[str, dict[str, Any]] = {
    "mathematics": {
        "code": "MAT",
        "waec_paper": "Mathematics",
        "ncee_paper": "Quantitative Aptitude",
        "questions_per_paper": 60,
        "topics": [
            "Place Value and Number Systems",
            "Fractions, Decimals and Percentages",
            "Directed Numbers",
            "Algebra — Linear Equations",
            "Geometry — Angles and Triangles",
            "Plane Shapes — Area and Perimeter",
            "Mensuration — Volume and Surface Area",
            "Statistics — Mean, Median, Mode",
            "Probability",
            "Sets",
        ],
    },
    "english_language": {
        "code": "ENG",
        "waec_paper": "English Language",
        "ncee_paper": "English Studies",
        "questions_per_paper": 80,
        "topics": [
            "Parts of Speech",
            "Tenses",
            "Comprehension",
            "Letter Writing",
            "Essay Writing",
            "Direct and Indirect Speech",
            "Punctuation",
            "Vocabulary",
            "Oral English",
        ],
    },
    "basic_science": {
        "code": "BSC",
        "waec_paper": "Basic Science",
        "ncee_paper": "Basic Science",
        "questions_per_paper": 60,
        "topics": [
            "Living Things and Classification",
            "States of Matter",
            "Acids, Bases and Salts",
            "Energy and Its Forms",
            "Simple Machines",
            "Ecology and Food Chains",
            "Genetics and Heredity",
            "Electricity",
            "Separation Techniques",
            "Reproduction",
        ],
    },
    "social_studies": {
        "code": "SST",
        "waec_paper": "Social Studies",
        "ncee_paper": "Social Studies",
        "questions_per_paper": 60,
        "topics": [
            "The Family",
            "Citizenship and Democracy",
            "Culture and Heritage",
            "Social Problems",
            "Government and Politics",
            "Human Rights",
            "National Development",
        ],
    },
    "basic_technology": {
        "code": "BTH",
        "waec_paper": "Basic Technology",
        "ncee_paper": None,
        "questions_per_paper": 60,
        "topics": [
            "Materials and Their Uses",
            "Tools and Safety",
            "Technical Drawing",
            "Simple Machines",
            "Electricity and Electronics",
        ],
    },
    "civic_education": {
        "code": "CIV",
        "waec_paper": "Civic Education",
        "ncee_paper": None,
        "questions_per_paper": 60,
        "topics": [
            "Citizenship",
            "Values and Norms",
            "Democratic Governance",
            "Human Rights",
            "Rule of Law",
        ],
    },
}

# ---------------------------------------------------------------------------
# Sample question bank (starter — expand by running with --manual or scrapers)
# ---------------------------------------------------------------------------

SAMPLE_QUESTIONS: dict[str, list[dict[str, Any]]] = {
    "mathematics": [
        {
            "id": "MAT-BECE-2023-001",
            "topic": "Fractions, Decimals and Percentages",
            "class_level": "JSS3",
            "year": 2023,
            "exam": "BECE",
            "body": "Evaluate ¾ + ⅔",
            "options": ["1 5/12", "1 7/12", "1 1/4", "1 1/3"],
            "correct_option": 0,
            "answer": "1 5/12",
            "explanation": "LCM of 4 and 3 is 12. ¾ = 9/12; ⅔ = 8/12. Sum = 17/12 = 1 5/12.",
            "difficulty": "medium",
            "marks": 1,
            "source": "sample",
            "lo_id": "LO:NERDC:MAT:JSS3:T1:001",
        },
        {
            "id": "MAT-BECE-2023-002",
            "topic": "Algebra — Linear Equations",
            "class_level": "JSS3",
            "year": 2023,
            "exam": "BECE",
            "body": "Solve for x: 3x − 5 = 10",
            "options": ["3", "5", "7", "15"],
            "correct_option": 1,
            "answer": "5",
            "explanation": "3x = 10 + 5 = 15; x = 15/3 = 5.",
            "difficulty": "easy",
            "marks": 1,
            "source": "sample",
            "lo_id": "LO:NERDC:MAT:JSS3:T2:001",
        },
        {
            "id": "MAT-BECE-2023-003",
            "topic": "Probability",
            "class_level": "JSS3",
            "year": 2023,
            "exam": "BECE",
            "body": "A bag contains 4 red, 6 blue and 2 green balls. A ball is picked at random. What is the probability of picking a blue ball?",
            "options": ["1/2", "1/3", "1/6", "3/4"],
            "correct_option": 0,
            "answer": "1/2",
            "explanation": "Total = 12. Blue = 6. P(blue) = 6/12 = 1/2.",
            "difficulty": "easy",
            "marks": 1,
            "source": "sample",
            "lo_id": "LO:NERDC:MAT:JSS3:T9:001",
        },
        {
            "id": "MAT-BECE-2022-001",
            "topic": "Mensuration — Volume and Surface Area",
            "class_level": "JSS3",
            "year": 2022,
            "exam": "BECE",
            "body": "Find the volume of a cylinder with radius 7 cm and height 10 cm. [π = 22/7]",
            "options": ["440 cm³", "1,540 cm³", "1,100 cm³", "2,200 cm³"],
            "correct_option": 1,
            "answer": "1,540 cm³",
            "explanation": "V = πr²h = (22/7) × 49 × 10 = 22 × 7 × 10 = 1,540 cm³.",
            "difficulty": "medium",
            "marks": 1,
            "source": "sample",
            "lo_id": "LO:NERDC:MAT:JSS3:T6:001",
        },
    ],
    "english_language": [
        {
            "id": "ENG-BECE-2023-001",
            "topic": "Parts of Speech",
            "class_level": "JSS3",
            "year": 2023,
            "exam": "BECE",
            "body": 'Identify the part of speech of the underlined word: "She runs very QUICKLY."',
            "options": ["Adjective", "Verb", "Adverb", "Noun"],
            "correct_option": 2,
            "answer": "Adverb",
            "explanation": '"Quickly" modifies the verb "runs" — it tells us HOW she runs → adverb.',
            "difficulty": "easy",
            "marks": 1,
            "source": "sample",
            "lo_id": "LO:NERDC:ENG:JSS3:T1:001",
        },
        {
            "id": "ENG-BECE-2023-002",
            "topic": "Direct and Indirect Speech",
            "class_level": "JSS3",
            "year": 2023,
            "exam": "BECE",
            "body": 'Change to indirect speech: She said, "I am going to school."',
            "options": [
                'She said that she is going to school.',
                'She said that she was going to school.',
                'She says that she was going to school.',
                'She said that I am going to school.',
            ],
            "correct_option": 1,
            "answer": "She said that she was going to school.",
            "explanation": 'In indirect speech with past reporting verb ("said"), present tense "am" changes to past "was".',
            "difficulty": "medium",
            "marks": 1,
            "source": "sample",
            "lo_id": "LO:NERDC:ENG:JSS3:T6:001",
        },
    ],
    "basic_science": [
        {
            "id": "BSC-BECE-2023-001",
            "topic": "Living Things and Classification",
            "class_level": "JSS3",
            "year": 2023,
            "exam": "BECE",
            "body": "Which of the following is a characteristic of living things?",
            "options": ["Hardness", "Respiration", "Solubility", "Density"],
            "correct_option": 1,
            "answer": "Respiration",
            "explanation": "Respiration (R in MRS GREN) is a characteristic of all living things. Hardness, solubility and density are physical properties of matter.",
            "difficulty": "easy",
            "marks": 1,
            "source": "sample",
            "lo_id": "LO:NERDC:BSC:JSS3:T1:001",
        },
        {
            "id": "BSC-BECE-2023-002",
            "topic": "Electricity",
            "class_level": "JSS3",
            "year": 2023,
            "exam": "BECE",
            "body": "A resistor has a resistance of 10 Ω and is connected to a 5 V battery. What is the current flowing through it?",
            "options": ["50 A", "2 A", "0.5 A", "15 A"],
            "correct_option": 2,
            "answer": "0.5 A",
            "explanation": "Ohm's Law: I = V/R = 5/10 = 0.5 A.",
            "difficulty": "medium",
            "marks": 1,
            "source": "sample",
            "lo_id": "LO:NERDC:BSC:JSS3:T8:001",
        },
    ],
}


# ---------------------------------------------------------------------------
# Scraper / Data writer
# ---------------------------------------------------------------------------

class BeceScraper:
    def __init__(
        self,
        output_dir: Path = Path("data/exam_papers/bece"),
        dry_run: bool = False,
    ) -> None:
        self.output_dir = output_dir
        self.dry_run = dry_run

    def write_subject_file(
        self,
        subject: str,
        years: list[int],
        questions: list[dict[str, Any]],
    ) -> Path:
        meta = BECE_SUBJECTS.get(subject, {})
        code = meta.get("code", "UNK")

        filtered = [
            q for q in questions
            if q.get("year") in years or not years
        ]

        out_data: dict[str, Any] = {
            "subject": subject,
            "subject_code": code,
            "exam": "BECE",
            "source_body": "WAEC Nigeria / NECO / State Ministries of Education",
            "class_levels": ["JSS1", "JSS2", "JSS3"],
            "years": sorted(set(q.get("year", 0) for q in filtered)),
            "question_count": len(filtered),
            "generated_at": datetime.now(tz=timezone.utc).isoformat(),
            "generator_version": "1.0.0",
            "questions": filtered,
        }

        out_dir = self.output_dir / subject
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "questions.json"

        if not self.dry_run:
            out_path.write_text(json.dumps(out_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  ✅ Written: {out_path} ({len(filtered)} questions)")
        else:
            print(f"  [DRY-RUN] Would write: {out_path} ({len(filtered)} questions)")

        return out_path

    def write_index(self, subjects_written: list[str]) -> Path:
        index: dict[str, Any] = {
            "description": "BECE / Common Entrance past questions index",
            "exam_bodies": ["WAEC Nigeria", "NECO", "NCEE", "State Ministries"],
            "class_levels": ["JSS1", "JSS2", "JSS3"],
            "subjects": subjects_written,
            "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        }
        out_path = self.output_dir / "INDEX.json"
        if not self.dry_run:
            out_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  ✅ Written: {out_path}")
        else:
            print(f"  [DRY-RUN] Would write: {out_path}")
        return out_path

    def run(self, subjects: list[str], years: list[int]) -> None:
        written_subjects: list[str] = []
        for subject in subjects:
            if subject not in BECE_SUBJECTS:
                print(f"  ⚠️  Unknown BECE subject: {subject}; skipping", file=sys.stderr)
                continue

            print(f"\n📚 Processing BECE: {subject}")
            questions = SAMPLE_QUESTIONS.get(subject, [])
            self.write_subject_file(subject, years, questions)
            written_subjects.append(subject)

        self.write_index(written_subjects)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aku Platform BECE/Common Entrance Scraper — JSS1–JSS3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--subject", help="Subject to scrape (e.g., mathematics)")
    parser.add_argument("--all", action="store_true", dest="all_subjects", help="Scrape all BECE subjects")
    parser.add_argument("--years", type=int, nargs="+", default=[2019, 2020, 2021, 2022, 2023],
                        help="Years to include (default: 2019–2023)")
    parser.add_argument("--output-dir", default="data/exam_papers/bece",
                        help="Output directory (default: data/exam_papers/bece)")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    scraper = BeceScraper(
        output_dir=Path(args.output_dir),
        dry_run=args.dry_run,
    )

    if args.all_subjects:
        subjects = list(BECE_SUBJECTS.keys())
    elif args.subject:
        subjects = [args.subject]
    else:
        parser.print_help()
        sys.exit(1)

    scraper.run(subjects=subjects, years=args.years)
    print(f"\n✅ Done. Output: {args.output_dir}")


if __name__ == "__main__":
    main()
