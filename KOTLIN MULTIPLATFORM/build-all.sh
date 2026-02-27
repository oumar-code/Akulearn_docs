#!/bin/bash
set -e

echo "🔨 Building shared module..."
./gradlew :shared:build

echo "📱 Building Android debug APK..."
./gradlew :androidApp:assembleDebug

echo "🧪 Running shared tests..."
./gradlew :shared:allTests

echo ""
echo "✅ All builds successful."
echo "📦 APK: androidApp/build/outputs/apk/debug/androidApp-debug.apk"
