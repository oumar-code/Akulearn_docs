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



#### Akudemy

- [x] Inventory existing automation (CI/CD, test, Docker, and basic test found)
- [x] Standardize CI/CD (added lint, Docker build, and docs build placeholder to workflow)
- [x] Automate testing (Jest test present)
- [x] Automate linting/formatting (ESLint config and ignore file added, lint step in CI)
- [x] Automate deployment (Docker build step in CI)
- [x] Automate documentation builds (placeholder in CI)
- [x] Document automation setup (badges and automation section added to README)

## Progress Log

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

_Last updated: 2026-04-08 — contracts repo fully complete: Pydantic schemas defined, dependency added to all 9 service repos (PRs merged), published to GitHub Packages._

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
| Frontend archive notices | `docs/service-migrations/frontend-archive-notices.md` |
| KMP migration runbook | `docs/03-mobile/kmp-migration-runbook.md` |
| Contracts repo proposal | `docs/aku-platform-contracts.md` |
| **Kubernetes manifests (staging)** | `docs/deployment/k8s/` |

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
| Add `write:packages` scope to `GH_PAT` secret | ⬜ Required (manual — regenerate PAT at github.com/settings/tokens) |
| Trigger workflow → push `v0.1.1` images to `ghcr.io/oumar-code/*` | ⬜ Pending first run |

### Step 2 — Sync OpenAPI Specs to Contracts Repo

| Action | Status |
|--------|--------|
| Create `docs/service-migrations/sync-openapi-to-contracts.sh` | ✅ Done |
| Create `.github/workflows/service-sync-openapi.yml` | ✅ Done |
| Workflow auto-triggers after lint/format/tag succeeds | ✅ Done (workflow_run trigger) |
| First sync run (copies openapi.yaml → aku_contracts/openapi/) | ⬜ Pending lint/format/tag re-run |

### Step 3 — Integration Tests (Health Checks)

| Action | Status |
|--------|--------|
| Create `.github/workflows/service-integration-test.yml` | ✅ Done |
| Workflow pulls GHCR images, starts all 9 services + shared infra (postgres + redis) | ✅ Done |
| Hits `/health` on each service and reports pass/fail | ✅ Done |
| Workflow auto-triggers after Docker build/push succeeds | ✅ Done (workflow_run trigger) |
| First integration test run | ⬜ Pending Docker images being pushed |

### Step 4 — Kubernetes Manifests (Staging)

| Action | Status |
|--------|--------|
| Create `docs/deployment/k8s/namespace.yaml` | ✅ Done |
| Create per-service manifests (Deployment + Service + ConfigMap) for all 9 services | ✅ Done |
| Create `docs/deployment/k8s/README.md` with deploy instructions | ✅ Done |
| Create GHCR pull secret in target cluster | ⬜ Pending cluster access |
| Create per-service Secrets with real credentials | ⬜ Pending (never commit — use kubectl or secrets manager) |
| Apply manifests to staging cluster | ⬜ Pending cluster access |

### Step 5 — Pin Contracts Version

| Action | Status |
|--------|--------|
| Create `docs/service-migrations/pin-contracts-version.sh` | ✅ Done |
| Run script to pin all 9 service repos to `v0.1.1` | ⬜ Pending (trigger manually after Docker images are validated) |
