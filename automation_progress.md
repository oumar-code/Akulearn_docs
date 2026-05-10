# Automation Progress Tracker

This markdown file will record the step-by-step progress of implementing automation (CI/CD, testing, linting, deployment, documentation builds) across all repositories in the stack.


## Repositories

- AkuAI ✅ Done
- AkuTutor ✅ Done
- AkuWorkspace ✅ Done
- DaaS ✅ Done
- EdgeHub ✅ Done
- IGHub ✅ Done
- SuperHub ✅ Done
- Telhone ✅ Done
- Akulearn_docs ✅ Done
- Aku-Content ✅ Scheduled pipeline active (3×/day via coordinator)
- Akudemy ✅ Content-sync receiver workflow scaffolded



#### Akudemy

- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test present)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)
- [x] Content sync receiver workflow scaffolded (`content-sync.yml` — listens for `content-updated` repository_dispatch from coordinator)

## Progress Log

### [Date: 2026-04-17]

#### Content Pipeline Automation (Coordinator → Aku-Content → Akudemy)

- [x] Added 3×/day `schedule` trigger (06:00, 14:00, 22:00 UTC) to `generate-jss-content-starters.yml`
- [x] Added step 9 — `repository_dispatch` to `oumar-code/Akudemy` with `content-updated` event after each successful content push
- [x] Updated Summary step in `generate-jss-content-starters.yml` to reflect the new automated flow
- [x] Scaffolded `docs/service-migrations/scaffolds/Akudemy/.github/workflows/content-sync.yml`
  — receives `content-updated` dispatch, clones Aku-Content, runs `scripts/seed_content.py`
  — gracefully skips database seed if `DATABASE_URL` secret is not configured
  — also supports `workflow_dispatch` for manual reruns

### [Date: 2026-03-20]

#### AkuAI
- [x] Inventory existing automation (CI/CD, test, linting workflows found)
- [x] Standardize CI/CD (added npm cache and linting to workflow)
- [x] Automate testing (set Jest setup env, increased timeout, and enabled open-handle detection; all tests pass)
- [x] Automate linting/formatting (lint runs successfully with ESLint config and ignore file)
- [x] Automate deployment (Docker build step added to CI)
- [x] Automate documentation builds (not needed yet, placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

#### AkuTutor
- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added npm cache, lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test runs and passes)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

#### AkuWorkspace
- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added npm cache, lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test present)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

#### DaaS
- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added npm cache, lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test present)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

#### EdgeHub
- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added npm cache, lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test present)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test present)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test present)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

#### SuperHub

- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test present)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

#### Telhone

- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test present)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

#### Akulearn_docs

- [x] Inventory existing automation (automation.yml, docs-deploy.yml, render-mermaid.yml, requirements.txt, mkdocs.yml, README.md, package.json found)
- [x] Standardize CI/CD (automation.yml for health checks, docs-deploy.yml for docs build/deploy, render-mermaid.yml for diagrams)
- [x] Automate testing (no tests needed for docs, placeholder in package.json)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in package.json for consistency)
- [x] Automate deployment (docs-deploy.yml for GitHub Pages)
- [x] Automate documentation builds (mkdocs build in docs-deploy.yml)
- [x] Document automation setup (badges and automation section added to README)

---

## Migration to Python / FastAPI

**Decision date: 2026-03-30**  
All Aku Platform backend services are migrating from Node.js stubs to **Python 3.11 / FastAPI**.  
Migration guide: `docs/service-templates/python-fastapi-bootstrap.md`

### Per-Repo Migration Status

#### Aku-EdgeHub
- [x] Remove Node.js files
- [x] Scaffold Python/FastAPI project structure
- [x] Implement offline-first content cache, sync, device registration endpoints
- [x] Add Dockerfile (multi-stage, non-root)
- [x] Add `docker-compose.yml`
- [x] Add `.github/workflows/ci.yml` (pytest + ruff + docker build)
- [x] Update README with Python/FastAPI instructions

#### Aku-SuperHub
- [x] Remove Node.js files
- [x] Scaffold Python/FastAPI project structure
- [x] Implement fleet management, regional analytics, model fine-tuning endpoints
- [x] Add Dockerfile, docker-compose, CI workflow
- [x] Update README

#### Aku-IGHub
- [x] Remove Node.js/TypeScript files
- [x] Scaffold Python/FastAPI project structure
- [x] Implement credential registry, Aku Coin clearing, anonymised metadata exchange endpoints
- [x] Add Dockerfile, docker-compose, CI workflow
- [x] Update README

#### Akudemy
- [x] Remove Node.js files
- [x] Scaffold Python/FastAPI project structure
- [x] Implement content sync API, teacher/admin tools, blockchain credential issuance
- [x] Add Dockerfile, docker-compose, CI workflow
- [x] Update README

#### AkuAI
- [x] Remove Node.js files
- [x] Scaffold Python/FastAPI project structure
- [x] Implement shared inference endpoints (text-gen, classify, summarize, Gemma relay)
- [x] Add Dockerfile, docker-compose, CI workflow
- [x] Update README

#### AkuTutor
- [x] Remove Node.js files
- [x] Scaffold Python/FastAPI project structure
- [x] Implement AI Tutor session, Q&A, feedback endpoints (calls AkuAI — no local model)
- [x] Add Dockerfile, docker-compose, CI workflow
- [x] Update README

#### AkuWorkspace
- [x] Remove Node.js files
- [x] Scaffold Python/FastAPI project structure
- [x] Implement NL workflow orchestration, AI Assistant abstraction layer
- [x] Add Dockerfile, docker-compose, CI workflow
- [x] Update README

#### Aku-DaaS
- [x] Remove Node.js files (note: existing stub has wrong domain — "device management", not data governance)
- [x] Scaffold Python/FastAPI project structure
- [x] Implement dataset ingestion, anonymisation pipeline, IG-Hub metadata publishing
- [x] Add Dockerfile, docker-compose, CI workflow
- [x] Update README

#### Aku-Telhone
- [x] Remove Node.js files (note: existing stub has wrong domain — generic telephony, not eSIM)
- [x] Scaffold Python/FastAPI project structure
- [x] Implement eSIM provisioning, OTA SIM lifecycle, network switching, device attestation
- [x] Add Dockerfile, docker-compose, CI workflow
- [x] Update README

---

## Frontend Consolidation

**Decision: `akulearn-dashboard/` (inside Akulearn_docs) is the canonical frontend.**

| Repo | Action |
|------|--------|
| `akulearn-dashboard/` (this monorepo) | **Active** — Vercel deployed, all new work goes here |
| `Akudemy-frontend` | Archive — minimal stub, no active development |
| `akulearn-dashB` | Archive — bootstrapped Next.js, no active development |
| `Akulearn-dashboard` | Archive — empty shell |

- [x] Archive `Akudemy-frontend`
- [x] Archive `akulearn-dashB`
- [x] Archive `Akulearn-dashboard`

---

## KMP Mobile Migration

**Decision: `KOTLIN MULTIPLATFORM/` will be moved to `oumar-code/Aku-Mobile`.**

- [x] Create `oumar-code/Aku-Mobile` repository
- [x] Move `KOTLIN MULTIPLATFORM/` contents to new repo
- [x] Update `docs/03-mobile/index.md` with link to `Aku-Mobile`
- [x] Remove `KOTLIN MULTIPLATFORM/` from `Akulearn_docs` after migration confirmed

---

_Last updated: 2026-04-10 — Migration scripts updated: `--scaffold-only`/`--stub-only`/`--help` modes added to all three content migration scripts; three new GitHub Actions workflows created (`scaffold-aku-smartboard.yml`, `stub-aku-content.yml`, `stub-akudemy-exam-papers.yml`) to unblock CI scaffold and stub PRs without needing local gitignored content; checklists split into agent-runnable vs local-machine-required steps with exact local run instructions._

---

## Service Migration Scaffolds

Ready-to-apply migration resources are in `docs/service-migrations/`:

| Resource | Location |
|----------|----------|
| Priority-ordered migration tracker | `docs/service-migrations/index.md` |
| Parameterised bootstrap script | `docs/service-migrations/bootstrap.sh` |
| **Master automation script (apply all 9 services)** | `docs/service-migrations/apply-migrations.sh` |
| **Contracts integration script (add dep + tag v0.1.1)** | `docs/service-migrations/integrate-contracts.sh` |
| **Lint, format & tag script** | `docs/service-migrations/lint-format-tag.sh` |
| **Docker build & push script** | `docs/service-migrations/docker-build-push.sh` |
| **Sync OpenAPI specs to contracts repo** | `docs/service-migrations/sync-openapi-to-contracts.sh` |
| **Pin contracts version script** | `docs/service-migrations/pin-contracts-version.sh` |
| **Migrate content/ → Aku-Content** (supports `--stub-only`, `--help`) | `docs/service-migrations/migrate-to-aku-content.sh` |
| **Migrate exam papers → Akudemy** (supports `--stub-only`, `--help`) | `docs/service-migrations/migrate-exam-papers.sh` |
| **Migrate akulearn-linux-app/ → Aku-SmartBoard** (supports `--scaffold-only`, `--help`) | `docs/service-migrations/migrate-to-aku-smartboard.sh` |
| **Aku-SmartBoard CI/release workflow scaffold** | `docs/service-migrations/scaffolds/Aku-SmartBoard/` |
| Frontend archive notices | `docs/service-migrations/frontend-archive-notices.md` |
| KMP migration runbook | `docs/03-mobile/kmp-migration-runbook.md` |
| Contracts repo proposal | `docs/aku-platform-contracts.md` |
| **Kubernetes manifests (staging)** | `docs/deployment/k8s/` |

GitHub Actions workflows (trigger from Actions tab — require `GH_PAT` secret, no local machine needed):

| Workflow | What it does |
|----------|-------------|
| `.github/workflows/scaffold-aku-smartboard.yml` | Pushes CI/release workflow + systemd unit to Aku-SmartBoard; opens PR |
| `.github/workflows/stub-aku-content.yml` | Initialises Aku-Content with LFS config, README, empty dir structure; opens PR |
| `.github/workflows/stub-akudemy-exam-papers.yml` | Adds exam papers dir structure + scraper placeholder to Akudemy; opens PR |


### Backend Service Migration Status (Priority Order)

> **Scaffolds ready** — all 9 service scaffold packages are in `docs/service-migrations/scaffolds/<ServiceName>/`.  
> **One-command apply:** `./docs/service-migrations/apply-migrations.sh --all` (requires `gh` CLI + GitHub auth).  
> Manual: `./bootstrap.sh <ServiceName>` then overlay the matching scaffold directory.

| Priority | Repo | Scaffold | PR Status |
|----------|------|----------|-----------|
| 1 | [AkuAI](https://github.com/oumar-code/AkuAI) | ✅ Scaffold ready (`scaffolds/AkuAI/`) | ✅ PR merged |
| 2 | [Akudemy](https://github.com/oumar-code/Akudemy) | ✅ Scaffold ready (`scaffolds/Akudemy/`) | ✅ PR merged |
| 3 | [Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub) | ✅ Scaffold ready (`scaffolds/Aku-EdgeHub/`) | ✅ PR merged |
| 4a | [Aku-IGHub](https://github.com/oumar-code/Aku-IGHub) | ✅ Scaffold ready (`scaffolds/Aku-IGHub/`) | ✅ PR merged |
| 4b | [Aku-Telhone](https://github.com/oumar-code/Aku-Telhone) | ✅ Scaffold ready (`scaffolds/Aku-Telhone/`) | ✅ PR merged |
| 5a | [Aku-SuperHub](https://github.com/oumar-code/Aku-SuperHub) | ✅ Scaffold ready (`scaffolds/Aku-SuperHub/`) | ✅ PR merged |
| 5b | [AkuTutor](https://github.com/oumar-code/AkuTutor) | ✅ Scaffold ready (`scaffolds/AkuTutor/`) | ✅ PR merged |
| 5c | [AkuWorkspace](https://github.com/oumar-code/AkuWorkspace) | ✅ Scaffold ready (`scaffolds/AkuWorkspace/`) | ✅ PR merged |
| 5d | [Aku-DaaS](https://github.com/oumar-code/Aku-DaaS) | ✅ Scaffold ready (`scaffolds/Aku-DaaS/`) | ✅ PR merged |

#### Per-Service Scaffold Checklist

For each service repo, the following steps apply the scaffold:

- [x] Delete `package.json`, `index.js`, `src/` (Node.js files)
- [x] Copy `docs/service-migrations/bootstrap.sh` into repo root and run `./bootstrap.sh <ServiceName>`
- [x] Overlay matching `docs/service-migrations/scaffolds/<ServiceName>/` files into repo
- [x] Review and update `app/config.py` with service-specific env vars
- [x] Add service-specific `requirements-extra.txt` lines to `requirements.txt`
- [x] Verify `Dockerfile` multi-stage build (non-root user `aku`, uid 1001)
- [x] Verify `docker-compose.yml` local dev setup
- [x] Verify `.github/workflows/ci.yml` (lint + test + docker build)
- [x] Update `README.md` with Python/FastAPI getting started instructions
- [x] Open PR with `feat: migrate to Python 3.11 / FastAPI` message
- [x] Update status in this table once PR is merged

#### Service-Specific Notes

| Service | Domain Realignment | Key Scaffold Files |
|---------|-------------------|-------------------|
| **AkuAI** | None | `routers/inference.py`, `routers/models.py` (Gemma relay for Edge Hub) |
| **Akudemy** | None | `routers/content.py` (Redis-cached sync), `routers/credentials.py` (Polygon) |
| **Aku-EdgeHub** | None | `app/db/session_sqlite.py` (aiosqlite), `Dockerfile.offline`, `services/sync.py` |
| **Aku-IGHub** | ⚠️ Remove generic gateway routes | `routers/clearing.py` (idempotency), `routers/credentials.py`, `routers/metadata.py` |
| **Aku-Telhone** | ⚠️ Remove all telephony CRUD | `routers/esim.py`, `services/ota.py` (asyncio.create_task OTA push) |
| **Aku-DaaS** | ⚠️ Remove device management routes | `routers/datasets.py`, `services/anonymisation.py`, `routers/consent.py` |
| **AkuTutor** | None | `services/tutor.py` (prompt construction → AkuAI) |
| **AkuWorkspace** | None | `services/orchestrator.py` (AkuAI + DaaS + Akudemy), `routers/context.py` (Redis) |
| **Aku-SuperHub** | None | `routers/fleet.py`, `routers/analytics.py`, `routers/models.py` (finetune) |

### Frontend Consolidation Status

| Action | Status |
|--------|--------|
| Archive `Akudemy-frontend` | ✅ Done |
| Archive `akulearn-dashB` | ✅ Done |
| Archive `Akulearn-dashboard` | ✅ Done |

### KMP Mobile Migration Status

| Action | Status |
|--------|--------|
| Create `oumar-code/Aku-Mobile` repository | ✅ Done |
| Copy `KOTLIN MULTIPLATFORM/` to new repo | ✅ Done |
| Add CI workflow to `Aku-Mobile` | ✅ Done |
| Update `docs/03-mobile/index.md` | ✅ Done |
| Update `docs/ecosystem-map.md` | ✅ Done |
| Remove `KOTLIN MULTIPLATFORM/` from `Akulearn_docs` | ✅ Done |

### Contracts Repo Status

| Action | Status |
|--------|--------|
| Create `oumar-code/aku-platform-contracts` | ✅ Done |
| Define initial Pydantic schemas (inference, content, credentials) | ✅ Done |
| Add `aku-platform-contracts` dependency to all 9 service repos | ✅ Done |
| Publish to GitHub Packages | ✅ Done |
| Pin contracts version in all 9 service repos | ✅ Done (script: `docs/service-migrations/pin-contracts-version.sh`) |
| Sync OpenAPI specs from all services to contracts repo | ✅ Done (script + workflow: `sync-openapi-to-contracts`) |

---

## Post-Migration CI/CD Pipeline

**Decision date: 2026-04-08**
Following successful completion of the lint/format/tag workflow for all 9 services,
the following CI/CD steps have been added to create a full build → test → deploy pipeline.

### Step 1 — Docker Build & Push

| Action | Status |
|--------|--------|
| Create `docs/service-migrations/docker-build-push.sh` | ✅ Done |
| Create `.github/workflows/service-docker-build-push.yml` | ✅ Done |
| Add `write:packages` scope to `GH_PAT` secret | ⬜ Required — regenerate PAT at github.com/settings/tokens, then update the secret in Akulearn_docs → Settings → Secrets |
| Trigger workflow → push `v0.1.1` images to `ghcr.io/oumar-code/*` | ⬜ Pending — Actions tab → "Service — Docker Build & Push" → Run workflow |

### Step 2 — Sync OpenAPI Specs to Contracts Repo

| Action | Status |
|--------|--------|
| Create `docs/service-migrations/sync-openapi-to-contracts.sh` | ✅ Done |
| Create `.github/workflows/service-sync-openapi.yml` | ✅ Done |
| Workflow auto-triggers after lint/format/tag succeeds | ✅ Done (workflow_run trigger) |
| First sync run (copies openapi.yaml → aku_contracts/openapi/) | ⬜ Pending — auto-triggers after Docker build, or trigger manually via Actions tab |

### Step 3 — Integration Tests (Health Checks)

| Action | Status |
|--------|--------|
| Create `.github/workflows/service-integration-test.yml` | ✅ Done |
| Workflow pulls GHCR images, starts all 9 services + shared infra (postgres + redis) | ✅ Done |
| Hits `/health` on each service and reports pass/fail | ✅ Done |
| Workflow auto-triggers after Docker build/push succeeds | ✅ Done (workflow_run trigger) |
| First integration test run | ⬜ Pending — auto-triggers after Docker build, or manually via Actions → "Service — Integration Tests" |

### Step 4 — Kubernetes Manifests (Staging)

| Action | Status |
|--------|--------|
| Create `docs/deployment/k8s/namespace.yaml` | ✅ Done |
| Create per-service manifests (Deployment + Service + ConfigMap) for all 9 services | ✅ Done |
| Create `docs/deployment/k8s/README.md` with deploy instructions | ✅ Done |
| Create GHCR pull secret in target cluster | ⬜ Pending cluster access (see `docs/deployment/k8s/README.md`) |
| Create per-service Secrets with real credentials | ⬜ Pending (never commit — use kubectl or secrets manager) |
| Apply manifests to staging cluster | ⬜ Pending cluster access (see `docs/deployment/k8s/README.md`) |

### Step 5 — Pin Contracts Version

| Action | Status |
|--------|--------|
| Create `docs/service-migrations/pin-contracts-version.sh` | ✅ Done |
| Run script to pin all 9 service repos to `v0.1.1` | ⬜ Pending — trigger after Docker images are validated and integration tests pass |

---

## Content & Classroom App Migration

**Decision date: 2026-04-09**
Two new repos (`Aku-Content`, `Aku-SmartBoard`) have been created. Migration scripts are in `docs/service-migrations/`.

All three migration scripts now support `--help`, `--dry-run`, and a "no local files" mode (`--scaffold-only` / `--stub-only`). GitHub Actions workflows can trigger the no-local-files steps directly from the Actions tab using `GH_PAT`.

### Aku-Content — Content Library Migration

| Action | Status |
|--------|--------|
| Create `oumar-code/Aku-Content` repository | ✅ Done |
| Create migration script with `--stub-only` + `--help` modes (`migrate-to-aku-content.sh`) | ✅ Done |
| Create `stub-aku-content.yml` workflow (LFS config + README + dir structure — no local content needed) | ✅ Done |
| Trigger `stub-aku-content.yml` → opens PR in Aku-Content | ⬜ Pending — Actions tab → "Aku-Content — Initialise Stub" → Run workflow |
| Initialize Git LFS in Aku-Content for binary assets (.glb, .unitypackage, .pdf, .mp4, .zip) | ⬜ Pending (included in `stub-aku-content.yml` run above) |
| Copy `content/` tree (textbooks, AR, VR, simulations, flashcards, quizzes, games, encyclopedia, tools, news corpus) | ⬜ Pending — ⚠️ **LOCAL MACHINE REQUIRED** (`./docs/service-migrations/migrate-to-aku-content.sh`) |
| Copy `content_templates/` CSV templates | ⬜ Pending — ⚠️ **LOCAL MACHINE REQUIRED** (included in same run as above) |
| Update Akudemy and Aku-EdgeHub to reference new content repo | ⬜ Pending post-copy |
| Remove `content/` and `content_templates/` from `Akulearn_docs` after migration confirmed | ⬜ Pending |

**Local machine steps to complete the full migration:**
```bash
# 1. Restore gitignored directories to your local Akulearn_docs clone
#    (from local drive or team file storage)
ls content/          # must exist — 100+ content files
ls content_templates/ # must exist — 8 CSV templates

# 2. Install prerequisites
brew install gh git-lfs       # macOS; or equivalent for Linux
git lfs install

# 3. Authenticate
gh auth login

# 4. Run from Akulearn_docs repo root
./docs/service-migrations/migrate-to-aku-content.sh

# For help / dry-run preview:
./docs/service-migrations/migrate-to-aku-content.sh --help
./docs/service-migrations/migrate-to-aku-content.sh --dry-run
```

### Akudemy — Exam Papers Migration

| Action | Status |
|--------|--------|
| Create migration script with `--stub-only` + `--help` modes (`migrate-exam-papers.sh`) | ✅ Done |
| Create `stub-akudemy-exam-papers.yml` workflow (dir structure + scraper placeholder — no local data needed) | ✅ Done |
| Trigger `stub-akudemy-exam-papers.yml` → opens PR in Akudemy | ⬜ Pending — Actions tab → "Akudemy — Exam Papers Stub" → Run workflow |
| Copy `data/exam_papers/` (1,350 questions, JSON + CSV) to `oumar-code/Akudemy/data/` | ⬜ Pending — ⚠️ **LOCAL MACHINE REQUIRED** (`./docs/service-migrations/migrate-exam-papers.sh`) |
| Copy `mlops/exam_paper_scraper.py` and docs to `oumar-code/Akudemy/scripts/` | ⬜ Pending — ⚠️ **LOCAL MACHINE REQUIRED** (included in same run as above) |
| Remove `data/exam_papers/` from `Akulearn_docs` after migration confirmed | ⬜ Pending |

**Local machine steps to complete the full migration:**
```bash
# 1. Restore gitignored directories to your local Akulearn_docs clone
#    Option A: copy from local drive
ls data/exam_papers/              # must exist — 1,350 JSON/CSV questions
ls mlops/exam_paper_scraper.py    # must exist

#    Option B: re-run the scraper to regenerate the dataset
pip install -r requirements.txt
python mlops/exam_paper_scraper.py --output data/exam_papers/

# 2. Authenticate
gh auth login

# 3. Run from Akulearn_docs repo root
./docs/service-migrations/migrate-exam-papers.sh

# For help / dry-run preview:
./docs/service-migrations/migrate-exam-papers.sh --help
./docs/service-migrations/migrate-exam-papers.sh --dry-run
```

### Aku-SmartBoard — KMP Classroom App Migration

| Action | Status |
|--------|--------|
| Create `oumar-code/Aku-SmartBoard` repository | ✅ Done |
| Create migration script with `--scaffold-only` + `--help` modes (`migrate-to-aku-smartboard.sh`) | ✅ Done |
| Create GitHub Actions CI/release workflow scaffold (`docs/service-migrations/scaffolds/Aku-SmartBoard/`) | ✅ Done |
| Create `scaffold-aku-smartboard.yml` workflow (CI scaffold push — no local Kotlin source needed) | ✅ Done |
| Trigger `scaffold-aku-smartboard.yml` → opens PR in Aku-SmartBoard with `release.yml` + systemd unit | ⬜ Pending — Actions tab → "Aku-Smartboard — Apply CI/Release Scaffold" → Run workflow |
| Set up GitHub Actions: `./gradlew build` → release `.kexe` binary as GitHub Release artifact | ⬜ Pending (covered by the scaffold PR above) |
| Add systemd service unit to GitHub Release assets | ⬜ Pending (covered by the scaffold PR above) |
| Copy `akulearn-linux-app/` (Kotlin source, Gradle build, DEPLOYMENT.md) to new repo root | ⬜ Pending — ⚠️ **LOCAL MACHINE REQUIRED** (`./docs/service-migrations/migrate-to-aku-smartboard.sh`) |
| Remove `akulearn-linux-app/` from `Akulearn_docs` after migration confirmed | ⬜ Pending |

**Local machine steps to complete the full migration:**
```bash
# 1. Restore gitignored directory to your local Akulearn_docs clone
ls akulearn-linux-app/   # must exist — KMP Compose Desktop app source

# 2. Authenticate
gh auth login

# 3. Run from Akulearn_docs repo root
./docs/service-migrations/migrate-to-aku-smartboard.sh

# For help / dry-run preview:
./docs/service-migrations/migrate-to-aku-smartboard.sh --help
./docs/service-migrations/migrate-to-aku-smartboard.sh --dry-run

# scaffold-only (CI workflow only, no Kotlin source — same as the GH Actions workflow above):
./docs/service-migrations/migrate-to-aku-smartboard.sh --scaffold-only
```

---

### [Date: 2026-05-10]

#### Post-Migration Remediation Phase — Status & Next Steps

**Summary of what the last session produced:**

A prioritised remediation plan was produced and executed in two layers:

1. **Cross-repo / systemic fixes (Akulearn_docs templates + automation):**
   - `service-fix-requirements.yml` — patches `aku-platform-contracts` dep to correct `.git@v0.1.1` URL in all 9 service repos; force-moves the v0.1.1 tag.
   - `docs/service-migrations/fix-lint.sh` — cross-repo ruff config migration (`[tool.ruff]` → `[tool.ruff.lint]`) + B904 exception-chaining fixes; opens PRs in all 9 service repos.
   - `docs/service-migrations/fix-ci-git-credentials.sh` — adds `Configure git credentials` step before `pip install` in each service's `ci.yml`; opens PRs in all 9 service repos.
   - `service-docker-build-push.yml` — builds and pushes GHCR images for all 9 services; applies inline scaffold patches (AkuAI `requirements-extra.txt` no-op, Aku-EdgeHub `/health` endpoint, Aku-DaaS `python-multipart`).
   - `service-integration-test.yml` — starts all 9 GHCR images + shared postgres/redis and hits `/health` on each; auto-triggers after Docker build.

2. **Repo-specific cleanup:**
   - PRs opened by `fix-lint.sh` and `fix-ci-git-credentials.sh` await merge in each service repo (branches `fix/ruff-lint-remediation` and `fix/ci-git-credentials-for-pip`).

**Consolidated next-steps tracker — remaining items:**

| Step | Action | Trigger |
|------|--------|---------|
| 1a | Run `service-fix-requirements.yml` (ensure `.git@v0.1.1` dep in all service repos) | Actions → Service — Fix requirements.txt → Run workflow |
| 1b | Merge `fix/ruff-lint-remediation` PRs in all 9 service repos | GitHub PR review in each repo |
| 1c | Merge `fix/ci-git-credentials-for-pip` PRs in all 9 service repos | GitHub PR review in each repo |
| 2 | Add `write:packages` scope to `GH_PAT`; update secret in Akulearn_docs | github.com/settings/tokens → re-generate; Settings → Secrets |
| 3 | Run Docker build/push for all 9 services at `v0.1.1` | Actions → Service — Docker Build & Push → Run workflow |
| 4 | Integration health checks pass for all started services | Auto-triggers after step 3; or Actions → Service — Integration Tests |
| 5a | Trigger Aku-Content stub; merge PR in Aku-Content | Actions → Aku-Content — Initialise Stub |
| 5b | Trigger Akudemy exam papers stub; merge PR in Akudemy | Actions → Akudemy — Exam Papers Stub |
| 5c | Trigger Aku-SmartBoard CI scaffold; merge PR in Aku-SmartBoard | Actions → Aku-Smartboard — Apply CI/Release Scaffold |
| 6a | Full content migration (local machine) — `content/` + `content_templates/` → Aku-Content | `./docs/service-migrations/migrate-to-aku-content.sh` |
| 6b | Full exam papers migration (local machine) — `data/exam_papers/` → Akudemy | `./docs/service-migrations/migrate-exam-papers.sh` |
| 6c | Full SmartBoard migration (local machine) — `akulearn-linux-app/` → Aku-SmartBoard | `./docs/service-migrations/migrate-to-aku-smartboard.sh` |
| 7 | Kubernetes staging: create GHCR pull secret → apply `docs/deployment/k8s/` manifests | `kubectl apply -f docs/deployment/k8s/` (cluster access required) |

**Full operator runbook with exact navigation steps:**
→ `docs/runbooks/post-remediation-runbook.md`

Mark each step `✅ Done` in the table above as it completes.
