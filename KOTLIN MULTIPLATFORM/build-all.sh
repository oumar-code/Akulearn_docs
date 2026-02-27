#!/usr/bin/env bash
# build-all.sh — Build all Kotlin Multiplatform targets for the Akulearn shared module
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Building Android..."
./gradlew :shared:assembleDebug

echo "Building iOS frameworks..."
./gradlew :shared:linkDebugFrameworkIosArm64
./gradlew :shared:linkDebugFrameworkIosX64
./gradlew :shared:linkDebugFrameworkIosSimulatorArm64

echo "All targets built successfully."
