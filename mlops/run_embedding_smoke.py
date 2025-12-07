"""Safe embedding smoke-runner

Backs up content/catalog.json (if present), writes a small test catalog with one asset
that contains clear text, runs the embedding auto-tagger, prints the generated suggestions,
then restores the original catalog file.
"""
from pathlib import Path
import json
import shutil
import sys
from mlops import auto_tagging_embeddings

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'content' / 'catalog.json'
BACKUP = ROOT / 'content' / 'catalog.json.bak'


def write_test_catalog():
    data = {
        'items': [
            {
                'path': 'tests/asset1.txt',
                'text': 'Solve quadratic equations by factorization and the quadratic formula. Examples include ax^2+bx+c=0.'
            }
        ]
    }
    with open(CATALOG, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    # backup
    if CATALOG.exists():
        shutil.copy2(CATALOG, BACKUP)
        backed = True
    else:
        backed = False

    try:
        write_test_catalog()
        print('Wrote temporary test catalog to', CATALOG)
        # call embedding tagger
        auto_tagging_embeddings.run(top_k=3)
        out = ROOT / 'content' / 'auto_tag_suggestions.json'
        if out.exists():
            print('--- Suggestions ---')
            print(out.read_text(encoding='utf-8'))
        else:
            print('No suggestions file produced')
    except Exception as e:
        print('Error during embedding smoke run:', e)
        raise
    finally:
        # restore
        if backed and BACKUP.exists():
            shutil.move(str(BACKUP), str(CATALOG))
            print('Restored original catalog')
        else:
            # remove test catalog
            if CATALOG.exists():
                CATALOG.unlink()
                print('Removed temporary catalog')


if __name__ == '__main__':
    main()
