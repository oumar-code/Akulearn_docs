"""
Inspect file headers and attempt PDF text extraction using multiple libraries.

- Prints magic bytes and basic header info for each target file.
- Tries pypdf/PyPDF2 extraction (already in repo), then tries pdfminer.six if available.
- Writes recovered text to `runs/recovered_texts/<filename>.txt` when extraction succeeds.

Usage:
    python -m mlops.pdf_repair_and_extract content/textbooks/math_grade6.pdf
"""
from pathlib import Path
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pdf_repair")

try:
    from pypdf import PdfReader
except Exception:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        PdfReader = None

try:
    # pdfminer.six import
    from pdfminer.high_level import extract_text as pdfminer_extract_text
except Exception:
    pdfminer_extract_text = None


def inspect_file(path: Path):
    info = {}
    with open(path, 'rb') as f:
        head = f.read(64)
        info['magic_bytes'] = head[:8].hex()
        info['head_ascii'] = repr(head[:64])
    try:
        info['size'] = path.stat().st_size
    except Exception:
        info['size'] = None
    return info


def try_pypdf(path: Path):
    if PdfReader is None:
        logger.info('pypdf/PyPDF2 not installed')
        return None
    try:
        reader = PdfReader(str(path))
        text = []
        for p in reader.pages:
            t = p.extract_text() or ""
            text.append(t)
        return "\n".join(text).strip()
    except Exception as e:
        logger.warning(f'pypdf extraction failed: {e}')
        return None


def try_pdfminer(path: Path):
    if pdfminer_extract_text is None:
        logger.info('pdfminer not available')
        return None
    try:
        text = pdfminer_extract_text(str(path))
        return text.strip()
    except Exception as e:
        logger.warning(f'pdfminer extraction failed: {e}')
        return None


def main():
    args = sys.argv[1:]
    if not args:
        print('Usage: python -m mlops.pdf_repair_and_extract <file1> [file2 ...]')
        sys.exit(1)
    root = Path(__file__).resolve().parents[1]
    out_dir = root / 'runs' / 'recovered_texts'
    out_dir.mkdir(parents=True, exist_ok=True)

    for p in args:
        path = Path(p)
        if not path.exists():
            # try relative to repo
            path = (root / p)
        if not path.exists():
            logger.error(f'File not found: {p}')
            continue
        logger.info(f'Inspecting: {path}')
        info = inspect_file(path)
        logger.info(f"Magic bytes: {info['magic_bytes']}")
        logger.info(f"Header (ascii repr): {info['head_ascii']}")
        logger.info(f"Size: {info['size']}")

        recovered = None
        # Try pypdf first
        recovered = try_pypdf(path)
        if recovered:
            out = out_dir / (path.name + '.txt')
            out.write_text(recovered, encoding='utf-8')
            logger.info(f'Extracted text via pypdf to {out}')
            continue
        # Try pdfminer
        recovered = try_pdfminer(path)
        if recovered:
            out = out_dir / (path.name + '.txt')
            out.write_text(recovered, encoding='utf-8')
            logger.info(f'Extracted text via pdfminer to {out}')
            continue
        logger.warning('No extraction succeeded for {path}')

if __name__ == '__main__':
    main()
