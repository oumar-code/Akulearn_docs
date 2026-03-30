# Automation Progress Tracker

This markdown file will record the step-by-step progress of implementing automation (CI/CD, testing, linting, deployment, documentation builds) across all repositories in the stack.

## Repositories
- AkuAI
- AkuTutor
- AkuWorkspace
- DaaS
- EdgeHub
- IGHub
- SuperHub
- Telhone
- Akulearn_docs


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
- [ ] Remove Node.js files
- [ ] Scaffold Python/FastAPI project structure
- [ ] Implement offline-first content cache, sync, device registration endpoints
- [ ] Add Dockerfile (multi-stage, non-root)
- [ ] Add `docker-compose.yml`
- [ ] Add `.github/workflows/ci.yml` (pytest + ruff + docker build)
- [ ] Update README with Python/FastAPI instructions

#### Aku-SuperHub
- [ ] Remove Node.js files
- [ ] Scaffold Python/FastAPI project structure
- [ ] Implement fleet management, regional analytics, model fine-tuning endpoints
- [ ] Add Dockerfile, docker-compose, CI workflow
- [ ] Update README

#### Aku-IGHub
- [ ] Remove Node.js/TypeScript files
- [ ] Scaffold Python/FastAPI project structure
- [ ] Implement credential registry, Aku Coin clearing, anonymised metadata exchange endpoints
- [ ] Add Dockerfile, docker-compose, CI workflow
- [ ] Update README

#### Akudemy
- [ ] Remove Node.js files
- [ ] Scaffold Python/FastAPI project structure
- [ ] Implement content sync API, teacher/admin tools, blockchain credential issuance
- [ ] Add Dockerfile, docker-compose, CI workflow
- [ ] Update README

#### AkuAI
- [ ] Remove Node.js files
- [ ] Scaffold Python/FastAPI project structure
- [ ] Implement shared inference endpoints (text-gen, classify, summarize, Gemma relay)
- [ ] Add Dockerfile, docker-compose, CI workflow
- [ ] Update README

#### AkuTutor
- [ ] Remove Node.js files
- [ ] Scaffold Python/FastAPI project structure
- [ ] Implement AI Tutor session, Q&A, feedback endpoints (calls AkuAI — no local model)
- [ ] Add Dockerfile, docker-compose, CI workflow
- [ ] Update README

#### AkuWorkspace
- [ ] Remove Node.js files
- [ ] Scaffold Python/FastAPI project structure
- [ ] Implement NL workflow orchestration, AI Assistant abstraction layer
- [ ] Add Dockerfile, docker-compose, CI workflow
- [ ] Update README

#### Aku-DaaS
- [ ] Remove Node.js files (note: existing stub has wrong domain — "device management", not data governance)
- [ ] Scaffold Python/FastAPI project structure
- [ ] Implement dataset ingestion, anonymisation pipeline, IG-Hub metadata publishing
- [ ] Add Dockerfile, docker-compose, CI workflow
- [ ] Update README

#### Aku-Telhone
- [ ] Remove Node.js files (note: existing stub has wrong domain — generic telephony, not eSIM)
- [ ] Scaffold Python/FastAPI project structure
- [ ] Implement eSIM provisioning, OTA SIM lifecycle, network switching, device attestation
- [ ] Add Dockerfile, docker-compose, CI workflow
- [ ] Update README

---

## Frontend Consolidation

**Decision: `akulearn-dashboard/` (inside Akulearn_docs) is the canonical frontend.**

| Repo | Action |
|------|--------|
| `akulearn-dashboard/` (this monorepo) | **Active** — Vercel deployed, all new work goes here |
| `Akudemy-frontend` | Archive — minimal stub, no active development |
| `akulearn-dashB` | Archive — bootstrapped Next.js, no active development |
| `Akulearn-dashboard` | Archive — empty shell |

- [ ] Archive `Akudemy-frontend`
- [ ] Archive `akulearn-dashB`
- [ ] Archive `Akulearn-dashboard`

---

## KMP Mobile Migration

**Decision: `KOTLIN MULTIPLATFORM/` will be moved to `oumar-code/Aku-Mobile`.**

- [ ] Create `oumar-code/Aku-Mobile` repository
- [ ] Move `KOTLIN MULTIPLATFORM/` contents to new repo
- [ ] Update `docs/03-mobile/index.md` with link to `Aku-Mobile`
- [ ] Remove `KOTLIN MULTIPLATFORM/` from `Akulearn_docs` after migration confirmed

---

_Last updated: 2026-03-30 — Python/FastAPI migration, frontend consolidation, KMP migration decisions recorded._

---

## Service Migration Scaffolds

Ready-to-apply migration resources are in `docs/service-migrations/`:

| Resource | Location |
|----------|----------|
| Priority-ordered migration tracker | `docs/service-migrations/index.md` |
| Parameterised bootstrap script | `docs/service-migrations/bootstrap.sh` |
| Frontend archive notices | `docs/service-migrations/frontend-archive-notices.md` |
| KMP migration runbook | `docs/03-mobile/kmp-migration-runbook.md` |
| Contracts repo proposal | `docs/aku-platform-contracts.md` |

### Backend Service Migration Status (Priority Order)

> **Scaffolds ready** — all 9 service scaffold packages are in `docs/service-migrations/scaffolds/<ServiceName>/`.  
> Apply to each repo with: `./bootstrap.sh <ServiceName>` then overlay the matching scaffold directory.

| Priority | Repo | Scaffold | PR Status |
|----------|------|----------|-----------|
| 1 | [AkuAI](https://github.com/oumar-code/AkuAI) | ✅ Scaffold ready (`scaffolds/AkuAI/`) | ⬜ PR not opened |
| 2 | [Akudemy](https://github.com/oumar-code/Akudemy) | ✅ Scaffold ready (`scaffolds/Akudemy/`) | ⬜ PR not opened |
| 3 | [Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub) | ✅ Scaffold ready (`scaffolds/Aku-EdgeHub/`) | ⬜ PR not opened |
| 4a | [Aku-IGHub](https://github.com/oumar-code/Aku-IGHub) | ✅ Scaffold ready (`scaffolds/Aku-IGHub/`) | ⬜ PR not opened |
| 4b | [Aku-Telhone](https://github.com/oumar-code/Aku-Telhone) | ✅ Scaffold ready (`scaffolds/Aku-Telhone/`) | ⬜ PR not opened |
| 5a | [Aku-SuperHub](https://github.com/oumar-code/Aku-SuperHub) | ✅ Scaffold ready (`scaffolds/Aku-SuperHub/`) | ⬜ PR not opened |
| 5b | [AkuTutor](https://github.com/oumar-code/AkuTutor) | ✅ Scaffold ready (`scaffolds/AkuTutor/`) | ⬜ PR not opened |
| 5c | [AkuWorkspace](https://github.com/oumar-code/AkuWorkspace) | ✅ Scaffold ready (`scaffolds/AkuWorkspace/`) | ⬜ PR not opened |
| 5d | [Aku-DaaS](https://github.com/oumar-code/Aku-DaaS) | ✅ Scaffold ready (`scaffolds/Aku-DaaS/`) | ⬜ PR not opened |

#### Per-Service Scaffold Checklist

For each service repo, the following steps apply the scaffold:

- [ ] Delete `package.json`, `index.js`, `src/` (Node.js files)
- [ ] Copy `docs/service-migrations/bootstrap.sh` into repo root and run `./bootstrap.sh <ServiceName>`
- [ ] Overlay matching `docs/service-migrations/scaffolds/<ServiceName>/` files into repo
- [ ] Review and update `app/config.py` with service-specific env vars
- [ ] Add service-specific `requirements-extra.txt` lines to `requirements.txt`
- [ ] Verify `Dockerfile` multi-stage build (non-root user `aku`, uid 1001)
- [ ] Verify `docker-compose.yml` local dev setup
- [ ] Verify `.github/workflows/ci.yml` (lint + test + docker build)
- [ ] Update `README.md` with Python/FastAPI getting started instructions
- [ ] Open PR with `feat: migrate to Python 3.11 / FastAPI` message
- [ ] Update status in this table once PR is merged

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
| Archive `Akudemy-frontend` | ⬜ Pending |
| Archive `akulearn-dashB` | ⬜ Pending |
| Archive `Akulearn-dashboard` | ⬜ Pending |

### KMP Mobile Migration Status

| Action | Status |
|--------|--------|
| Create `oumar-code/Aku-Mobile` repository | ⬜ Pending |
| Copy `KOTLIN MULTIPLATFORM/` to new repo | ⬜ Pending |
| Add CI workflow to `Aku-Mobile` | ⬜ Pending |
| Update `docs/03-mobile/index.md` | ✅ Done |
| Update `docs/ecosystem-map.md` | ✅ Done |
| Remove `KOTLIN MULTIPLATFORM/` from `Akulearn_docs` | ⬜ Pending (after confirmation) |

### Contracts Repo Status

| Action | Status |
|--------|--------|
| Create `oumar-code/aku-platform-contracts` | ⬜ Pending (after AkuAI migration) |
| Define initial Pydantic schemas (inference, content, credentials) | ⬜ Pending |
| Publish to GitHub Packages | ⬜ Pending |
