# Akulearn Kotlin Multiplatform (KMP) Module

This directory contains the shared Kotlin Multiplatform code for the Akulearn platform, targeting Android and iOS.

## Structure

```
KOTLIN MULTIPLATFORM/
├── androidApp/          # Android application module
├── shared/              # Shared KMP library (business logic, API, auth)
│   └── src/
│       ├── androidMain/ # Android-specific implementations
│       ├── commonMain/  # Shared Kotlin code (all platforms)
│       │   └── kotlin/com/akuplatform/shared/
│       │       ├── api/          # API clients (Wave3ApiClient)
│       │       └── auth/         # Authentication (AuthRepository, SessionManager, TokenStorage)
│       └── iosMain/     # iOS-specific implementations
├── gradle/              # Gradle wrapper and version catalog
├── build-all.sh         # Script to build all platform targets
└── settings.gradle.kts  # Project settings
```

## Prerequisites

- JDK 17
- Android SDK (set `ANDROID_HOME` or create `local.properties`)
- Xcode (for iOS targets, macOS only)

## Building

```bash
# Build all targets
./build-all.sh

# Build Android only
./gradlew :shared:assembleDebug

# Build iOS framework (macOS only)
./gradlew :shared:linkDebugFrameworkIosArm64
```

## Key Modules

### `com.akuplatform.shared.api`
- **Wave3ApiClient** – HTTP client for the Akulearn Wave 3 REST API.

### `com.akuplatform.shared.auth`
- **AuthRepository** – High-level authentication operations (login, logout).
- **SessionManager** – Manages the active user session using `StateFlow`.
- **TokenStorage** – Interface for persisting `AuthToken` on each platform.
- **model/AuthToken** – Data class holding access token, refresh token, and expiry.

## Notes

- `local.properties` and `.gradle/` are excluded from version control via `.gitignore`.
- The `gradlew` / `gradlew.bat` wrapper scripts are committed so builds work without a local Gradle installation.
