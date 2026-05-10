# Akulearn Documentation Repository

![CI](https://github.com/oumar-code/Akulearn_docs/actions/workflows/automation.yml/badge.svg)

Welcome to the Akulearn documentation repository! This space contains all official documentation for the Akulearn EdTech platform, designed to empower learners and educators across Nigeria and Africa.

## Key Platform Decisions

| Decision | Choice |
|----------|--------|
| **Backend language** | Python 3.11 / FastAPI (all services) |
| **Frontend / Dashboard** | `akulearn-dashboard/` in this monorepo (Next.js 16.1.6) — canonical Vercel deployment |
| **Mobile** | Kotlin Multiplatform — migrating to `oumar-code/Aku-Mobile` |
| **Documentation** | This repo (`Akulearn_docs`) — MkDocs site on GitHub Pages |

## Ecosystem Repository Map

> Full details: [`docs/ecosystem-map.md`](docs/ecosystem-map.md)

### Backend Services (Python / FastAPI)

| Repo | Role |
|------|------|
| [Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub) | Tier 1 — Offline edge server, local AI inference, device sync |
| [Aku-SuperHub](https://github.com/oumar-code/Aku-SuperHub) | Tier 2 — Regional analytics, fleet management |
| [Aku-IGHub](https://github.com/oumar-code/Aku-IGHub) | Tier 3 — Global gateway, Aku Coin clearing, credential registry |
| [Akudemy](https://github.com/oumar-code/Akudemy) | Aku Learn — content delivery, offline sync, blockchain credentials |
| [AkuAI](https://github.com/oumar-code/AkuAI) | Shared AI/ML inference layer (text-gen, classify, Gemma) |
| [AkuTutor](https://github.com/oumar-code/AkuTutor) | AI Tutor — curriculum Q&A, feedback loops |
| [AkuWorkspace](https://github.com/oumar-code/AkuWorkspace) | AI-Native Productivity Suite |
| [Aku-DaaS](https://github.com/oumar-code/Aku-DaaS) | Data governance — anonymised datasets, IG-Hub publishing |
| [Aku-Telhone](https://github.com/oumar-code/Aku-Telhone) | eSIM provisioning — OTA SIM lifecycle, MVNO (Telhone brand) |
| [Aku-Hardware](https://github.com/oumar-code/Aku-Hardware) | Edge Hub hardware design, power system, firmware (INA3221), test procedures |

### Frontend (canonical: this monorepo)

| Location | Role |
|----------|------|
| `akulearn-dashboard/` | Marketing site + all dashboard pages — Vercel deployed |

## Project Overview

Akulearn is an innovative EdTech initiative with a mission to make quality, personalized, and verifiable education universally accessible. Our hybrid learning ecosystem leverages technology—including AI, blockchain, and solar-powered hardware—to deliver engaging, curriculum-aligned content to both connected and underserved communities.

## What's Inside

This repository is organized for clarity and ease of navigation:

- **docs/ecosystem-map.md**: Master map of all repos, roles, and status
- **docs/service-templates/**: Python/FastAPI bootstrap guide for all service repos
- **docs/00-project-overview/**: Vision, mission, and Phase 1 roadmap
- **docs/01-architecture/**: System architecture, ADRs, and design documents
- **docs/02-backend/**: Backend handbook, API specs, and database schemas
- **docs/03-mobile/**: Mobile app guidelines
- **docs/04-iot-projector/**: IoT projector guidelines
- **docs/05-cross-cutting/**: Technical specs and coding standards
- **docs/06-process-methodology/**: Agile/DevOps methodology
- **docs/07-glossary/**: Glossary of Akulearn terms
- **docs/images/**: Diagrams and screenshots
- **akulearn-dashboard/**: Canonical Next.js frontend (source of truth)
- **client_examples/**: Apollo/GraphQL + WebSocket + D3 visualization SDK examples
- **aku_platform_contracts/**: Shared Pydantic schemas, OpenAPI specs, Kafka topic constants

### Strategic Roadmap & Thought Leadership
- **docs/clean_energy_for_africa.md**: Clean energy research and vision for Africa
- **docs/clean_energy_whitepaper.md**: Whitepaper on clean energy and digital transformation
- **docs/ai_automation_industry4.md**: AI, automation, and Industry 4.0 for Africa
- **docs/aku_change_maker.md**: Aku’s role as a change maker and ecosystem builder

## How to Contribute

We welcome contributions! Please check back soon for our contribution guidelines and process.


## Deployment & Automation

CI/CD, linting, and documentation builds are automated via [GitHub Actions](.github/workflows/automation.yml) and [docs-deploy.yml](.github/workflows/docs-deploy.yml).

### Automation Steps
- Linting (ESLint, placeholder for docs)
- Docs build (MkDocs)
- Docs deployment (GitHub Pages)
- Mermaid diagram rendering (render-mermaid.yml)
- Progress tracked in automation_progress.md

## How to View Documentation

To view the documentation locally:

1. Install [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

2. In your terminal, run:

   ```sh
   pip install mkdocs mkdocs-material
   mkdocs serve
   ```

3. Open [http://localhost:8000](http://localhost:8000) in your browser to explore the docs.

## Team Setup & Supabase Provisioning

Both `team.py` and `supabase_provision.py` live at the **project root** and must be run from there.

### 1. View team dashboards (`team.py`)

```sh
# From the project root directory (e.g. Akulearn_docs/)
python team.py
```

Prints every team member's name, role, dashboard key, and the full list of platform accesses they have.

### 2. Provision team members in Supabase (`supabase_provision.py`)

**Prerequisites** — copy `.env.example` to `.env` and fill in your values:

```sh
cp .env.example .env
# then edit .env and set:
#   SUPABASE_URL              = https://your-project-ref.supabase.co
#   SUPABASE_SERVICE_ROLE_KEY = <service_role key from Supabase Dashboard → Project Settings → API>
#   RESEND_API_KEY            = <optional — only needed to email credentials>
```

**Run the provisioning script:**

```sh
# From the project root directory (e.g. Akulearn_docs/)
python supabase_provision.py
```

- If `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` are not set, the script runs in **dry-run mode** — it prints the team roster with sample credentials but does **not** create any accounts.
- When the credentials are present, the script creates each team member's account in Supabase with the correct role and dashboard assigned.
- If `RESEND_API_KEY` is also set, each newly created user receives a welcome email with their temporary password.

> ⚠ Never commit your `.env` file. It is already listed in `.gitignore`.

## Repository Structure

| Directory | Purpose |
|---|---|
| `akulearn-dashboard/` | Canonical Next.js frontend — marketing site + all dashboard pages |
| `docs/` | Platform documentation (MkDocs site) |
| `client_examples/` | Apollo/GraphQL + WebSocket + D3 visualization SDK examples |
| `aku_platform_contracts/` | Shared Pydantic schemas, OpenAPI specs, Kafka topic constants |

Full documentation structure:

- **`docs/ecosystem-map.md`** — Master map of all repos, roles, and migration status
- **`docs/00-project-overview/`** — Vision, mission, and Phase 1 roadmap
- **`docs/01-architecture/`** — System architecture and design documents
- **`docs/02-backend/`** — Backend handbook, API specs, and database schemas
- **`docs/03-mobile/`** — Mobile app guidelines (links to `oumar-code/Aku-Mobile`)
- **`docs/04-iot-projector/`** — IoT projector guidelines
- **`docs/05-cross-cutting/`** — Technical specs and coding standards
- **`docs/06-process-methodology/`** — Agile/DevOps methodology
- **`docs/07-glossary/`** — Glossary of Aku terms
- **`docs/client-sdk/`** — Client SDK integration guide

## Getting Started

### Documentation Site
```sh
pip install mkdocs mkdocs-material
mkdocs serve
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

### Backend Services
Each service repo has its own Python/FastAPI scaffold (see `docs/service-templates/python-fastapi-bootstrap.md`):
```sh
# In any service repo (AkuAI, Akudemy, Aku-EdgeHub, etc.)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Mobile App (Android / iOS)
See [`oumar-code/Aku-Mobile`](https://github.com/oumar-code/Aku-Mobile) for full setup instructions.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests or opening issues.

## Contact

For questions, feedback, or partnership inquiries, please contact the Aku Platform team (details coming soon).

---

## Interactive Zamfara Network Map

[![Zamfara Network Map Preview](docs/network-map/preview.png)](https://oumar-code.github.io/Akulearn_docs/docs/network-map/)

> **Click the image above or [this link](https://oumar-code.github.io/Akulearn_docs/docs/network-map/) to view the interactive Zamfara mesh network map.**

---

Thank you for helping us build a brighter future for education and connectivity!
