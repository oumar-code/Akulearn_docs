"""Clean BOM CSV by ensuring exactly 10 columns per row.

If a row has more than 10 fields, extra fields are merged into the last (Notes) column.
If fewer than 10, empty strings are appended.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOM = ROOT / 'hardware' / 'boms' / 'edge_alpha_bom.csv'


def clean_bom(path: Path):
    if not path.exists():
        print('BOM not found at', path)
        return False
    cleaned = []
    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0] if rows else []
    cleaned.append(header[:10] + ([''] * (10 - len(header))) if len(header) < 10 else header[:10])

    for r in rows[1:]:
        if len(r) == 10:
            cleaned.append(r)
        elif len(r) < 10:
            cleaned.append(r + [''] * (10 - len(r)))
        else:
            # more than 10 columns: keep first 9, join the rest into notes
            first9 = r[:9]
            notes = ','.join(r[9:]).strip()
            first9.append(notes)
            cleaned.append(first9)

    # write back
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(cleaned)

    print('Cleaned BOM written to', path)
    return True


if __name__ == '__main__':
    clean_bom(BOM)
