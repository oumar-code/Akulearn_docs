#!/usr/bin/env bash
# write-lfs-gitattributes.sh — Write .gitattributes with Git LFS rules
#
# Called by .github/workflows/migrate-aku-content-full.yml
# Extracted into a helper script to avoid YAML/heredoc indentation incompatibility.
#
# Usage: bash write-lfs-gitattributes.sh <target-dir>
#   <target-dir>  — root of the cloned Aku-Content repo

set -euo pipefail

TARGET_DIR="${1:?Usage: $0 <target-dir>}"

cat > "${TARGET_DIR}/.gitattributes" << 'EOF'
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
