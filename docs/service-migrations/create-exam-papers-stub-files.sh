#!/usr/bin/env bash
# create-exam-papers-stub-files.sh — Write stub files for the Akudemy exam papers migration
#
# Called by .github/workflows/stub-akudemy-exam-papers.yml
# Usage: bash create-exam-papers-stub-files.sh <target-clone-dir>

set -euo pipefail

TARGET_CLONE="${1:?Usage: $0 <target-clone-dir>}"

# ── data/exam_papers/.gitkeep ─────────────────────────────────────────────────

mkdir -p "${TARGET_CLONE}/data/exam_papers"
cat > "${TARGET_CLONE}/data/exam_papers/.gitkeep" << 'EOF'
# Placeholder — full dataset (1,350 questions) to be added via full migration.
# Run: ./docs/service-migrations/migrate-exam-papers.sh (from a local machine
# with data/exam_papers/ and mlops/exam_paper_scraper.py present)
EOF
echo "✅ Written: data/exam_papers/.gitkeep"

# ── scripts/exam_paper_scraper.py (stub) ──────────────────────────────────────

mkdir -p "${TARGET_CLONE}/scripts"
cat > "${TARGET_CLONE}/scripts/exam_paper_scraper.py" << 'EOF'
"""
exam_paper_scraper.py — Placeholder

The full scraper will be added when the complete exam papers migration is run
from a local machine with mlops/exam_paper_scraper.py present.

Migration tracker:
  https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md

Usage (once the full file is in place):
  pip install -r requirements.txt
  python scripts/exam_paper_scraper.py --output data/exam_papers/
"""
raise NotImplementedError(
    "Full scraper not yet migrated. See module docstring for migration instructions."
)
EOF
echo "✅ Written: scripts/exam_paper_scraper.py (stub)"

# ── scripts/README.md ─────────────────────────────────────────────────────────

cat > "${TARGET_CLONE}/scripts/README.md" << 'EOF'
# Akudemy Scripts

## exam_paper_scraper.py

Generates `data/exam_papers/` — 1,350 structured WAEC/NECO/JAMB questions.

> **Status**: Full migration pending. The stub file is a placeholder.
> Run `./docs/service-migrations/migrate-exam-papers.sh` from a local machine
> with `data/exam_papers/` and `mlops/exam_paper_scraper.py` present to complete
> the migration.

### Usage (once migrated)

```bash
pip install -r requirements.txt
python scripts/exam_paper_scraper.py --output data/exam_papers/
```

### Output

| File | Description |
|------|-------------|
| `data/exam_papers/INDEX.json` | Dataset manifest — 1,350 questions, 4 subjects, 27 topics |
| `data/exam_papers/<subject>/` | Per-subject JSON question files |
| `data/exam_papers/<subject>.csv` | Per-subject CSV question files |

### Data Sources

Scrapes and structures publicly available past questions from WAEC, NECO, and JAMB (2020–2024).
Covers: Mathematics, English Language, Physics, Chemistry.

See `EXAM_SCRAPER_DELIVERABLES.md` for full specification (added during full migration).
EOF
echo "✅ Written: scripts/README.md"
