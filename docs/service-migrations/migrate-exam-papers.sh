#!/usr/bin/env bash
# migrate-exam-papers.sh — Copy data/exam_papers/ and mlops/exam_paper_scraper.py to oumar-code/Akudemy
#
# Usage (run from the Akulearn_docs repo root — must have local data/ and mlops/ present):
#   chmod +x docs/service-migrations/migrate-exam-papers.sh
#
#   # Dry-run — preview every step without making changes
#   ./docs/service-migrations/migrate-exam-papers.sh --dry-run
#
#   # Live run — clones Akudemy, copies exam papers and scraper, opens PR
#   ./docs/service-migrations/migrate-exam-papers.sh
#
# Prerequisites:
#   - gh CLI installed and authenticated (gh auth status)
#   - git installed
#   - data/exam_papers/ and mlops/exam_paper_scraper.py present locally (gitignored in Akulearn_docs)
#
# Migration tracker: docs/ecosystem-map.md — Content & Classroom App Migration Checklists

set -euo pipefail

GITHUB_ORG="oumar-code"
TARGET_REPO="Akudemy"
BRANCH_NAME="feat/exam-papers-migration"
COMMIT_MSG="feat: migrate exam papers and scraper from Akulearn_docs"
PR_TITLE="feat: migrate exam papers dataset and scraper from Akulearn_docs"
PR_BODY="Automated migration of \`data/exam_papers/\` and \`mlops/exam_paper_scraper.py\` from the Akulearn_docs monorepo.

## What's included
- \`data/exam_papers/\`: 1,350 structured exam questions — WAEC/NECO/JAMB, 4 subjects, 27 topics, 2020–2024 (JSON + CSV, see INDEX.json)
- \`scripts/exam_paper_scraper.py\`: scraper that generated the dataset (originally at mlops/exam_paper_scraper.py)
- \`scripts/README.md\`: usage instructions for the scraper

## Next steps
1. Confirm data integrity (spot-check data/exam_papers/INDEX.json)
2. Wire \`data/exam_papers/\` into Akudemy's content API (routers/content.py)
3. Schedule \`scripts/exam_paper_scraper.py\` as a periodic GitHub Actions job if needed
4. Merge this PR, then remove data/exam_papers/ from Akulearn_docs
5. Update docs/ecosystem-map.md migration checklist accordingly

Migration tracker: https://github.com/${GITHUB_ORG}/Akulearn_docs/blob/main/docs/ecosystem-map.md
"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "🔍 DRY-RUN mode — no changes will be made"
fi

run() {
  if $DRY_RUN; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

# ── Validate prerequisites ────────────────────────────────────────────────────

echo "✅ Checking prerequisites..."
command -v gh  >/dev/null || { echo "❌ gh CLI not found. Install: https://cli.github.com"; exit 1; }
command -v git >/dev/null || { echo "❌ git not found"; exit 1; }

MONOREPO_ROOT="$(git rev-parse --show-toplevel)"
EXAM_PAPERS_SRC="${MONOREPO_ROOT}/data/exam_papers"
SCRAPER_SRC="${MONOREPO_ROOT}/mlops/exam_paper_scraper.py"
SCRAPER_DOCS_SRC="${MONOREPO_ROOT}/EXAM_SCRAPER_DELIVERABLES.md"

[[ -d "$EXAM_PAPERS_SRC" ]]  || { echo "❌ data/exam_papers/ not found at ${EXAM_PAPERS_SRC}. Ensure it is present locally."; exit 1; }
[[ -f "$SCRAPER_SRC" ]]      || { echo "❌ mlops/exam_paper_scraper.py not found at ${SCRAPER_SRC}. Ensure it is present locally."; exit 1; }

echo "✅ Source files confirmed:"
echo "   ${EXAM_PAPERS_SRC}"
echo "   ${SCRAPER_SRC}"
[[ -f "$SCRAPER_DOCS_SRC" ]] && echo "   ${SCRAPER_DOCS_SRC}" || echo "   (EXAM_SCRAPER_DELIVERABLES.md not found — skipping)"

# ── Clone target repo ─────────────────────────────────────────────────────────

WORK_DIR="$(mktemp -d)"
TARGET_CLONE="${WORK_DIR}/${TARGET_REPO}"
echo ""
echo "📁 Cloning ${GITHUB_ORG}/${TARGET_REPO} into ${TARGET_CLONE}..."
run gh repo clone "${GITHUB_ORG}/${TARGET_REPO}" "${TARGET_CLONE}"

cd "${TARGET_CLONE}"
run git checkout -b "${BRANCH_NAME}"

# ── Copy exam papers ──────────────────────────────────────────────────────────

echo ""
echo "📂 Copying data/exam_papers/ tree..."
run mkdir -p "${TARGET_CLONE}/data"
run cp -r "${EXAM_PAPERS_SRC}" "${TARGET_CLONE}/data/exam_papers"

# ── Copy scraper and docs ─────────────────────────────────────────────────────

echo ""
echo "📂 Copying mlops/exam_paper_scraper.py → scripts/..."
run mkdir -p "${TARGET_CLONE}/scripts"
run cp "${SCRAPER_SRC}" "${TARGET_CLONE}/scripts/exam_paper_scraper.py"

if [[ -f "$SCRAPER_DOCS_SRC" ]] && ! $DRY_RUN; then
  cp "${SCRAPER_DOCS_SRC}" "${TARGET_CLONE}/scripts/EXAM_SCRAPER_DELIVERABLES.md"
  echo "   Copied EXAM_SCRAPER_DELIVERABLES.md"
fi

# ── Create scripts/README.md ──────────────────────────────────────────────────

if ! $DRY_RUN; then
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
  echo "   Written: scripts/README.md"
fi

# ── Commit and push ───────────────────────────────────────────────────────────

echo ""
echo "📤 Committing and pushing..."
run git add .
run git commit -m "${COMMIT_MSG}"
run git push -u origin "${BRANCH_NAME}"

# ── Open PR ───────────────────────────────────────────────────────────────────

echo ""
echo "🔀 Opening pull request..."
run gh pr create \
  --repo "${GITHUB_ORG}/${TARGET_REPO}" \
  --base main \
  --head "${BRANCH_NAME}" \
  --title "${PR_TITLE}" \
  --body "${PR_BODY}"

echo ""
echo "✅ Migration script complete!"
echo "   1. Review the PR in https://github.com/${GITHUB_ORG}/${TARGET_REPO}"
echo "   2. Merge the PR once data integrity is confirmed"
echo "   3. Wire data/exam_papers/ into Akudemy's content API"
echo "   4. Remove data/exam_papers/ from Akulearn_docs"
echo "   5. Update docs/ecosystem-map.md migration checklist"
