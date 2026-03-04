#!/usr/bin/env bash
# setup.sh — Akulearn project setup helper
#
# Integrates team.py, supabase_provision.py, and README.md from source
# control into the project directory and prepares the environment for use.
#
# Usage:
#   chmod +x setup.sh
#   ./setup.sh

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "=== Akulearn Project Setup ==="
echo ""

# ---------------------------------------------------------------------------
# 1. Pull latest files from source control
# ---------------------------------------------------------------------------
echo "1. Pulling latest files from source control..."
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git fetch origin
    git merge --ff-only origin/main 2>/dev/null || \
        echo "   (already up-to-date or on a feature branch — skipping merge)"
else
    echo "   Not a git repository — skipping pull."
fi

# ---------------------------------------------------------------------------
# 2. Verify the key files are present
# ---------------------------------------------------------------------------
echo ""
echo "2. Verifying required files..."
MISSING=0
for f in team.py supabase_provision.py README.md; do
    if [[ -f "$f" ]]; then
        echo "   ✔  $f"
    else
        echo "   ✘  $f — NOT FOUND (check your source branch)"
        MISSING=1
    fi
done

if [[ "$MISSING" -eq 1 ]]; then
    echo ""
    echo "ERROR: One or more required files are missing."
    echo "       Run the following commands to retrieve them from source control:"
    echo "         git fetch origin"
    echo "         git checkout origin/main -- team.py supabase_provision.py README.md"
    exit 1
fi

# ---------------------------------------------------------------------------
# 3. Install Python dependencies
# ---------------------------------------------------------------------------
echo ""
echo "3. Installing Python dependencies..."
if [[ ! -f "requirements.txt" ]]; then
    echo "   WARNING: requirements.txt not found — skipping dependency install."
    echo "            Retrieve it from source control:"
    echo "              git checkout origin/main -- requirements.txt"
elif command -v pip3 &>/dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &>/dev/null; then
    pip install -r requirements.txt
else
    echo "   WARNING: pip not found — please install Python and pip, then run:"
    echo "     pip install -r requirements.txt"
fi

# ---------------------------------------------------------------------------
# 4. Set up .env if not already present
# ---------------------------------------------------------------------------
echo ""
echo "4. Setting up environment configuration..."
if [[ ! -f ".env" ]]; then
    if [[ ! -f ".env.example" ]]; then
        echo "   WARNING: .env.example not found — cannot create .env."
        echo "            Retrieve it from source control:"
        echo "              git checkout origin/main -- .env.example"
    else
        cp .env.example .env
        echo "   .env created from .env.example"
        echo "   → Open .env and fill in SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY"
    fi
else
    echo "   .env already exists — skipping"
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  python team.py                # view team roster and dashboard assignments"
echo "  python supabase_provision.py  # provision team members in Supabase"
echo ""
echo "  (Set SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY in .env before provisioning)"
