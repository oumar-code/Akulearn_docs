#!/usr/bin/env bash
# write-akudemy-scripts-readme.sh — Write scripts/README.md for the Akudemy migration
#
# Called by .github/workflows/migrate-exam-papers-full.yml
# Extracted into a helper script to avoid YAML/heredoc indentation incompatibility.
#
# Usage: bash write-akudemy-scripts-readme.sh <target-clone-dir>
#   <target-clone-dir>  — root of the cloned Akudemy repo

set -euo pipefail

TARGET_CLONE="${1:?Usage: $0 <target-clone-dir>}"

mkdir -p "${TARGET_CLONE}/scripts"

cat > "${TARGET_CLONE}/scripts/README.md" << 'EOF'
# Akudemy Scripts

## exam_paper_scraper.py

Generates `data/exam_papers/` — 1,350 structured WAEC/NECO/JAMB questions.

### Usage

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

See `EXAM_SCRAPER_DELIVERABLES.md` for full specification.
EOF

echo "✅ Written: scripts/README.md"
