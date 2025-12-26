#!/usr/bin/env python3
"""
Validate lesson tone using NaijaSenti-style sentiment models.
- Scores key text fields for sentiment (positive/neutral/negative)
- Useful to catch unintended negativity or inappropriate tone in localized lessons

Requires:
- transformers
- sentiment model (e.g., set via NAIJASENTI_MODEL env or --model)
"""

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_classifier(model_name: str, device: Optional[int] = None):
    try:
        from transformers import pipeline
    except ImportError:
        raise SystemExit("Install transformers (and torch): pip install transformers torch")

    kwargs = {"model": model_name}
    if device is not None:
        kwargs["device"] = device
    return pipeline("text-classification", **kwargs)


def gather_text_fields(lesson: Dict[str, Any]) -> List[str]:
    texts: List[str] = []

    texts.extend(lesson.get("learning_objectives", []))
    texts.extend(lesson.get("prerequisites", []))

    for section in lesson.get("content_sections", []):
        texts.append(section.get("title", ""))
        texts.append(section.get("content", ""))

    for ex in lesson.get("worked_examples", []):
        texts.append(ex.get("title", ""))
        texts.append(ex.get("context", ""))
        texts.append(ex.get("problem", ""))
        texts.append(ex.get("solution", ""))

    for prob in lesson.get("practice_problems", []):
        texts.append(prob.get("problem", ""))
        texts.append(prob.get("answer", ""))
        texts.append(prob.get("explanation", ""))

    for term in lesson.get("glossary", []):
        texts.append(term.get("definition", ""))
        texts.append(term.get("example", ""))

    assess = lesson.get("assessment", {})
    texts.extend(assess.get("quick_checks", []))
    for q in assess.get("end_of_lesson_quiz", []):
        texts.append(q.get("question", ""))
        texts.extend(q.get("options", []))
        texts.append(q.get("correct", ""))
    for q in assess.get("exam_style_questions", []):
        texts.append(q.get("question", ""))
        texts.append(q.get("answer_guide", ""))

    for aid in lesson.get("resources", {}).get("visual_aids", []):
        texts.append(aid.get("title", ""))
        texts.append(aid.get("description", ""))

    # Deduplicate short strings
    return [t for t in {x.strip() for x in texts if x and x.strip()}]


def classify_texts(texts: List[str], classifier) -> Dict[str, Any]:
    results = []
    for t in texts:
        # limit extremely long passages
        sample = t[:512]
        out = classifier(sample)[0]
        results.append({"text": sample, "label": out["label"], "score": out["score"]})
    summary = summarize(results)
    return {"summary": summary, "details": results}


def summarize(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts: Dict[str, int] = {}
    for r in results:
        counts[r["label"]] = counts.get(r["label"], 0) + 1
    total = len(results) or 1
    pct = {k: round(v * 100 / total, 1) for k, v in counts.items()}
    flags = []
    if pct.get("negative", 0) > 20:
        flags.append("High negative sentiment (>20%)")
    if pct.get("neutral", 0) > 80:
        flags.append("Mostly neutral—check engagement tone")
    return {"counts": counts, "percent": pct, "flags": flags}


def parse_args():
    parser = argparse.ArgumentParser(description="Tone validation with NaijaSenti models")
    parser.add_argument("json_path", help="Lesson JSON to validate")
    parser.add_argument("--model", help="Hugging Face sentiment model (env: NAIJASENTI_MODEL)")
    parser.add_argument("--device", type=int, default=None, help="Device id for transformers pipeline")
    parser.add_argument("--output", help="Optional report path (JSON)")
    return parser.parse_args()


def main():
    args = parse_args()
    json_path = Path(args.json_path)
    if not json_path.exists():
        raise SystemExit(f"JSON not found: {json_path}")

    model_name = args.model or os.getenv("NAIJASENTI_MODEL")
    if not model_name:
        raise SystemExit("Provide --model or set NAIJASENTI_MODEL")

    classifier = load_classifier(model_name, device=args.device)

    with open(json_path, "r", encoding="utf-8") as f:
        lesson = json.load(f)

    report = classify_texts(gather_text_fields(lesson), classifier)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"✅ Tone report saved to: {out_path}")
    else:
        print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
