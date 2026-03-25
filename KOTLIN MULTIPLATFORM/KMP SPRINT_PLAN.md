# Akulearn Kotlin Multiplatform (KMP) – 2-Week Sprint Plan

## Overview
This sprint plan outlines a detailed, actionable roadmap for developing cross-platform apps using Kotlin Multiplatform (KMP) with JDK, IntelliJ IDEA, and Android Studio. It leverages the current project structure and shared modules for maximum productivity.

---

## Week 1: Foundation & Core Setup

### Phase 1: Environment & Project Initialization
- Open the `KOTLIN MULTIPLATFORM` project in IntelliJ IDEA.
- Verify JDK 17, Android SDK, and (if on macOS) Xcode are installed.
- Sync Gradle and ensure all dependencies resolve.
- Build all targets using `./build-all.sh` and run Android/iOS sample apps.
- Confirm shared module (`shared/`) compiles for all targets.
- Set up GitHub Copilot in IntelliJ IDEA and Android Studio for code suggestions.

### Phase 2: Architecture & Core Libraries
- Review and document the current architecture (see `shared/src/commonMain`).
- Integrate or update libraries:
  - Ktor (networking, in `api/`)
  - kotlinx.coroutines (already present)
  - kotlinx.serialization (add if not present)
  - SQLDelight or similar for local storage (if needed)
- Define dependency injection approach (Koin, Dagger, or manual).
- Document architecture decisions in the repo.

### Phase 3: Core Features Skeleton
- Implement platform abstraction (`Platform.kt`, `Platform.android.kt`, `Platform.ios.kt`).
- Build out the authentication module:
  - Complete `AuthRepository`, `SessionManager`, `TokenStorage`, and `AuthToken`.
  - Wire up `Wave3ApiClient` for login and token refresh.
- Create basic UI screens in Android and iOS apps (Splash, Login, Home).
- Set up navigation for both platforms.
- Write unit tests for shared business logic.

---

## Week 2: Feature Development & Integration

### Phase 4: Feature Implementation
- Implement authentication flow end-to-end:
  - Connect UI to shared logic for login/logout.
  - Persist tokens using `TokenStorage` on each platform.
  - Handle error states and loading indicators.
- Integrate API calls using `Wave3ApiClient`.
- Add local data caching if required.

### Phase 5: Platform-Specific Enhancements
- Polish Android UI (Material components, theming).
- Polish iOS UI (SwiftUI/UIKit, platform conventions).
- Implement platform-specific features (permissions, notifications, etc.).
- Ensure platform-specific code in `androidMain` and `iosMain` is clean and documented.

### Phase 6: Testing, CI, and Documentation
- Expand test coverage (unit, integration, UI tests).
- Set up CI pipeline (GitHub Actions or similar) for builds and tests.
- Document:
  - Project structure and setup (update `README.md`)
  - Contribution guidelines
  - API usage and authentication flow
- Sprint review: demo working features, gather feedback, and plan next steps.

---

## References
- See `KOTLIN MULTIPLATFORM/README.md` for module structure and build instructions.
- Key modules: `shared/api`, `shared/auth`, `shared/Platform.kt`.
- Use GitHub Copilot in IntelliJ IDEA and Android Studio for code assistance.
