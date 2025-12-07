from pathlib import Path
import json
from datetime import datetime
from typing import List, Tuple, Dict, Any


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
CATALOG_PATH = CONTENT_DIR / "catalog.json"
LO_CATALOG_PATH = CONTENT_DIR / "lo_catalog.json"
OUTPUT_PATH = CONTENT_DIR / "auto_tag_suggestions.json"


def _lazy_embed(texts: List[str], model_name: str = "all-MiniLM-L6-v2"):
    # Lazy import to avoid heavy dependency at import time
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
    except Exception as e:
        raise RuntimeError("Missing dependency for embeddings: install sentence-transformers and numpy") from e

    model = SentenceTransformer(model_name)
    emb = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    # normalize for cosine similarity with dot-product
    norms = (emb ** 2).sum(axis=1, keepdims=True) ** 0.5
    norms[norms == 0] = 1.0
    emb = emb / norms
    return emb


def _build_index(embeddings):
    # Try faiss first, fallback to sklearn NearestNeighbors
    try:
        import faiss
        import numpy as np
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)  # inner-product on normalized vectors => cosine
        index.add(embeddings.astype('float32'))
        return ('faiss', index)
    except Exception:
        # fallback
        try:
            from sklearn.neighbors import NearestNeighbors
            nn = NearestNeighbors(n_neighbors=10, metric='cosine')
            nn.fit(embeddings)
            return ('sklearn', nn)
        except Exception as e:
            raise RuntimeError('No suitable nearest-neighbor backend available (faiss or scikit-learn)') from e


def _query_index(index_obj, backend: str, query_emb, top_k=5):
    import numpy as np
    if backend == 'faiss':
        D, I = index_obj.search(query_emb.astype('float32'), top_k)
        # D is inner product (cosine) scores because vectors are normalized
        return I[0].tolist(), D[0].tolist()
    else:
        # sklearn returns distances (cosine distances); convert to similarity
        dists, idx = index_obj.kneighbors(query_emb, n_neighbors=top_k)
        sims = (1.0 - dists).tolist()
        return idx[0].tolist(), sims[0]


def load_lo_catalog(path: Path = LO_CATALOG_PATH) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('lo_entries', [])


def load_catalog_texts(path: Path = CATALOG_PATH) -> List[Tuple[str, str]]:
    # returns list of (asset_id, text_snippet)
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    items = []
    for it in data if isinstance(data, list) else data.get('items', data.get('assets', [])):
        asset_id = it.get('path') or it.get('asset_path') or it.get('id') or it.get('file')
        text = it.get('text') or it.get('first_page_text') or it.get('snippet') or ''
        items.append((asset_id or 'unknown', text or ''))
    return items


def run(top_k: int = 3, model_name: str = "all-MiniLM-L6-v2"):
    los = load_lo_catalog()
    if not los:
        print('No LO entries found at', LO_CATALOG_PATH)
        return

    lo_texts = [l.get('lo_text', '') for l in los]
    lo_ids = [l.get('lo_id') for l in los]

    # embed LOs
    lo_emb = _lazy_embed(lo_texts, model_name=model_name)
    backend, index = _build_index(lo_emb)

    assets = load_catalog_texts()
    suggestions = []
    for asset_id, text in assets:
        if not text or len(text.strip()) < 10:
            # skip empty/placeholder assets
            continue
        q_emb = _lazy_embed([text], model_name=model_name)
        idxs, scores = _query_index(index, backend, q_emb, top_k=top_k)
        candidates = []
        for i, s in zip(idxs, scores):
            candidates.append({
                'lo_id': lo_ids[int(i)],
                'score': float(s)
            })
        suggestions.append({
            'asset_id': asset_id,
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'candidates': candidates
        })

    out = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'model': model_name,
        'top_k': top_k,
        'suggestions': suggestions
    }
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f'Wrote suggestions to {OUTPUT_PATH}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--top', type=int, default=3)
    parser.add_argument('--model', type=str, default='all-MiniLM-L6-v2')
    args = parser.parse_args()
    run(top_k=args.top, model_name=args.model)
