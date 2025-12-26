#!/usr/bin/env python3
"""
Prepare parallel corpus for machine translation training.
- Reads generated news corpus
- Builds parallel sentence pairs (English ↔ Hausa/Igbo/Yoruba)
- Outputs in formats suitable for training (TSV, JSON, HF datasets)

Usage:
  python prepare_ml_dataset.py --corpus content/news_corpus --output content/ml_datasets --lang ha --format tsv
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple
import re


def load_corpus(corpus_dir: Path, source_lang: str = "en", target_lang: str = None) -> List[Dict[str, str]]:
    """Load articles from corpus directory and pair them"""
    pairs = []
    
    # Find all JSON files in source lang folder
    source_articles = list(corpus_dir.glob(f"{source_lang}/**/*.json"))
    
    for article_path in source_articles:
        with open(article_path, "r", encoding="utf-8") as f:
            article = json.load(f)
        
        source_text = article.get("body", "")
        if not source_text:
            continue
        
        # Get target text
        if target_lang and target_lang in article.get("translations", {}):
            target_text = article["translations"][target_lang].get("body", "")
        elif target_lang:
            # Try to load translated version from disk
            target_articles = list(corpus_dir.glob(f"{target_lang}/**/{article_path.stem}.json"))
            if target_articles:
                with open(target_articles[0], "r", encoding="utf-8") as f:
                    trans_article = json.load(f)
                    target_text = trans_article.get("body", "")
            else:
                continue
        else:
            continue
        
        pairs.append({
            "source": source_text,
            "target": target_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "source_file": str(article_path),
        })
    
    return pairs


def split_into_sentences(text: str) -> List[str]:
    """Basic sentence splitting (period, question mark, exclamation)"""
    # Simple regex split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def build_sentence_pairs(text_pairs: List[Dict[str, str]]) -> List[Tuple[str, str]]:
    """Build sentence-level pairs for training"""
    sentence_pairs = []
    
    for pair in text_pairs:
        source_sents = split_into_sentences(pair["source"])
        target_sents = split_into_sentences(pair["target"])
        
        # Align sentences (naive: 1-to-1 if same length)
        for src, tgt in zip(source_sents, target_sents):
            if src and tgt:
                sentence_pairs.append((src, tgt))
    
    return sentence_pairs


def save_as_tsv(pairs: List[Tuple[str, str]], output_path: Path):
    """Save as TSV (source \\t target)"""
    with open(output_path, "w", encoding="utf-8") as f:
        for src, tgt in pairs:
            f.write(f"{src}\t{tgt}\n")
    print(f"✅ Saved TSV: {output_path} ({len(pairs)} pairs)")


def save_as_json(pairs: List[Tuple[str, str]], output_path: Path):
    """Save as JSON Lines"""
    with open(output_path, "w", encoding="utf-8") as f:
        for src, tgt in pairs:
            f.write(json.dumps({"source": src, "target": tgt}, ensure_ascii=False) + "\n")
    print(f"✅ Saved JSONL: {output_path} ({len(pairs)} pairs)")


def save_as_hf_dataset(pairs: List[Tuple[str, str]], output_path: Path, source_lang: str, target_lang: str):
    """Save in HF Datasets format (dict with 'source' and 'target' lists)"""
    data = {
        "translation": [
            {
                source_lang: src,
                target_lang: tgt,
            }
            for src, tgt in pairs
        ]
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved HF format: {output_path} ({len(pairs)} pairs)")


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare ML dataset from news corpus")
    parser.add_argument("--corpus", default="content/news_corpus", help="News corpus directory")
    parser.add_argument("--source-lang", default="en", help="Source language (en)")
    parser.add_argument("--target-lang", default="ha", help="Target language (ha, yo, ig)")
    parser.add_argument("--output", default="content/ml_datasets", help="Output directory")
    parser.add_argument("--format", choices=["tsv", "json", "hf"], default="tsv", help="Output format")
    parser.add_argument("--sentence-level", action="store_true", help="Split into sentence pairs")
    return parser.parse_args()


def main():
    args = parse_args()
    
    corpus_dir = Path(args.corpus)
    if not corpus_dir.exists():
        raise SystemExit(f"Corpus directory not found: {corpus_dir}")
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📚 Loading corpus from {corpus_dir}...")
    text_pairs = load_corpus(corpus_dir, args.source_lang, args.target_lang)
    print(f"✅ Loaded {len(text_pairs)} document pairs")
    
    if args.sentence_level:
        pairs = build_sentence_pairs(text_pairs)
    else:
        pairs = [(p["source"], p["target"]) for p in text_pairs]
    
    print(f"📊 Prepared {len(pairs)} training examples")
    
    # Save in requested format
    lang_pair = f"{args.source_lang}-{args.target_lang}"
    
    if args.format == "tsv":
        output_path = output_dir / f"{lang_pair}.tsv"
        save_as_tsv(pairs, output_path)
    elif args.format == "json":
        output_path = output_dir / f"{lang_pair}.jsonl"
        save_as_json(pairs, output_path)
    elif args.format == "hf":
        output_path = output_dir / f"{lang_pair}_hf.json"
        save_as_hf_dataset(pairs, output_path, args.source_lang, args.target_lang)
    
    print(f"\n✅ Dataset ready for training")


if __name__ == "__main__":
    main()
