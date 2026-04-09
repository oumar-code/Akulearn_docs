#!/usr/bin/env bash
# migrate-to-aku-content.sh — Copy content/ and content_templates/ to oumar-code/Aku-Content
#
# Usage (run from the Akulearn_docs repo root — must have local content/ present):
#   chmod +x docs/service-migrations/migrate-to-aku-content.sh
#
#   # Dry-run — preview every step without making changes
#   ./docs/service-migrations/migrate-to-aku-content.sh --dry-run
#
#   # Live run — clones Aku-Content, initialises Git LFS, copies content, opens PR
#   ./docs/service-migrations/migrate-to-aku-content.sh
#
# Prerequisites:
#   - gh CLI installed and authenticated (gh auth status)
#   - git and git-lfs installed
#   - content/ and content_templates/ present locally (they are gitignored in Akulearn_docs)
#
# Migration tracker: docs/ecosystem-map.md — Content & Classroom App Migration Checklists

set -euo pipefail

GITHUB_ORG="oumar-code"
TARGET_REPO="Aku-Content"
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

# Git LFS tracked extensions
LFS_EXTENSIONS=("*.glb" "*.unitypackage" "*.pdf" "*.mp4" "*.zip" "*.zim" "*.fbx" "*.obj" "*.png" "*.jpg")

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
command -v gh   >/dev/null || { echo "❌ gh CLI not found. Install: https://cli.github.com"; exit 1; }
command -v git  >/dev/null || { echo "❌ git not found"; exit 1; }
command -v git-lfs >/dev/null || { echo "❌ git-lfs not found. Install: https://git-lfs.com"; exit 1; }

MONOREPO_ROOT="$(git rev-parse --show-toplevel)"
CONTENT_SRC="${MONOREPO_ROOT}/content"
TEMPLATES_SRC="${MONOREPO_ROOT}/content_templates"

[[ -d "$CONTENT_SRC" ]]   || { echo "❌ content/ directory not found at ${CONTENT_SRC}. Ensure it is present locally."; exit 1; }
[[ -d "$TEMPLATES_SRC" ]] || { echo "❌ content_templates/ directory not found at ${TEMPLATES_SRC}. Ensure it is present locally."; exit 1; }

echo "✅ Source directories confirmed:"
echo "   ${CONTENT_SRC}"
echo "   ${TEMPLATES_SRC}"

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

# ── Copy content ──────────────────────────────────────────────────────────────

echo ""
echo "📂 Copying content/ tree..."
run cp -r "${CONTENT_SRC}" "${TARGET_CLONE}/content"

echo "📂 Copying content_templates/ tree..."
run cp -r "${TEMPLATES_SRC}" "${TARGET_CLONE}/content_templates"

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
echo "   1. Review the PR in https://github.com/${GITHUB_ORG}/${TARGET_REPO}"
echo "   2. Merge the PR once content integrity is confirmed"
echo "   3. Update Akudemy and Aku-EdgeHub to reference ${TARGET_REPO}"
echo "   4. Remove content/ and content_templates/ from Akulearn_docs"
echo "   5. Update docs/ecosystem-map.md migration checklist"
