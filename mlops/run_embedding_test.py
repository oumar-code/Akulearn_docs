import shutil
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'content' / 'catalog.json'
BACKUP = ROOT / 'content' / 'catalog.json.bak'

sample = [
    {
        "path": "content/sample_asset.txt",
        "text": "Right-angled triangles: the Pythagorean theorem states that in a right-angled triangle, the square of the hypotenuse equals the sum of the squares of the other two sides."
    }
]

def main():
    if not CATALOG.exists():
        CATALOG.parent.mkdir(parents=True, exist_ok=True)
    # backup if exists
    if CATALOG.exists():
        shutil.copy2(CATALOG, BACKUP)
    try:
        with open(CATALOG, 'w', encoding='utf-8') as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)
        # run the embedding auto-tagging
        from mlops import auto_tagging_embeddings as at
        print('Running embedding auto-tagging (test)')
        at.run(top_k=3)
        print('Embedding test completed — suggestions written to content/auto_tag_suggestions.json')
    except Exception as e:
        print('Embedding test failed:', e)
        raise
    finally:
        # restore backup
        if BACKUP.exists():
            shutil.move(str(BACKUP), str(CATALOG))

if __name__ == '__main__':
    main()
