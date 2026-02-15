"""
Auto-tagging prototype:
- Loads `content/lo_catalog.json` (LO descriptions)
- Loads `content/catalog.json` content first_page snippets
- Vectorizes LO texts and asset texts using TF-IDF and computes cosine similarity
- Writes `content/auto_tag_suggestions.json` with top-N suggested LO IDs per asset

Usage:
    python -m mlops.auto_tagging --top 3
"""
import json
from pathlib import Path
import argparse
import logging

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('auto_tag')

ROOT = Path(__file__).resolve().parents[1]
LO_CATALOG = ROOT / 'content' / 'lo_catalog.json'
CATALOG = ROOT / 'content' / 'catalog.json'
OUT = ROOT / 'content' / 'auto_tag_suggestions.json'


def load_lo_texts():
    if not LO_CATALOG.exists():
        return []
    data = json.loads(LO_CATALOG.read_text(encoding='utf-8'))
    return data.get('lo_entries', [])


def load_catalog():
    if not CATALOG.exists():
        return []
    data = json.loads(CATALOG.read_text(encoding='utf-8'))
    return data.get('items', [])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top', type=int, default=3)
    args = parser.parse_args()

    lo_entries = load_lo_texts()
    catalog_items = load_catalog()

    lo_texts = [ (lo['lo_id'], lo.get('lo_text','')) for lo in lo_entries ]
    asset_texts = [ (it['path'], it.get('first_page','')) for it in catalog_items ]

    # Build TF-IDF over both LO texts and asset_texts to have consistent vocab
    texts = [t for _,t in lo_texts] + [t for _,t in asset_texts]
    vect = TfidfVectorizer(max_features=1000)
    X = vect.fit_transform(texts)
    X_lo = X[:len(lo_texts)]
    X_assets = X[len(lo_texts):]

    suggestions = []
    if X_assets.shape[0] == 0:
        logger.info('No asset texts to suggest tags for')
    else:
        sims = cosine_similarity(X_assets, X_lo)
        for i, (path, text) in enumerate(asset_texts):
            row = sims[i]
            idxs = np.argsort(row)[::-1][:args.top]
            candidates = []
            for j in idxs:
                candidates.append({
                    'lo_id': lo_texts[j][0],
                    'score': float(row[j]),
                    'lo_text': lo_texts[j][1],
                })
            suggestions.append({
                'asset_path': path,
                'candidates': candidates,
            })

    out = { 'generated_at': '', 'suggestions': suggestions }
    OUT.write_text(json.dumps(out, indent=2), encoding='utf-8')
    logger.info(f'Wrote suggestions to {OUT}')

if __name__ == '__main__':
    main()
