# KMP Migration Runbook — `KOTLIN MULTIPLATFORM/` → `oumar-code/Aku-Mobile`

This runbook describes every step to move the existing KMP module out of the `Akulearn_docs` monorepo into a dedicated `oumar-code/Aku-Mobile` repository.

> **Decision recorded in:** [`docs/ecosystem-map.md — KMP Migration Checklist`](../ecosystem-map.md#kmp-migration-checklist)  
> **Tracking:** internal operations tracker (removed from this public repository)

---

## Current State

| Item | Location |
|------|----------|
| KMP shared library | `KOTLIN MULTIPLATFORM/shared/` |
| Android app module | `KOTLIN MULTIPLATFORM/androidApp/` |
| Build scripts | `KOTLIN MULTIPLATFORM/build-all.sh`, `settings.gradle.kts`, `build.gradle.kts` |
| Gradle wrapper | `KOTLIN MULTIPLATFORM/gradle/`, `gradlew`, `gradlew.bat` |
| Sprint plan | `KOTLIN MULTIPLATFORM/KMP SPRINT_PLAN.md` |

### Key Modules in `shared/`
- `com.akuplatform.shared.api` — `Wave3ApiClient` (HTTP client for Aku REST API)
- `com.akuplatform.shared.auth` — `AuthRepository`, `SessionManager`, `TokenStorage`, `AuthToken`

---

## Prerequisites

- JDK 17
- Android SDK (`ANDROID_HOME` or `local.properties`)
- Xcode (for iOS targets — macOS only)
- GitHub CLI (`gh`) or access to github.com/oumar-code

---

## Step 1 — Create `oumar-code/Aku-Mobile` on GitHub

```bash
# Using GitHub CLI
gh repo create oumar-code/Aku-Mobile \
  --public \
  --description "Aku Platform — Kotlin Multiplatform shared library for Android and iOS" \
  --homepage "https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md"
```

Or via GitHub UI:
1. Go to https://github.com/new
2. Owner: `oumar-code`, Name: `Aku-Mobile`
3. Description: `Aku Platform — KMP shared library for Android and iOS`
4. Public, no README (we'll push one)

---

## Step 2 — Copy Contents from `KOTLIN MULTIPLATFORM/`

Run this from the `Akulearn_docs` repo root:

```bash
# Create a staging directory
mkdir -p /tmp/aku-mobile-migration

# Copy everything from the KMP directory
cp -r "KOTLIN MULTIPLATFORM/." /tmp/aku-mobile-migration/

# Verify contents
ls -la /tmp/aku-mobile-migration/
```

---

## Step 3 — Initialise the New Repo and Push

```bash
cd /tmp/aku-mobile-migration

# Init git repo
git init
git add .
git commit -m "feat: initial KMP module migrated from oumar-code/Akulearn_docs"

# Add remote and push
git remote add origin https://github.com/oumar-code/Aku-Mobile.git
git branch -M main
git push -u origin main
```

---

## Step 4 — Add Repository Metadata

Create a proper `.gitignore` in the new repo:

```
# Gradle
.gradle/
build/
local.properties

# IDE
.idea/
*.iml

# KMP targets
*.klib
*.dSYM
```

Update `README.md` with a migration notice and getting-started instructions referencing this docs repo.

---

## Step 5 — Update This Docs Repo

### 5a — Update `docs/03-mobile/index.md`

Add a link to the new repo at the top of the mobile index.

### 5b — Update `docs/ecosystem-map.md`

Change the Mobile table row for `Aku-Mobile` from:
```
| [Aku-Mobile](https://github.com/oumar-code/Aku-Mobile) *(to create)* | ... | **Pending** |
```
to:
```
| [Aku-Mobile](https://github.com/oumar-code/Aku-Mobile) | ... | **Active** |
```

### 5c — Mark KMP checklist items done in `internal operations tracker`

---

## Step 6 — Verify Migration

```bash
# Clone new repo and verify it builds
git clone https://github.com/oumar-code/Aku-Mobile /tmp/aku-mobile-verify
cd /tmp/aku-mobile-verify

# Android build
./gradlew :shared:assembleDebug

# iOS framework (macOS only)
./gradlew :shared:linkDebugFrameworkIosArm64
```

---

## Step 7 — Remove `KOTLIN MULTIPLATFORM/` from Akulearn_docs

Only after the migration is confirmed working:

```bash
cd /path/to/Akulearn_docs

git rm -r "KOTLIN MULTIPLATFORM/"
git commit -m "chore: remove KOTLIN MULTIPLATFORM/ — migrated to oumar-code/Aku-Mobile"
git push origin main
```

> ⚠️ Do NOT remove it before confirming the new repo builds successfully.

---

## Step 8 — Add CI to Aku-Mobile

Add `.github/workflows/build.yml` to the new repo:

```yaml
name: Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: Build shared module (Android)
        run: ./gradlew :shared:assembleDebug

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"

      - name: Build iOS framework
        run: ./gradlew :shared:linkDebugFrameworkIosArm64
```

---

## Migration Checklist

- [ ] Create `oumar-code/Aku-Mobile` repository
- [ ] Copy `KOTLIN MULTIPLATFORM/` contents to new repo root
- [ ] Initial commit and push to `Aku-Mobile`
- [ ] Add `.gitignore` and CI workflow to `Aku-Mobile`
- [ ] Verify Android build passes in `Aku-Mobile`
- [ ] Update `docs/03-mobile/index.md` with link to `Aku-Mobile`
- [ ] Update `docs/ecosystem-map.md` — change status from Pending → Active
- [ ] Update `internal operations tracker` — mark KMP checklist items done
- [ ] Remove `KOTLIN MULTIPLATFORM/` from `Akulearn_docs` after confirmation
