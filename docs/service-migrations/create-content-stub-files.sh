#!/usr/bin/env bash
# create-content-stub-files.sh — Write stub files for the Aku-Content repo
#
# Called by .github/workflows/stub-aku-content.yml
# Usage: bash create-content-stub-files.sh <target-clone-dir>

set -euo pipefail

TARGET_CLONE="${1:?Usage: $0 <target-clone-dir>}"

# ── .gitattributes ────────────────────────────────────────────────────────────

cat > "${TARGET_CLONE}/.gitattributes" << 'EOF'
# Git LFS — binary content assets
*.glb filter=lfs diff=lfs merge=lfs -text
*.unitypackage filter=lfs diff=lfs merge=lfs -text
*.pdf filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
*.zim filter=lfs diff=lfs merge=lfs -text
*.fbx filter=lfs diff=lfs merge=lfs -text
*.obj filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
EOF
echo "✅ Written: .gitattributes"

# ── README.md ─────────────────────────────────────────────────────────────────

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

> **Status**: Directory structure initialised. Actual content pending full migration.
> See [migration tracker](https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md).

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
echo "✅ Written: README.md"

# ── Empty directory structure with .gitkeep placeholders ─────────────────────

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

GITKEEP_CONTENT='# Placeholder — actual content to be added via full migration.
# Run: ./docs/service-migrations/migrate-to-aku-content.sh (from a local machine
# with content/ and content_templates/ present)'

for dir in "${CONTENT_DIRS[@]}"; do
  mkdir -p "${TARGET_CLONE}/${dir}"
  printf '%s\n' "${GITKEEP_CONTENT}" > "${TARGET_CLONE}/${dir}/.gitkeep"
  echo "✅ Created: ${dir}/.gitkeep"
done
