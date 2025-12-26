#!/usr/bin/env python3
"""
Translate lesson JSONs using Hugging Face translation models (Masakhane-friendly).
- Input: lesson JSON (English source)
- Output: translated JSON saved under content/ai_generated_translated/<lang>/...

Notes:
- Requires `transformers` and a translation model (e.g., a Masakhane MT model) available locally or via the Hugging Face Hub.
- Provide the model via --model or HUGGINGFACE_TRANSLATION_MODEL env var.
- Keeps structure; only text fields are translated. Adds translation metadata.
"""

import argparse
import copy
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

# Lazy import transformers to allow help/usage without dependency installed
def load_translator(model_name: str, device: Optional[int] = None):
    try:
        from transformers import pipeline
    except ImportError:
        raise SystemExit("Install transformers (and torch) to use translation: pip install transformers torch")

    kwargs = {"model": model_name}
    if device is not None:
        kwargs["device"] = device
    return pipeline("translation", **kwargs)


def chunk_text(text: str, max_chars: int = 450) -> List[str]:
    """Naive text chunking to avoid overly long inputs"""
    if len(text) <= max_chars:
        return [text]
    parts = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        # try to break on sentence end
        period = text.rfind(". ", start, end)
        if period != -1 and period + 2 - start > max_chars * 0.4:
            end = period + 1
        parts.append(text[start:end].strip())
        start = end
    return [p for p in parts if p]


def translate_text(text: str, translator) -> str:
    if not text:
        return text
    chunks = chunk_text(text)
    outputs = []
    for ch in chunks:
        result = translator(ch)[0]["translation_text"]
        outputs.append(result)
    return " ".join(outputs)


def translate_list(items: List[str], translator) -> List[str]:
    return [translate_text(x, translator) for x in items]


def translate_lesson(lesson: Dict[str, Any], target_lang: str, translator, model_name: str) -> Dict[str, Any]:
    data = copy.deepcopy(lesson)

    # Metadata
    data["metadata"]["lesson_title"] = translate_text(data["metadata"]["lesson_title"], translator)
    data["metadata"]["unit_title"] = translate_text(data["metadata"].get("unit_title", ""), translator)
    data["metadata"]["translation"] = {
        "source_language": data["metadata"].get("language", "en"),
        "target_language": target_lang,
        "model": model_name,
    }

    # Learning objectives & prerequisites
    data["learning_objectives"] = translate_list(data.get("learning_objectives", []), translator)
    data["prerequisites"] = translate_list(data.get("prerequisites", []), translator)

    # Content sections
    for section in data.get("content_sections", []):
        section["title"] = translate_text(section.get("title", ""), translator)
        section["content"] = translate_text(section.get("content", ""), translator)

    # Worked examples
    for ex in data.get("worked_examples", []):
        ex["title"] = translate_text(ex.get("title", ""), translator)
        ex["context"] = translate_text(ex.get("context", ""), translator)
        ex["problem"] = translate_text(ex.get("problem", ""), translator)
        ex["solution"] = translate_text(ex.get("solution", ""), translator)

    # Practice problems
    for prob in data.get("practice_problems", []):
        prob["problem"] = translate_text(prob.get("problem", ""), translator)
        prob["answer"] = translate_text(prob.get("answer", ""), translator)
        prob["explanation"] = translate_text(prob.get("explanation", ""), translator)

    # Glossary
    for term in data.get("glossary", []):
        term["term"] = translate_text(term.get("term", ""), translator)
        term["definition"] = translate_text(term.get("definition", ""), translator)
        term["example"] = translate_text(term.get("example", ""), translator)

    # Assessment
    assess = data.get("assessment", {})
    if assess.get("quick_checks"):
        assess["quick_checks"] = translate_list(assess["quick_checks"], translator)
    if assess.get("end_of_lesson_quiz"):
        for q in assess["end_of_lesson_quiz"]:
            q["question"] = translate_text(q.get("question", ""), translator)
            q["options"] = translate_list(q.get("options", []), translator)
            q["correct"] = translate_text(q.get("correct", ""), translator)
    if assess.get("exam_style_questions"):
        for q in assess["exam_style_questions"]:
            q["question"] = translate_text(q.get("question", ""), translator)
            q["answer_guide"] = translate_text(q.get("answer_guide", ""), translator)

    # Resources
    for aid in data.get("resources", {}).get("visual_aids", []):
        aid["title"] = translate_text(aid.get("title", ""), translator)
        aid["description"] = translate_text(aid.get("description", ""), translator)

    return data


def build_output_path(input_path: Path, target_lang: str) -> Path:
    rel = input_path.relative_to(Path("content/ai_generated"))
    out_dir = Path("content/ai_generated_translated") / target_lang / rel.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / rel.name


def parse_args():
    parser = argparse.ArgumentParser(description="Translate lesson JSON using HF translation models")
    parser.add_argument("json_path", help="Path to lesson JSON")
    parser.add_argument("--lang", required=True, help="Target language code (e.g., ha, yo, ig)")
    parser.add_argument("--model", help="Hugging Face translation model name (env: HUGGINGFACE_TRANSLATION_MODEL)")
    parser.add_argument("--device", type=int, default=None, help="Device id for transformers pipeline (e.g., 0 for GPU)")
    parser.add_argument("--output", help="Optional output path; defaults under content/ai_generated_translated/<lang>/...")
    return parser.parse_args()


def main():
    args = parse_args()
    json_path = Path(args.json_path)
    if not json_path.exists():
        raise SystemExit(f"JSON not found: {json_path}")

    model_name = args.model or os.getenv("HUGGINGFACE_TRANSLATION_MODEL")
    if not model_name:
        raise SystemExit("Provide --model or set HUGGINGFACE_TRANSLATION_MODEL")

    translator = load_translator(model_name, device=args.device)

    with open(json_path, "r", encoding="utf-8") as f:
        lesson = json.load(f)

    translated = translate_lesson(lesson, args.lang, translator, model_name)

    out_path = Path(args.output) if args.output else build_output_path(json_path, args.lang)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)

    print(f"✅ Translated saved to: {out_path}")


if __name__ == "__main__":
    main()
