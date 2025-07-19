# Akulearn Coding Standards & Best Practices Guide

## General Principles

- **Readability:** Code should be easy to read and understand. Prioritize clarity over cleverness.
- **Consistency:** Follow established patterns and styles throughout the codebase.
- **Simplicity:** Favor straightforward solutions and avoid unnecessary complexity.
- **Modularity:** Break down problems into reusable components (functions, classes, modules).
- **Testability:** Design components to be easily testable in isolation.
- **Defensive Programming:** Anticipate errors and handle edge cases gracefully.
- **YAGNI:** Don't add functionality until it's needed. Avoid premature optimization.
- **DRY:** Avoid duplicating code. Abstract common logic into reusable functions or classes.

### Python

- **Naming:**
  - Variables, functions, methods: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private members: Prefix with `_`
- **Comments & Docstrings:**
  - Explain "why" not just "what"
  - Use PEP 257 for docstrings
- **Formatting:**
  - Use Black and isort
  - 4 spaces for indentation
- **Error Handling:**
  - Handle errors explicitly, raise specific exceptions
  - Add context to errors for debugging
- **Async:**
  - Use `asyncio` for I/O-bound operations
- **Database:**
  - Use SQLAlchemy for PostgreSQL, pymongo for MongoDB

### Go

- **Naming:**
  - Variables, functions: `lowercase` for unexported, `PascalCase` for exported
  - Package names: short, lowercase
- **Comments & Documentation:**
  - Use Godoc conventions
- **Formatting:**
  - Use `go fmt` and `goimports`
  - Tabs for indentation
- **Error Handling:**
  - Return errors, add context
- **Concurrency:**
  - Use goroutines and channels
  - Prefer communication over shared memory
- **Database:**
  - Use database/sql, GORM, or SQLBoiler

## Backend Specifics (Microservices)

- **API Design:**
  - RESTful principles, clear endpoints, versioning (`/v1/`)
  - Consistent JSON structures, proper status codes
  - Validate all incoming requests
- **Microservice Communication:**
  - Kafka for async, REST/gRPC for sync
  - Idempotency for consumers
  - Schema evolution for Kafka messages
- **Database:**
  - Separate data access layer
  - Use transactions for multi-step operations
  - Index frequently queried columns
  - Connection pooling
- **Security:**
  - JWT authentication, RBAC
  - Input validation & sanitization
  - Secrets management (env vars, vaults)
  - HTTPS everywhere
  - Least privilege principle
- **Testing:**
  - Unit, integration, end-to-end tests
  - Mocking frameworks (unittest.mock, gomock)
  - Continuous testing in CI/CD

## Mobile App Guidelines (Kotlin/Android)

- **Architecture:**
  - MVVM, repository pattern, single activity architecture
- **Data Persistence:**
  - Room database, WorkManager for background tasks
  - Content encryption
- **UI/UX:**
  - Jetpack Compose, responsive design, accessibility
- **Network & Sync:**
  - Retrofit for API calls, coroutines for async
  - Connectivity monitoring, idempotent sync
- **Security:**
  - HTTPS, secure token storage, input validation
  - ProGuard/R8 for obfuscation

## Frontend Guidelines (React/Vue)

- **Component Structure:**
  - Modular, reusable components
  - Container/presentational pattern
  - Atomic design (optional)
- **State Management:**
  - React Context, Zustand/Jotai, Redux (RTK Query)
  - Vuex for Vue
  - Immutable state
- **Styling:**
  - CSS-in-JS or CSS Modules
  - Adhere to design system
- **API Interaction:**
  - Axios/Fetch API, error boundaries
  - React Query/SWR for data fetching
- **Performance & Accessibility:**
  - Lazy loading, image optimization
  - Semantic HTML, keyboard navigation

## Code Review & Quality Assurance

- Mandatory peer code reviews
- Use standardized review checklist
- Automated linting, static analysis, security scanning in CI/CD
- Strive for high test coverage with meaningful tests

---

This guide is a living document and will evolve with the Akulearn platform. Adherence to these standards is crucial for building a high-quality, maintainable, and successful product.
