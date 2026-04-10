# Aku Platform Ecosystem Map

This is the single source of truth for all repositories in the Aku Platform ecosystem.  
**All architectural decisions recorded here take precedence over individual repo READMEs.**

---

## Decisions & Source-of-Truth

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend language | **Python / FastAPI** | Matches AI/ML tooling (PyTorch, HuggingFace, LangChain), aligns with existing `requirements.txt` and documented standards in `docs/02-backend/index.md` |
| Frontend / Dashboard | **`akulearn-dashboard/` in this monorepo** | Fully implemented Next.js app with all marketing and dashboard pages; canonical Vercel deployment target |
| Mobile | **Kotlin Multiplatform (KMP)** — dedicated repo `oumar-code/Aku-Mobile` (migration in progress) | Shared business logic for Android and iOS from one codebase |
| Documentation | **This repo (`Akulearn_docs`)** | MkDocs site deployed to GitHub Pages; all service specs, ADRs, API contracts live here |

---

## Repository Inventory

### 🏛 Platform Hub (Docs & Frontend)

| Repo | Role | Tech | Status |
|------|------|------|--------|
| [Akulearn_docs](https://github.com/oumar-code/Akulearn_docs) | Platform docs, MkDocs site, Next.js dashboard, KMP module (migrating) | MkDocs, Next.js 14, Kotlin | **Active — source of truth** |

### 🔵 Core Backend Microservices  
*All services: Python 3.11 / FastAPI / Docker / Kubernetes*

| Repo | Tier | Aku Platform Role | Service Brand | Migration Status |
|------|------|-------------------|---------------|-----------------|
| [Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub) | Tier 1 — Edge | Offline-first local server; Wi-Fi hotspot, local AI inference (Gemma), SQLite store, cloud sync | — | ✅ Python/FastAPI — migrated |
| [Aku-SuperHub](https://github.com/oumar-code/Aku-SuperHub) | Tier 2 — Regional | Regional analytics aggregation, Edge Hub fleet management, model fine-tuning, regional API gateway | — | ✅ Python/FastAPI — migrated |
| [Aku-IGHub](https://github.com/oumar-code/Aku-IGHub) | Tier 3 — Global | Cross-border metadata exchange, Aku Coin financial clearing, policy/compliance enforcement, global credential registry | — | ✅ Python/FastAPI — migrated |
| [Akudemy](https://github.com/oumar-code/Akudemy) | Core Service | Aku Learn: content delivery, offline sync, teacher/admin tools, blockchain credentials | **Akudemy** | ✅ Python/FastAPI — migrated |
| [AkuAI](https://github.com/oumar-code/AkuAI) | Core Service | Shared AI/ML inference: text-gen, classification, summarisation, adaptive learning paths, Gemma fine-tuning | — | ✅ Python/FastAPI — migrated (tagged v0.1.1) |
| [AkuTutor](https://github.com/oumar-code/AkuTutor) | Core Service | AI Tutor: curriculum-aligned Q&A, hint system, feedback loops; consumes AkuAI | — | ✅ Python/FastAPI — migrated |
| [AkuWorkspace](https://github.com/oumar-code/AkuWorkspace) | Core Service | AI-Native Productivity Suite: NL data analysis, doc generation, contextual memory, distributed compute | — | ✅ Python/FastAPI — migrated |
| [Aku-DaaS](https://github.com/oumar-code/Aku-DaaS) | Core Service | Data governance: anonymised dataset pipelines, IG-Hub metadata publishing, privacy labels, consent | — | ✅ Python/FastAPI — migrated |
| [Aku-Telhone](https://github.com/oumar-code/Aku-Telhone) | Core Service | eSIM provisioning: OTA SIM lifecycle, MVNO network switching, device attestation via IG-Hub | **Telhone** | ✅ Python/FastAPI — migrated |

### 🟢 Frontend

| Repo | Role | Tech | Status |
|------|------|------|--------|
| `akulearn-dashboard/` (inside Akulearn_docs) | **Canonical dashboard & marketing site** | Next.js 14, TypeScript, Supabase | **Active — deploy target** |
| [Akudemy-frontend](https://github.com/oumar-code/Akudemy-frontend) | Minimal student-facing landing | Next.js 14 | ⛔ Archived |
| [akulearn-dashB](https://github.com/oumar-code/akulearn-dashB) | Bootstrapped Next.js | Next.js 15 | ⛔ Archived |
| [Akulearn-dashboard](https://github.com/oumar-code/Akulearn-dashboard) | Empty shell | — | ⛔ Archived |

### 📱 Mobile

| Repo | Role | Tech | Status |
|------|------|------|--------|
| `KOTLIN MULTIPLATFORM/` (inside Akulearn_docs) | Shared KMP library — **migrated out** | Kotlin Multiplatform | Migration to `oumar-code/Aku-Mobile` complete; pending removal from this repo |
| [Aku-Mobile](https://github.com/oumar-code/Aku-Mobile) | Standalone KMP repo for Android + iOS | Kotlin Multiplatform, Ktor, Coroutines | **Active** |

### 🖥️ Classroom Edge Clients

| Repo | Role | Tech | Status |
|------|------|------|--------|
| `akulearn-linux-app/` (inside Akulearn_docs) | Classroom client app (Smart TV/Board, Raspberry Pi, Jetson) — syncs content from Edge Hub, AR/VR launcher, offline cache, facilitator dashboard | Kotlin Multiplatform, Compose for Desktop, linuxX64 | **⏳ Pending migration → `oumar-code/Aku-SmartBoard`** |
| [Aku-SmartBoard](https://github.com/oumar-code/Aku-SmartBoard) | Standalone desktop app repo — linuxX64 binary, systemd service, touchscreen support | KMP + Compose Desktop | ✅ Repo created — migration in progress |

### 📦 Content

| Repo | Role | Tech | Status |
|------|------|------|--------|
| `content/` (inside Akulearn_docs) | Offline content library: AI-generated textbooks (9 subjects × SS1), AR/VR assets (.glb, .unitypackage), simulations, flashcards, quizzes, games, offline Wikipedia (.zim), multilingual news corpus (EN/HA/YO), parallel translation corpora | JSON, Markdown, PDF, Unity, GLB | **⏳ Pending migration → `oumar-code/Aku-Content`** |
| `content_templates/` (inside Akulearn_docs) | WAEC/NERDC lesson CSV templates (8 subjects) used by the content generation pipeline | CSV | **⏳ Pending migration → `oumar-code/Aku-Content`** |
| `data/exam_papers/` (inside Akulearn_docs) | 1,350 structured exam questions (WAEC/NECO/JAMB, 4 subjects, 27 topics, 2020–2024) generated by `mlops/exam_paper_scraper.py` | JSON, CSV | **⏳ Pending migration → `oumar-code/Akudemy`** |
| [Aku-Content](https://github.com/oumar-code/Aku-Content) | Dedicated content delivery repo (Git LFS for binaries) — consumed by Akudemy and Aku-EdgeHub | — | ✅ Repo created — migration in progress |

---

## Service Dependency Graph

```
Learner Device / Akudemy-frontend
        |
   akulearn-dashboard (Akulearn_docs monorepo — Next.js)
        |
   API Gateway (Aku-IGHub — Tier 3)
        |
   ┌────────────────────────────────────────────────┐
   │                                                │
Aku-EdgeHub (T1)           Aku-SuperHub (T2)        │
   │  └─ AkuAI (Gemma local inference)             │
   │  └─ Akudemy (offline content sync)             │
   │                                                │
   └── cloud sync ──► Aku-SuperHub ──► Aku-IGHub ──┘
                           │
                    ┌──────┴──────┐
                 Aku-DaaS    AkuWorkspace
                    │
                 AkuTutor
                    │
                  AkuAI (cloud inference)

Aku-Telhone (eSIM) ─── auth ──► Aku-IGHub
```

---

## Python/FastAPI Standard Stack per Service

Every backend service must use:

| Layer | Technology |
|-------|------------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| ASGI server | Uvicorn |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2 (async) |
| Migrations | Alembic |
| Database | PostgreSQL (primary), Redis (cache) |
| Auth | JWT (python-jose) + RBAC |
| Async messaging | Kafka (confluent-kafka-python) |
| Testing | Pytest + pytest-asyncio + httpx |
| Linting | Ruff + Black + isort |
| Container | Docker (multi-stage, non-root user) |
| Orchestration | Kubernetes |

See [`docs/service-templates/python-fastapi-bootstrap.md`](service-templates/python-fastapi-bootstrap.md) for the step-by-step migration guide.

---

## Contracts & API Specs

All OpenAPI specs live in this repo:

| Document | Location |
|----------|----------|
| Authentication API | `docs/02-backend/api-specs.md` |
| Content API | `docs/02-backend/api-specs.md` |
| Full API reference | `docs/api_specs.md` |
| Database schemas | `docs/02-backend/database-schemas.md` |
| Containerisation spec | `docs/05-cross-cutting/containerization.md` |

A dedicated [`aku-platform-contracts`](https://github.com/oumar-code/aku-platform-contracts) repo (OpenAPI YAML files, Pydantic models, Kafka schemas) has been created to share types across all 9 service repos.  
**Proposal & implementation checklist:** [`docs/aku-platform-contracts.md`](aku-platform-contracts.md)  
**Next step:** define Pydantic schemas and run `docs/service-migrations/integrate-contracts.sh` to add the package dependency to all 9 services.

---

## Client SDK Examples

Reference implementations for integrating with the Aku Platform Wave 3 APIs live in [`client_examples/`](https://github.com/oumar-code/Akulearn_docs/tree/main/client_examples):

| File(s) | What It Covers |
|---------|---------------|
| `apolloClient.js` + `graphqlQueries.js` | Apollo Client setup, all GQL query/mutation/subscription definitions |
| `ApolloUsageExamples.jsx` | React integration — lesson fetch, progress tracking, leaderboard, quiz submission |
| `WebSocketClient.js` | Standalone WS client — reconnect, ping/pong, typed event emission |
| `KnowledgeGraphVisualization.jsx` + `.css` | D3.js force-directed knowledge graph with subject/difficulty filters |
| `LearningPathwayVisualization.jsx` + `.css` | Learning pathway UI — lesson status, path selection |
| `RecommendationsWidget.jsx` + `.css` | Recommendations card widget |
| `VisualizationIntegrationExample.jsx` + `.css` | Combined dashboard page |
| `ReactNativeExamples.jsx` | React Native integration for mobile |

Full usage guide: [`docs/client-sdk/index.md`](client-sdk/index.md)

---

## Content & Classroom App Migration Checklists

> **Migration scripts** are in `docs/service-migrations/`:
>
> | Script | What it does |
> |--------|-------------|
> | `migrate-to-aku-content.sh` | Clones Aku-Content, initialises Git LFS, copies `content/` + `content_templates/`, opens PR. `--stub-only` flag: initialises LFS + dir structure without local content (can run in CI). `--help` for full usage. |
> | `migrate-exam-papers.sh` | Clones Akudemy, copies `data/exam_papers/` + `mlops/exam_paper_scraper.py`, opens PR. `--stub-only` flag: creates dir structure + scraper placeholder without local data (can run in CI). `--help` for full usage. |
> | `migrate-to-aku-smartboard.sh` | Clones Aku-SmartBoard, copies `akulearn-linux-app/`, applies CI/release workflow scaffold, opens PR. `--scaffold-only` flag: pushes just the CI scaffold without needing local app source (can run in CI). `--help` for full usage. |
>
> CI/release workflow scaffold for Aku-SmartBoard: `docs/service-migrations/scaffolds/Aku-SmartBoard/`
>
> **GitHub Actions workflows** (no local machine needed — require `GH_PAT` secret):
>
> | Workflow | What it does |
> |----------|-------------|
> | `scaffold-aku-smartboard.yml` | Pushes CI/release workflow + systemd unit to Aku-SmartBoard; opens PR |
> | `stub-aku-content.yml` | Initialises Aku-Content with LFS config, README, dir structure; opens PR |
> | `stub-akudemy-exam-papers.yml` | Adds exam papers dir structure + scraper placeholder to Akudemy; opens PR |

### Aku-Content (new repo)

The `content/` and `content_templates/` directories should move to a dedicated `oumar-code/Aku-Content` repo with Git LFS for binary assets (.glb, .unitypackage, .pdf, .mp4, .zip).

- [x] Create `oumar-code/Aku-Content` repository with Git LFS
- [x] Create migration script with `--stub-only` and `--help` modes (`docs/service-migrations/migrate-to-aku-content.sh`)
- [x] Create GitHub Actions workflow to push LFS config + README + dir structure stub (`stub-aku-content.yml`) — **no local machine needed**
- [ ] **Trigger `stub-aku-content.yml`** from GitHub Actions UI → opens PR in Aku-Content with LFS config + empty dirs
- [ ] ⚠️ **LOCAL MACHINE REQUIRED** — Copy `content/` tree (textbooks, AR, VR, simulations, flashcards, quizzes, games, encyclopedia, tools, news corpus): restore `content/` locally, then run `./docs/service-migrations/migrate-to-aku-content.sh`
- [ ] ⚠️ **LOCAL MACHINE REQUIRED** — Copy `content_templates/` CSV templates (included in the same full migration run above)
- [ ] Update Akudemy and Aku-EdgeHub to reference new content repo
- [ ] Remove `content/` and `content_templates/` from `Akulearn_docs` after migration is confirmed

### Akudemy — Exam Papers

The `data/exam_papers/` dataset and `mlops/exam_paper_scraper.py` belong in `oumar-code/Akudemy`.

- [x] Create migration script with `--stub-only` and `--help` modes (`docs/service-migrations/migrate-exam-papers.sh`)
- [x] Create GitHub Actions workflow to push dir structure + scraper stub (`stub-akudemy-exam-papers.yml`) — **no local machine needed**
- [ ] **Trigger `stub-akudemy-exam-papers.yml`** from GitHub Actions UI → opens PR in Akudemy with placeholder structure
- [ ] ⚠️ **LOCAL MACHINE REQUIRED** — Copy `data/exam_papers/` (1,350 questions, JSON + CSV): restore `data/exam_papers/` locally, then run `./docs/service-migrations/migrate-exam-papers.sh`
- [ ] ⚠️ **LOCAL MACHINE REQUIRED** — Copy `mlops/exam_paper_scraper.py` and its docs (included in the same full migration run above)
- [ ] Remove `data/` (exam_papers) from `Akulearn_docs` after migration is confirmed

### Aku-SmartBoard (new repo)

The `akulearn-linux-app/` directory is a full KMP/Compose Desktop application — it needs its own CI/CD and release pipeline.

- [x] Create `oumar-code/Aku-SmartBoard` repository
- [x] Create migration script with `--scaffold-only` and `--help` modes (`docs/service-migrations/migrate-to-aku-smartboard.sh`)
- [x] Create GitHub Actions CI/release workflow scaffold (`docs/service-migrations/scaffolds/Aku-SmartBoard/`)
- [x] Create GitHub Actions workflow to push CI scaffold to Aku-SmartBoard (`scaffold-aku-smartboard.yml`) — **no local machine needed**
- [ ] **Trigger `scaffold-aku-smartboard.yml`** from GitHub Actions UI → opens PR in Aku-SmartBoard with `release.yml` + `systemd/` unit
- [ ] ⚠️ **LOCAL MACHINE REQUIRED** — Copy `akulearn-linux-app/` (Kotlin source, Gradle build, DEPLOYMENT.md): restore `akulearn-linux-app/` locally, then run `./docs/service-migrations/migrate-to-aku-smartboard.sh`
- [ ] Add systemd service unit to GitHub Release assets (covered by CI workflow scaffold, applied above)
- [ ] Remove `akulearn-linux-app/` from `Akulearn_docs` after migration is confirmed

---

## KMP Migration Checklist

The `KOTLIN MULTIPLATFORM/` directory in this repo has been moved to `oumar-code/Aku-Mobile`.

- [x] Create `oumar-code/Aku-Mobile` repository
- [x] Copy contents of `KOTLIN MULTIPLATFORM/` to new repo root
- [x] Add `oumar-code/Aku-Mobile` to this table once live
- [ ] Remove `KOTLIN MULTIPLATFORM/` from `Akulearn_docs` after migration is confirmed
- [ ] Update `docs/03-mobile/index.md` with link to the new repo

---

## Frontend Consolidation Decision

The canonical frontend is **`akulearn-dashboard/` inside this monorepo**. It is:
- Deployed via Vercel (CI in `.github/workflows/vercel-deploy.yml`)
- Source of truth for all marketing pages (`/`, `/about`, `/blog`, `/pricing`, `/register`, `/jamb`)
- Source of truth for all authenticated dashboard pages (`/dashboard/*`)
- Backed by Supabase for auth and data

`Akudemy-frontend`, `akulearn-dashB`, and `Akulearn-dashboard` repos have been **archived**. All future frontend work goes to `akulearn-dashboard/` in this monorepo.
