"""
Simple content ingestion helper.

- Scans `content/textbooks` and `content/modules` for PDFs and ZIPs
- Lists files and reads first-page text when possible (PDFs)
- Lists members of ZIP files without extracting
- Writes a `content/catalog.json` with metadata (path, type, size, first_page_text)

Usage:
    python -m mlops.content_ingest --output content/catalog.json

This is a small starter tool to create an inventory we can map to syllabi.
"""
from pathlib import Path
import argparse
import json
import zipfile
import logging

try:
    # pypdf is preferred; try import, otherwise fall back to PdfReader from pypdf
    from pypdf import PdfReader
except Exception:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        PdfReader = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("content_ingest")

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
OUTPUT_DIR = ROOT / "content"


def read_first_page_text(pdf_path: Path) -> str:
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(str(pdf_path))
        if len(reader.pages) > 0:
            page = reader.pages[0]
            text = page.extract_text() or ""
            return text.strip().replace("\n", " ")[:2000]
    except Exception as e:
        logger.warning(f"Failed to read PDF {pdf_path}: {e}")
    return ""


def list_zip_members(zip_path: Path):
    try:
        with zipfile.ZipFile(str(zip_path), 'r') as z:
            return z.namelist()
    except Exception as e:
        logger.warning(f"Failed to read ZIP {zip_path}: {e}")
        return []


def scan_content() -> list:
    items = []
    # Walk textbooks and modules
    for sub in (CONTENT_DIR / "textbooks").iterdir():
        path = sub
        if path.is_file() and path.suffix.lower() == ".pdf":
            items.append({
                "path": str(path.relative_to(ROOT)),
                "type": "pdf",
                "size": path.stat().st_size,
                "first_page": read_first_page_text(path)
            })
        elif path.is_dir():
            # list files inside
            for f in path.rglob("*"):
                if f.is_file():
                    items.append({
                        "path": str(f.relative_to(ROOT)),
                        "type": f.suffix.lower().lstrip('.'),
                        "size": f.stat().st_size,
                        "first_page": read_first_page_text(f) if f.suffix.lower()=='.pdf' else ""
                    })
    # modules
    modules_dir = CONTENT_DIR / "modules"
    for sub in modules_dir.iterdir():
        path = sub
        if path.is_file() and path.suffix.lower() == ".zip":
            items.append({
                "path": str(path.relative_to(ROOT)),
                "type": "zip",
                "size": path.stat().st_size,
                "members": list_zip_members(path)
            })
        elif path.is_dir():
            for f in path.rglob("*"):
                items.append({
                    "path": str(f.relative_to(ROOT)),
                    "type": f.suffix.lower().lstrip('.'),
                    "size": f.stat().st_size,
                    "first_page": read_first_page_text(f) if f.suffix.lower()=='.pdf' else ""
                })
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUTPUT_DIR / "catalog.json"))
    args = parser.parse_args()

    catalog = scan_content()
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({"generated_at": "", "items": catalog}, f, indent=2)
    print(f"Wrote catalog with {len(catalog)} items to {out_path}")


if __name__ == '__main__':
    main()
