#!/usr/bin/env bash
# migrate-exam-papers.sh — Copy data/exam_papers/ and mlops/exam_paper_scraper.py to oumar-code/Akudemy
#
# Usage (run from the Akulearn_docs repo root):
#   chmod +x docs/service-migrations/migrate-exam-papers.sh
#
#   # Show this help
#   ./docs/service-migrations/migrate-exam-papers.sh --help
#
#   # Stub-only — push scripts/README.md and data/exam_papers placeholder to Akudemy (no local data needed)
#   ./docs/service-migrations/migrate-exam-papers.sh --stub-only
#
#   # Stub-only dry-run
#   ./docs/service-migrations/migrate-exam-papers.sh --stub-only --dry-run
#
#   # Full migration — clones Akudemy, copies exam papers and scraper, opens PR
#   # ⚠️  MUST RUN FROM LOCAL MACHINE — requires data/exam_papers/ and mlops/ present locally (gitignored)
#   ./docs/service-migrations/migrate-exam-papers.sh
#
#   # Full migration dry-run
#   ./docs/service-migrations/migrate-exam-papers.sh --dry-run
#
# Prerequisites (full migration):
#   - gh CLI installed and authenticated (gh auth status)
#   - git installed
#   - data/exam_papers/ and mlops/exam_paper_scraper.py present locally (gitignored in Akulearn_docs)
#
# Prerequisites (--stub-only, can run in CI):
#   - gh CLI installed and authenticated — or GH_TOKEN/GH_PAT env var set
#   - git installed
#
# Migration tracker: docs/ecosystem-map.md — Content & Classroom App Migration Checklists

set -euo pipefail

GITHUB_ORG="oumar-code"
TARGET_REPO="Akudemy"

# ── Flag parsing ──────────────────────────────────────────────────────────────

DRY_RUN=false
STUB_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --help|-h)
      cat << 'HELP'
migrate-exam-papers.sh — Migrate exam papers dataset from Akulearn_docs to Akudemy

MODES
  (no flags)     Full migration — copies data/exam_papers/ + scraper to Akudemy.
                 ⚠️  MUST RUN FROM LOCAL MACHINE — requires the gitignored directories.

  --stub-only    Stub-only — pushes scripts/README.md and a data/exam_papers/ placeholder
                 WITHOUT needing local data. Good for partially setting up the target repo.
                 Can be run from any machine or GitHub Actions (set GH_PAT env var).

  --dry-run      Preview every step without making any changes (works with both modes).
  --help, -h     Show this help message.

USAGE EXAMPLES
  # Stub-only (no local data needed — can run in CI):
  ./docs/service-migrations/migrate-exam-papers.sh --stub-only

  # Full migration (run from local machine with data/exam_papers/ and mlops/ present):
  ./docs/service-migrations/migrate-exam-papers.sh

  # Full migration dry-run:
  ./docs/service-migrations/migrate-exam-papers.sh --dry-run

LOCAL MACHINE SETUP (full migration only)
  The following directories are gitignored in Akulearn_docs and exist only locally:
    - data/exam_papers/          (1,350 JSON/CSV questions)
    - mlops/exam_paper_scraper.py

  Steps:
  1. Ensure data/exam_papers/ and mlops/ are present in your local Akulearn_docs clone
     (restore from your local drive or re-run the scraper)
  2. Install gh CLI:  https://cli.github.com
  3. Authenticate:    gh auth login
  4. Run from the Akulearn_docs repo root:
       ./docs/service-migrations/migrate-exam-papers.sh

  To regenerate the dataset locally:
    pip install -r requirements.txt
    python mlops/exam_paper_scraper.py --output data/exam_papers/

MIGRATION TRACKER
  https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md
HELP
      exit 0
      ;;
    --stub-only) STUB_ONLY=true ;;
    --dry-run)   DRY_RUN=true ;;
    *)
      echo "❌ Unknown flag: $arg  (use --help for usage)" >&2
      exit 1
      ;;
  esac
done

if $STUB_ONLY; then
  BRANCH_NAME="feat/exam-papers-stub"
  COMMIT_MSG="feat: add exam papers directory structure and scripts placeholder"
  PR_TITLE="feat: add exam papers directory structure and scraper placeholder to Akudemy"
  PR_BODY="Adds the directory structure and scripts placeholder for the exam papers migration.

## What's included
- \`data/exam_papers/.gitkeep\` — placeholder for the 1,350-question dataset
- \`scripts/exam_paper_scraper.py\` — stub with usage instructions
- \`scripts/README.md\` — usage guide for the scraper and dataset

## What's NOT included yet
The actual exam papers dataset (\`data/exam_papers/\`) is gitignored in the Akulearn_docs
monorepo and must be copied separately from a local machine.

Run \`./docs/service-migrations/migrate-exam-papers.sh\` (full migration, local machine) once
\`data/exam_papers/\` and \`mlops/exam_paper_scraper.py\` are available locally.

## Next steps
1. Merge this PR to set up the directory structure
2. Restore data/exam_papers/ locally and run the full migration
3. Wire \`data/exam_papers/\` into Akudemy's content API (\`routers/content.py\`)

Migration tracker: https://github.com/${GITHUB_ORG}/Akulearn_docs/blob/main/docs/ecosystem-map.md
"
else
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
fi

if $DRY_RUN; then
  echo "🔍 DRY-RUN mode — no changes will be made"
fi
$STUB_ONLY && echo "🔧 STUB-ONLY mode — skipping local data copy"

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

if ! $STUB_ONLY; then
  EXAM_PAPERS_SRC="${MONOREPO_ROOT}/data/exam_papers"
  SCRAPER_SRC="${MONOREPO_ROOT}/mlops/exam_paper_scraper.py"
  SCRAPER_DOCS_SRC="${MONOREPO_ROOT}/EXAM_SCRAPER_DELIVERABLES.md"

  MISSING=false
  if [[ ! -d "$EXAM_PAPERS_SRC" ]]; then
    MISSING=true
    MISSING_DATA=true
  fi
  if [[ ! -f "$SCRAPER_SRC" ]]; then
    MISSING=true
    MISSING_SCRAPER=true
  fi

  if $MISSING; then
    cat >&2 << 'LOCAL_MACHINE_ERR'

❌ MUST RUN FROM LOCAL MACHINE
─────────────────────────────────────────────────────────────────────────────
One or more required directories/files were not found:

  data/exam_papers/          — 1,350-question JSON/CSV dataset (gitignored)
  mlops/exam_paper_scraper.py — scraper that generated the dataset (gitignored)

These are gitignored and exist only on a developer's local machine.
The full migration CANNOT run in a fresh git clone or CI environment.

TO RUN THE FULL MIGRATION:
  1. Restore data/exam_papers/ and mlops/ to your local Akulearn_docs clone
     — restore from your local drive, OR re-run the scraper:
       pip install -r requirements.txt
       python mlops/exam_paper_scraper.py --output data/exam_papers/
  2. Install and authenticate the gh CLI:
       gh auth login
  3. Run from the Akulearn_docs repo root:
       ./docs/service-migrations/migrate-exam-papers.sh

ALTERNATIVE — push a stub structure without the actual data:
  ./docs/service-migrations/migrate-exam-papers.sh --stub-only
  Or trigger the "Akudemy — Exam Papers Stub" GitHub Actions workflow
  from the Akulearn_docs Actions tab (requires GH_PAT secret).
─────────────────────────────────────────────────────────────────────────────
LOCAL_MACHINE_ERR
    exit 1
  fi

  echo "✅ Source files confirmed:"
  echo "   ${EXAM_PAPERS_SRC}"
  echo "   ${SCRAPER_SRC}"
  [[ -f "$SCRAPER_DOCS_SRC" ]] && echo "   ${SCRAPER_DOCS_SRC}" || echo "   (EXAM_SCRAPER_DELIVERABLES.md not found — skipping)"
fi

# ── Clone target repo ─────────────────────────────────────────────────────────

WORK_DIR="$(mktemp -d)"
TARGET_CLONE="${WORK_DIR}/${TARGET_REPO}"
echo ""
echo "📁 Cloning ${GITHUB_ORG}/${TARGET_REPO} into ${TARGET_CLONE}..."
run gh repo clone "${GITHUB_ORG}/${TARGET_REPO}" "${TARGET_CLONE}"

cd "${TARGET_CLONE}"
run git checkout -b "${BRANCH_NAME}"

if $STUB_ONLY; then
  # ── Stub mode: create placeholder structure ───────────────────────────────

  echo ""
  echo "📂 Creating data/exam_papers/ placeholder..."
  run mkdir -p "${TARGET_CLONE}/data/exam_papers"
  if ! $DRY_RUN; then
    cat > "${TARGET_CLONE}/data/exam_papers/.gitkeep" << 'EOF'
# Placeholder — full dataset (1,350 questions) to be added via full migration.
# Run: ./docs/service-migrations/migrate-exam-papers.sh (from a local machine
# with data/exam_papers/ and mlops/exam_paper_scraper.py present)
EOF
    echo "   Written: data/exam_papers/.gitkeep"
  fi

  echo ""
  echo "📂 Creating scripts/ placeholder..."
  run mkdir -p "${TARGET_CLONE}/scripts"
  if ! $DRY_RUN; then
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
    echo "   Written: scripts/exam_paper_scraper.py (stub)"
  fi

else
  # ── Full mode: copy exam papers ────────────────────────────────────────────

  echo ""
  echo "📂 Copying data/exam_papers/ tree..."
  run mkdir -p "${TARGET_CLONE}/data"
  run cp -r "${EXAM_PAPERS_SRC}" "${TARGET_CLONE}/data/exam_papers"

  # ── Copy scraper and docs ─────────────────────────────────────────────────

  echo ""
  echo "📂 Copying mlops/exam_paper_scraper.py → scripts/..."
  run mkdir -p "${TARGET_CLONE}/scripts"
  run cp "${SCRAPER_SRC}" "${TARGET_CLONE}/scripts/exam_paper_scraper.py"

  if [[ -f "$SCRAPER_DOCS_SRC" ]] && ! $DRY_RUN; then
    cp "${SCRAPER_DOCS_SRC}" "${TARGET_CLONE}/scripts/EXAM_SCRAPER_DELIVERABLES.md"
    echo "   Copied EXAM_SCRAPER_DELIVERABLES.md"
  fi
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
if $STUB_ONLY; then
  echo "   1. Review the PR in https://github.com/${GITHUB_ORG}/${TARGET_REPO}"
  echo "   2. Merge this PR to set up the directory structure"
  echo "   3. Restore data/exam_papers/ locally and run the full migration"
  echo "   4. Wire data/exam_papers/ into Akudemy's content API"
else
  echo "   1. Review the PR in https://github.com/${GITHUB_ORG}/${TARGET_REPO}"
  echo "   2. Merge the PR once data integrity is confirmed"
  echo "   3. Wire data/exam_papers/ into Akudemy's content API"
  echo "   4. Remove data/exam_papers/ from Akulearn_docs"
  echo "   5. Update docs/ecosystem-map.md migration checklist"
fi
