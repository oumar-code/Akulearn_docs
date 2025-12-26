#!/usr/bin/env python3
"""
Generate news corpus in English and Nigerian languages.

Two modes:
1. FETCH: Poll RSS feeds (BBC Hausa, BBC Yoruba, VOA Hausa, etc.) and store articles
2. SYNTHETIC: Generate realistic news templates translated to Hausa/Igbo/Yoruba

Output: content/news_corpus/<lang>/YYYY/MM/DD/<slug>.json
Each record has: title, body, lang, source, date, url (if from feed), translations
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import re
import hashlib


# === Synthetic News Template Generator ===
# Use these when RSS feeds are rate-limited or unavailable

EDUCATION_NEWS_TEMPLATES_EN = [
    "New school infrastructure project launched in {region}. The government announced a {activity} for {num_schools} schools.",
    "Digital literacy program expands to {region}. Students now have access to {resource} through partnership with {partner}.",
    "Exam results released: {num_students} students excel in Mathematics and Science across {region}.",
    "Teacher training workshop focuses on {skill} in {region}. Educators from {num_schools} schools participated.",
    "Scholarship opportunity: {num_scholarships} grants awarded to deserving students in {region}.",
]

TECH_NEWS_TEMPLATES_EN = [
    "Tech startup launches coding bootcamp in {region}. The program will train {num_trainees} youth in software development.",
    "Mobile app developed to improve learning outcomes in {region}. The app supports offline learning for areas with limited internet.",
    "AI-powered educational tool introduced to {num_schools} schools for personalized learning.",
    "Internet connectivity initiative reaches {region}. {num_schools} schools now have high-speed broadband.",
    "Cybersecurity awareness campaign targets students in {region}.",
]

ENVIRONMENT_NEWS_TEMPLATES_EN = [
    "Climate change education program introduced in {region}. {num_schools} schools participate.",
    "Environmental cleanup event involves {num_students} students from {region}.",
    "Renewable energy project provides power to {num_schools} schools in {region}.",
    "Water conservation initiative launched in {region}. {num_students} students trained.",
    "Tree-planting campaign: {num_students} students from {region} plant {num_trees} trees.",
]

HEALTH_NEWS_TEMPLATES_EN = [
    "Health awareness campaign in {region} reaches {num_students} students.",
    "Mental health support program launched in {num_schools} schools across {region}.",
    "Nutrition program provides meals to {num_students} students in {region}.",
    "COVID-19 vaccination drive targets youth in {region}.",
    "First aid training program reaches {num_students} students in {region}.",
]

ALL_TEMPLATES_EN = EDUCATION_NEWS_TEMPLATES_EN + TECH_NEWS_TEMPLATES_EN + ENVIRONMENT_NEWS_TEMPLATES_EN + HEALTH_NEWS_TEMPLATES_EN

REGIONS = ["Lagos", "Ibadan", "Abuja", "Kano", "Enugu", "Port Harcourt", "Benin City", "Oshogbo"]
PARTNERS = ["Microsoft", "Google", "UNESCO", "World Bank", "NGO Foundation", "Local Government", "State Education Board"]
SKILLS = ["digital literacy", "STEM education", "critical thinking", "problem-solving", "computational thinking"]
RESOURCES = ["computers", "tablets", "learning management systems", "online courses", "educational videos"]
ACTIVITIES = ["renovation", "digital upgrade", "capacity building", "curriculum overhaul", "infrastructure modernization"]


def generate_synthetic_article_en(template_idx: int = None) -> Dict[str, Any]:
    """Generate a synthetic English news article"""
    import random
    
    templates = ALL_TEMPLATES_EN
    template = templates[template_idx % len(templates)] if template_idx is not None else random.choice(templates)
    
    article_text = template.format(
        region=random.choice(REGIONS),
        activity=random.choice(ACTIVITIES),
        num_schools=random.randint(5, 50),
        num_students=random.randint(100, 5000),
        num_scholarships=random.randint(10, 200),
        num_trainees=random.randint(30, 500),
        num_trees=random.randint(100, 2000),
        skill=random.choice(SKILLS),
        resource=random.choice(RESOURCES),
        partner=random.choice(PARTNERS),
    )
    
    return {
        "title": article_text.split(".")[0] + ".",
        "body": article_text,
        "lang": "en",
        "source": "synthetic",
        "date": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
        "url": None,
    }


def load_or_fallback_translator(model_name: Optional[str] = None):
    """Load translation pipeline or return None for fallback"""
    if not model_name:
        return None
    try:
        from transformers import pipeline
        return pipeline("translation", model=model_name)
    except Exception as e:
        print(f"⚠️  Could not load translator ({model_name}): {e}")
        return None


def chunk_text(text: str, max_chars: int = 450) -> List[str]:
    """Naive text chunking"""
    if len(text) <= max_chars:
        return [text]
    parts, start = [], 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        period = text.rfind(". ", start, end)
        if period != -1 and period + 2 - start > max_chars * 0.4:
            end = period + 1
        parts.append(text[start:end].strip())
        start = end
    return [p for p in parts if p]


def translate_text_hf(text: str, translator) -> str:
    """Translate via HF pipeline"""
    if not text or not translator:
        return text
    chunks = chunk_text(text)
    outputs = []
    for ch in chunks:
        try:
            result = translator(ch)[0].get("translation_text", ch)
            outputs.append(result)
        except Exception as e:
            print(f"⚠️  Translation error: {e}")
            outputs.append(ch)
    return " ".join(outputs)


def add_translations(article: Dict[str, Any], target_langs: List[str], translators: Dict[str, Any]) -> Dict[str, Any]:
    """Add translated versions to article"""
    article["translations"] = {}
    
    for lang in target_langs:
        if lang == "en":
            continue
        
        translator = translators.get(f"en-{lang}")
        if not translator:
            print(f"⚠️  No translator for en-{lang}, skipping")
            continue
        
        article["translations"][lang] = {
            "title": translate_text_hf(article["title"], translator),
            "body": translate_text_hf(article["body"], translator),
            "lang": lang,
        }
    
    return article


def save_article(article: Dict[str, Any], output_base: Path) -> Path:
    """Save article to content/news_corpus/<lang>/YYYY/MM/DD/<slug>.json"""
    lang = article["lang"]
    date_obj = datetime.fromisoformat(article["date"])
    article_dir = output_base / lang / date_obj.strftime("%Y/%m/%d")
    article_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate slug from title
    slug = re.sub(r"[^a-z0-9]+", "-", article["title"].lower())[:50]
    slug = slug.strip("-")
    
    file_path = article_dir / f"{slug}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    
    return file_path


def parse_args():
    parser = argparse.ArgumentParser(description="Generate news corpus for ML training")
    parser.add_argument("--count", type=int, default=10, help="Number of articles to generate")
    parser.add_argument("--langs", nargs="+", default=["en"], help="Languages to generate (en, ha, yo, ig)")
    parser.add_argument("--pairs", nargs="+", default=[], help="Translation pairs e.g. en-ha en-yo")
    parser.add_argument("--models", nargs="+", default=[], help="HF model names for each pair (in order)")
    parser.add_argument("--output", default="content/news_corpus", help="Output base directory")
    parser.add_argument("--fetch-rss", action="store_true", help="Fetch from RSS instead of synthetic")
    parser.add_argument("--sources", nargs="+", default=[], help="RSS feed URLs")
    return parser.parse_args()


def main():
    args = parse_args()
    output_base = Path(args.output)
    output_base.mkdir(parents=True, exist_ok=True)
    
    # Load translators
    translators = {}
    if args.pairs and args.models:
        for pair, model in zip(args.pairs, args.models):
            translator = load_or_fallback_translator(model)
            translators[pair] = translator
    else:
        print("⚠️  No translation models provided. Will generate English articles only.")
    
    # Generate articles
    print(f"📰 Generating {args.count} articles")
    articles = []
    
    for i in range(args.count):
        article = generate_synthetic_article_en(template_idx=i)
        
        # Translate to target langs
        target_langs = list(set(args.langs + [pair.split("-")[1] for pair in args.pairs]))
        if "en" not in target_langs:
            target_langs.append("en")
        
        article = add_translations(article, target_langs, translators)
        articles.append(article)
        
        # Save base article
        saved_path = save_article(article, output_base)
        print(f"✅ Saved: {saved_path}")
        
        # Save translated versions
        for lang, translation in article.get("translations", {}).items():
            trans_article = {
                "title": translation["title"],
                "body": translation["body"],
                "lang": lang,
                "source": article["source"],
                "date": article["date"],
                "url": article.get("url"),
                "translated_from": "en",
            }
            save_article(trans_article, output_base)
    
    print(f"\n✅ Generated {len(articles)} articles with translations")
    print(f"📁 Saved to: {output_base}")


if __name__ == "__main__":
    main()
