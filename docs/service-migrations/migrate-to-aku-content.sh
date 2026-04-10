#!/usr/bin/env bash
# migrate-to-aku-content.sh — Copy content/ and content_templates/ to oumar-code/Aku-Content
#
# Usage (run from the Akulearn_docs repo root):
#   chmod +x docs/service-migrations/migrate-to-aku-content.sh
#
#   # Show this help
#   ./docs/service-migrations/migrate-to-aku-content.sh --help
#
#   # Stub-only — push README + .gitattributes + empty directory structure (no local content needed)
#   ./docs/service-migrations/migrate-to-aku-content.sh --stub-only
#
#   # Stub-only dry-run
#   ./docs/service-migrations/migrate-to-aku-content.sh --stub-only --dry-run
#
#   # Full migration — clones Aku-Content, initialises Git LFS, copies content, opens PR
#   # ⚠️  MUST RUN FROM LOCAL MACHINE — requires content/ and content_templates/ present locally (gitignored)
#   ./docs/service-migrations/migrate-to-aku-content.sh
#
#   # Full migration dry-run
#   ./docs/service-migrations/migrate-to-aku-content.sh --dry-run
#
# Prerequisites (full migration):
#   - gh CLI installed and authenticated (gh auth status)
#   - git and git-lfs installed
#   - content/ and content_templates/ present locally (they are gitignored in Akulearn_docs)
#
# Prerequisites (--stub-only, can run in CI):
#   - gh CLI installed and authenticated — or GH_TOKEN/GH_PAT env var set
#   - git and git-lfs installed
#
# Migration tracker: docs/ecosystem-map.md — Content & Classroom App Migration Checklists

set -euo pipefail

GITHUB_ORG="oumar-code"
TARGET_REPO="Aku-Content"

# Git LFS tracked extensions
LFS_EXTENSIONS=("*.glb" "*.unitypackage" "*.pdf" "*.mp4" "*.zip" "*.zim" "*.fbx" "*.obj" "*.png" "*.jpg")

# ── Flag parsing ──────────────────────────────────────────────────────────────

DRY_RUN=false
STUB_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --help|-h)
      cat << 'HELP'
migrate-to-aku-content.sh — Migrate content library from Akulearn_docs to Aku-Content

MODES
  (no flags)     Full migration — initialises Git LFS, copies content/ + content_templates/.
                 ⚠️  MUST RUN FROM LOCAL MACHINE — requires the gitignored directories.

  --stub-only    Stub-only — pushes README + .gitattributes (LFS rules) + empty directory
                 structure WITHOUT needing local content. Good for initialising the target
                 repo with LFS configuration before the actual content is available.
                 Can be run from any machine or GitHub Actions (set GH_PAT env var).

  --dry-run      Preview every step without making any changes (works with both modes).
  --help, -h     Show this help message.

USAGE EXAMPLES
  # Stub-only (no local content needed — can run in CI):
  ./docs/service-migrations/migrate-to-aku-content.sh --stub-only

  # Full migration (run from local machine with content/ and content_templates/ present):
  ./docs/service-migrations/migrate-to-aku-content.sh

  # Full migration dry-run:
  ./docs/service-migrations/migrate-to-aku-content.sh --dry-run

LOCAL MACHINE SETUP (full migration only)
  The following directories are gitignored in Akulearn_docs and exist only locally:
    - content/              (100+ files: textbooks, AR, VR, simulations, etc.)
    - content_templates/    (8 WAEC/NERDC subject CSV templates)

  Steps:
  1. Ensure content/ and content_templates/ are present in your local Akulearn_docs clone
     (restore from your local drive or team file storage)
  2. Install gh CLI:    https://cli.github.com
  3. Install git-lfs:   https://git-lfs.com
  4. Authenticate:      gh auth login
  5. Run from the Akulearn_docs repo root:
       ./docs/service-migrations/migrate-to-aku-content.sh

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
  BRANCH_NAME="feat/content-repo-stub"
  COMMIT_MSG="feat: initialise Aku-Content with LFS config, README, and directory structure"
  PR_TITLE="feat: initialise Aku-Content with Git LFS config, README, and directory structure"
  PR_BODY="Sets up the Aku-Content repo with Git LFS configuration, README, and empty directory structure.

## What's included
- \`.gitattributes\` — Git LFS rules for all binary asset types (.glb, .unitypackage, .pdf, .mp4, .zip, .zim)
- \`README.md\` — repo documentation and Git LFS usage guide
- Empty directory structure with \`.gitkeep\` placeholders:
  \`content/textbooks/\`, \`content/ar/\`, \`content/vr/\`, \`content/simulations/\`,
  \`content/flashcards/\`, \`content/quizzes/\`, \`content/games/\`, \`content/encyclopedia/\`,
  \`content/tools/\`, \`content/news_corpus/\`, \`content_templates/\`

## What's NOT included yet
The actual content files are gitignored in the Akulearn_docs monorepo and must be copied
separately from a local machine.

Run \`./docs/service-migrations/migrate-to-aku-content.sh\` (full migration, local machine) once
\`content/\` and \`content_templates/\` are available locally.

## Next steps
1. Merge this PR to initialise LFS and directory structure
2. Restore content/ and content_templates/ locally and run the full migration
3. Update Akudemy and Aku-EdgeHub to reference this repo

Migration tracker: https://github.com/${GITHUB_ORG}/Akulearn_docs/blob/main/docs/ecosystem-map.md
"
else
  BRANCH_NAME="feat/initial-content-migration"
  COMMIT_MSG="feat: initial content migration from Akulearn_docs"
  PR_TITLE="feat: initial content migration from Akulearn_docs monorepo"
  PR_BODY="Automated migration of \`content/\` and \`content_templates/\` from the Akulearn_docs monorepo.

## What's included
- \`content/\` tree: AI-generated textbooks (9 subjects × SS1), AR/VR assets (.glb, .unitypackage), simulations, flashcards, quizzes, games, offline Wikipedia (.zim), multilingual news corpus (EN/HA/YO), parallel translation corpora
- \`content_templates/\` CSV templates: 8 WAEC/NERDC subject lesson plan templates
- \`.gitattributes\` with Git LFS rules for binary assets (.glb, .unitypackage, .pdf, .mp4, .zip)

## Next steps
1. Confirm content integrity (spot-check a few files)
2. Update Akudemy and Aku-EdgeHub to clone/submodule this repo instead of reading from local content/
3. Merge this PR, then remove content/ and content_templates/ from Akulearn_docs
4. Update docs/ecosystem-map.md migration checklist accordingly

Migration tracker: https://github.com/${GITHUB_ORG}/Akulearn_docs/blob/main/docs/ecosystem-map.md
"
fi

if $DRY_RUN; then
  echo "🔍 DRY-RUN mode — no changes will be made"
fi
$STUB_ONLY && echo "🔧 STUB-ONLY mode — skipping local content copy"

run() {
  if $DRY_RUN; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

# ── Validate prerequisites ────────────────────────────────────────────────────

echo "✅ Checking prerequisites..."
command -v gh   >/dev/null || { echo "❌ gh CLI not found. Install: https://cli.github.com"; exit 1; }
command -v git  >/dev/null || { echo "❌ git not found"; exit 1; }
command -v git-lfs >/dev/null || { echo "❌ git-lfs not found. Install: https://git-lfs.com"; exit 1; }

MONOREPO_ROOT="$(git rev-parse --show-toplevel)"

if ! $STUB_ONLY; then
  CONTENT_SRC="${MONOREPO_ROOT}/content"
  TEMPLATES_SRC="${MONOREPO_ROOT}/content_templates"

  MISSING=false
  [[ ! -d "$CONTENT_SRC" ]]   && MISSING=true
  [[ ! -d "$TEMPLATES_SRC" ]] && MISSING=true

  if $MISSING; then
    cat >&2 << 'LOCAL_MACHINE_ERR'

❌ MUST RUN FROM LOCAL MACHINE
─────────────────────────────────────────────────────────────────────────────
One or more required directories were not found:

  content/            — 100+ content files (textbooks, AR, VR, simulations, etc.)
  content_templates/  — 8 WAEC/NERDC subject CSV lesson templates

These are gitignored and exist only on a developer's local machine.
The full migration CANNOT run in a fresh git clone or CI environment.

TO RUN THE FULL MIGRATION:
  1. Restore content/ and content_templates/ to your local Akulearn_docs clone
     (copy from your local drive or team file storage)
  2. Install gh CLI:    https://cli.github.com
  3. Install git-lfs:   https://git-lfs.com
  4. Authenticate:      gh auth login
  5. Run from the Akulearn_docs repo root:
       ./docs/service-migrations/migrate-to-aku-content.sh

ALTERNATIVE — initialise the repo with LFS config and empty directory structure:
  ./docs/service-migrations/migrate-to-aku-content.sh --stub-only
  Or trigger the "Aku-Content — Initialise Stub" GitHub Actions workflow
  from the Akulearn_docs Actions tab (requires GH_PAT secret).
─────────────────────────────────────────────────────────────────────────────
LOCAL_MACHINE_ERR
    exit 1
  fi

  echo "✅ Source directories confirmed:"
  echo "   ${CONTENT_SRC}"
  echo "   ${TEMPLATES_SRC}"
fi

# ── Clone target repo ─────────────────────────────────────────────────────────

WORK_DIR="$(mktemp -d)"
TARGET_CLONE="${WORK_DIR}/${TARGET_REPO}"
echo ""
echo "📁 Cloning ${GITHUB_ORG}/${TARGET_REPO} into ${TARGET_CLONE}..."
run gh repo clone "${GITHUB_ORG}/${TARGET_REPO}" "${TARGET_CLONE}"

cd "${TARGET_CLONE}"
run git checkout -b "${BRANCH_NAME}"

# ── Configure Git LFS ─────────────────────────────────────────────────────────

echo ""
echo "📦 Configuring Git LFS..."
run git lfs install

GITATTRIBUTES="${TARGET_CLONE}/.gitattributes"
if ! $DRY_RUN; then
  {
    echo "# Git LFS — binary content assets"
    for ext in "${LFS_EXTENSIONS[@]}"; do
      echo "${ext} filter=lfs diff=lfs merge=lfs -text"
    done
  } > "${GITATTRIBUTES}"
  echo "   Written: .gitattributes"
else
  echo "[dry-run] Would write .gitattributes with LFS rules for: ${LFS_EXTENSIONS[*]}"
fi

if $STUB_ONLY; then
  # ── Stub mode: create empty directory structure ───────────────────────────

  echo ""
  echo "📂 Creating empty directory structure with .gitkeep placeholders..."
  CONTENT_DIRS=(
    "content/textbooks"
    "content/ar"
    "content/vr"
    "content/simulations"
    "content/flashcards"
    "content/quizzes"
    "content/games"
    "content/encyclopedia"
    "content/tools"
    "content/news_corpus"
    "content_templates"
  )
  for dir in "${CONTENT_DIRS[@]}"; do
    run mkdir -p "${TARGET_CLONE}/${dir}"
    if ! $DRY_RUN; then
      cat > "${TARGET_CLONE}/${dir}/.gitkeep" << 'EOF'
# Placeholder — actual content to be added via full migration.
# Run: ./docs/service-migrations/migrate-to-aku-content.sh (from a local machine
# with content/ and content_templates/ present)
EOF
      echo "   Created: ${dir}/.gitkeep"
    fi
  done

else
  # ── Full mode: copy content ────────────────────────────────────────────────

  echo ""
  echo "📂 Copying content/ tree..."
  run cp -r "${CONTENT_SRC}" "${TARGET_CLONE}/content"

  echo "📂 Copying content_templates/ tree..."
  run cp -r "${TEMPLATES_SRC}" "${TARGET_CLONE}/content_templates"
fi

# ── Create README if absent ───────────────────────────────────────────────────

if [[ ! -f "${TARGET_CLONE}/README.md" ]] && ! $DRY_RUN; then
  cat > "${TARGET_CLONE}/README.md" << 'EOF'
# Aku-Content

Offline content library for the Aku Platform — consumed by **Akudemy** and **Aku-EdgeHub**.

## Contents

| Directory | Description |
|-----------|-------------|
| `content/textbooks/` | AI-generated WAEC textbooks — 9 subjects × SS1 (JSON + MD) |
| `content/ar/` | Augmented Reality assets (.glb) |
| `content/vr/` | Virtual Reality scene packages (.unitypackage) |
| `content/simulations/` | Interactive science simulations |
| `content/flashcards/` | Subject flashcard decks |
| `content/quizzes/` | Formative assessment question banks |
| `content/games/` | Gamified learning modules |
| `content/encyclopedia/` | Offline Wikipedia (.zim) |
| `content/tools/` | Interactive learning tools |
| `content/news_corpus/` | Multilingual news corpus (EN/HA/YO) + translation corpora |
| `content_templates/` | WAEC/NERDC lesson CSV templates (8 subjects) |

## Git LFS

Binary assets (`.glb`, `.unitypackage`, `.pdf`, `.mp4`, `.zip`, `.zim`) are tracked via **Git LFS**.
Run `git lfs install` and `git lfs pull` after cloning.

## Usage in Other Repos

Clone or submodule this repo to make content available offline:

```bash
# As a submodule
git submodule add https://github.com/oumar-code/Aku-Content content
git lfs install && git lfs pull
```

## Source

Migrated from `Akulearn_docs` monorepo — see [migration tracker](https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md).
EOF
  echo "   Written: README.md"
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
  echo "   2. Merge this PR to initialise LFS and directory structure"
  echo "   3. Restore content/ and content_templates/ locally and run the full migration"
  echo "   4. Update Akudemy and Aku-EdgeHub to reference ${TARGET_REPO}"
else
  echo "   1. Review the PR in https://github.com/${GITHUB_ORG}/${TARGET_REPO}"
  echo "   2. Merge the PR once content integrity is confirmed"
  echo "   3. Update Akudemy and Aku-EdgeHub to reference ${TARGET_REPO}"
  echo "   4. Remove content/ and content_templates/ from Akulearn_docs"
  echo "   5. Update docs/ecosystem-map.md migration checklist"
fi
