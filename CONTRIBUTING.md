# Contributing to the Aku Platform

Thank you for your interest in contributing! This guide will help you get started quickly.

## Repository Structure

This is a multi-technology monorepo. The primary areas of active development are:

| Directory | Technology | Notes |
|---|---|---|
| KOTLIN MULTIPLATFORM/ | Kotlin, Android, iOS | Mobile apps — main Phase 5 focus |
| supabase/ | SQL, Edge Functions | Auth and database schema |
| docs/ | Markdown, MkDocs | Platform documentation |
| wave3_rest_api.py and related | Python | Content and recommendation backend |
| infra/ / kubernetes/ | Docker, K8s | Infrastructure |

## Getting Started

1. Fork this repository and clone your fork.
2. For the mobile app, follow the setup guide in KOTLIN MULTIPLATFORM/README.md.
3. For the docs site: pip install mkdocs mkdocs-material && mkdocs serve
4. For the Python backend: pip install -r requirements.txt

## Branching Strategy

| Branch | Purpose |
|---|---|
| main | Production-ready code only |
| develop | Integration branch — all PRs target here |
| feature/<name> | New features |
| fix/<name> | Bug fixes |
| docs/<name> | Documentation updates |

## Pull Request Process

1. Branch from develop: git checkout -b feature/your-feature develop
2. Keep PRs focused — one concern per PR.
3. Write or update tests for any logic changes in shared/.
4. Ensure the build passes locally before opening a PR:
   ./gradlew :shared:build :shared:allTests
5. Fill in the PR template fully.
6. Request a review from a maintainer.

## Code Style

- Kotlin: Follow Kotlin Coding Conventions.
- Python: Follow PEP 8.
- Commits: Use conventional commits — feat:, fix:, docs:, chore:, test:.

## Reporting Issues

Open a GitHub Issue and include:
- A clear title and description
- Steps to reproduce
- Expected vs actual behaviour
- Platform and version (e.g. Android API 26, iOS 16)
