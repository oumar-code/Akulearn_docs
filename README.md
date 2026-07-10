# Akulearn Documentation Repository

![CI](https://github.com/oumar-code/Akulearn_docs/actions/workflows/automation.yml/badge.svg)

This repository is the public documentation workspace for the Akulearn ecosystem.
It is curated for external stakeholders (including the iDICE Founders Lab team) to quickly understand what Akulearn is building, what is live in the MVP, and how platform components fit together.

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
| [Aku-Telhone](https://github.com/oumar-code/Aku-Telhone) | Connectivity model: app-first access, then SIM/eSIM scale |
| [Aku-Hardware](https://github.com/oumar-code/Aku-Hardware) | Edge Hub hardware design, power system, firmware, test procedures |

### Frontend (canonical: this monorepo)

| Location | Role |
|----------|------|
| `akulearn-dashboard/` | Marketing site + all dashboard pages — Vercel deployed |

## Project Overview

Akulearn is building an education + connectivity ecosystem designed for connected and underserved communities across Africa. The platform combines localized edge infrastructure, AI-enabled learning services, and practical connectivity models to reduce costs while improving access.

## What's Inside

This repository is organized for clarity and ease of navigation:

- **[docs/ecosystem-map.md](docs/ecosystem-map.md)**: Master map of all repos, roles, and status
- **[docs/service-templates/](docs/service-templates/)**: Python/FastAPI bootstrap guide for all service repos
- **[docs/00-project-overview/](docs/00-project-overview/)**: Vision, mission, and Phase 1 roadmap
- **[docs/01-architecture/](docs/01-architecture/)**: System architecture, ADRs, and design documents
- **[docs/02-backend/](docs/02-backend/)**: Backend handbook, API specs, and database schemas
- **[docs/03-mobile/](docs/03-mobile/)**: Mobile app guidelines
- **[docs/04-iot-projector/](docs/04-iot-projector/)**: IoT projector guidelines
- **[docs/05-cross-cutting/](docs/05-cross-cutting/)**: Technical specs and coding standards
- **[docs/06-process-methodology/](docs/06-process-methodology/)**: Agile/DevOps methodology
- **[docs/07-glossary/](docs/07-glossary/)**: Glossary of Akulearn terms
- **[docs/images/](docs/images/)**: Diagrams and screenshots
- **[akulearn-dashboard/](akulearn-dashboard/)**: Canonical Next.js frontend (source of truth)
- **[client_examples/](client_examples/)**: Apollo/GraphQL + WebSocket + D3 visualization SDK examples
- **[aku_platform_contracts/](aku_platform_contracts/)**: Shared Pydantic schemas, OpenAPI specs, Kafka topic constants

## Deployment & Automation

CI/CD, linting, and documentation builds are automated via [GitHub Actions](.github/workflows/automation.yml) and [docs-deploy.yml](.github/workflows/docs-deploy.yml).

### Automation Steps
- Linting (ESLint, placeholder for docs)
- Docs build (MkDocs)
- Docs deployment (GitHub Pages)
- Mermaid diagram rendering (render-mermaid.yml)

## How to View Documentation

To view the documentation locally:

```sh
pip install mkdocs mkdocs-material
mkdocs serve
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## Repository Structure

| Directory | Purpose |
|---|---|
| `akulearn-dashboard/` | Canonical Next.js frontend — marketing site + all dashboard pages |
| `docs/` | Platform documentation (MkDocs site) |
| `client_examples/` | Apollo/GraphQL + WebSocket + D3 visualization SDK examples |
| `aku_platform_contracts/` | Shared Pydantic schemas, OpenAPI specs, Kafka topic constants |

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests or opening issues.

## Contact

For questions, feedback, or partnership inquiries, please contact the Aku Platform team (details coming soon).
