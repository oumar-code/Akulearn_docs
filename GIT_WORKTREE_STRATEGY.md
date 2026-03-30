# Git Worktree Strategy for Akulearn

## What Is the Main Worktree?

Every git repository has a **primary (main) worktree** — the working directory created when you first clone or `git init` the repository. In Akulearn_docs this is the checkout you work in day-to-day. Additional worktrees can be linked to it with `git worktree add`, allowing you to check out other branches into separate directories **without cloning the repository again** and without losing your current working state.

---

## Why Leverage the Main Worktree?

| Benefit | Detail |
|---|---|
| **Parallel development** | Keep `main` always accessible in the main worktree while developing features in a linked worktree |
| **Fast hotfixes** | Patch `main` directly from its own directory without stashing feature work |
| **CI/CD baseline** | All deployment workflows in this repo run on `main`; the main worktree is the authoritative source of truth |
| **No re-cloning** | Linked worktrees share the same `.git` object store — fast and disk-efficient |
| **Side-by-side comparison** | Easily diff a feature branch against `main` using two terminal windows |

---

## Recommended Developer Workflow

### 1 — Set Up a Linked Worktree for Feature Work

```bash
# From the repository root (main worktree on branch main):
git worktree add ../akulearn-feature my-feature-branch

# This creates ../akulearn-feature/ checked out on my-feature-branch.
# Your main worktree stays on main.
```

### 2 — Keep Main Clean

The main worktree should **always** match the latest `origin/main`.

```bash
# In the main worktree:
git pull --ff-only origin main
```

Never commit experimental or in-progress work directly to main.

### 3 — Hot-Fix Workflow

```bash
# From the main worktree (branch: main):
git worktree add ../akulearn-hotfix hotfix/critical-fix

cd ../akulearn-hotfix
# … make the fix …
git commit -am "fix: correct critical bug"
git push origin hotfix/critical-fix
# Open a PR → merge to main → CI deploys automatically
```

### 4 — Tear Down Worktrees When Done

```bash
git worktree remove ../akulearn-feature
git worktree prune          # clean up stale references
```

---

## CI/CD and the Main Worktree

All GitHub Actions workflows that deploy live services (`docs-deploy.yml`, `vercel-deploy.yml`, etc.) are scoped to `branches: [main]`. This means:

- **The main worktree is the deployment gate.** Only code merged to `main` is deployed.
- Workflows use `fetch-depth: 0` where full git history is required (e.g. changelog generation, diff-based checks, worktree comparisons).
- The nightly `automation.yml` validates that the main worktree is healthy before any scheduled operations run.

### Path-Filtered Triggers

Workflows in this repo are path-filtered so that only the jobs relevant to a particular change run. This keeps CI fast and avoids unnecessary deploys from the main worktree.

| Workflow | Trigger path(s) |
|---|---|
| `docs-deploy.yml` | `docs/**`, `mkdocs.yml` |
| `vercel-deploy.yml` | `akulearn-dashboard/**` |
| `render-mermaid.yml` | `docs/**/*.md` |
| `automation.yml` | Nightly schedule |

---

## Branching Model

```
main (main worktree — always deployable)
 ├── feature/xxx          → linked worktree ../akulearn-feature
 ├── hotfix/yyy           → linked worktree ../akulearn-hotfix
 └── docs/zzz             → linked worktree ../akulearn-docs
```

Feature and docs branches are developed in **linked worktrees** and merged to `main` via Pull Requests. The main worktree never accumulates WIP commits.

---

## Active Service Repositories

This monorepo (`Akulearn_docs`) is the documentation and frontend hub. The following separate repos contain the service implementations. Each must be developed independently and linked back to this repo's specs via `docs/ecosystem-map.md`.

### Backend Services (Python / FastAPI)

| Repo | Tier / Role | GitHub |
|------|-------------|--------|
| `Aku-EdgeHub` | Tier 1 — Offline edge server, local AI, device sync | https://github.com/oumar-code/Aku-EdgeHub |
| `Aku-SuperHub` | Tier 2 — Regional analytics, fleet management | https://github.com/oumar-code/Aku-SuperHub |
| `Aku-IGHub` | Tier 3 — Global gateway, Aku Coin clearing, credentials | https://github.com/oumar-code/Aku-IGHub |
| `Akudemy` | Aku Learn service — content delivery, offline sync | https://github.com/oumar-code/Akudemy |
| `AkuAI` | Shared AI/ML inference layer | https://github.com/oumar-code/AkuAI |
| `AkuTutor` | AI Tutor — curriculum Q&A, feedback loops | https://github.com/oumar-code/AkuTutor |
| `AkuWorkspace` | AI-Native Productivity Suite | https://github.com/oumar-code/AkuWorkspace |
| `Aku-DaaS` | Data governance — anonymised dataset pipelines | https://github.com/oumar-code/Aku-DaaS |
| `Aku-Telhone` | eSIM provisioning — OTA SIM lifecycle, MVNO | https://github.com/oumar-code/Aku-Telhone |

### Frontend (Next.js — canonical inside this monorepo)

| Location | Role |
|----------|------|
| `akulearn-dashboard/` (this repo) | **Source of truth** — all dashboard and marketing pages |

### Mobile (Kotlin Multiplatform)

| Repo | Role |
|------|------|
| `KOTLIN MULTIPLATFORM/` (this repo — migrating) | KMP shared library — migrating to `oumar-code/Aku-Mobile` |
| `Aku-Mobile` (to create) | Standalone KMP repo for Android + iOS |

---

## Working Across Repos with Worktrees

When you need to work on a service repo alongside this docs repo simultaneously:

```bash
# Clone the service repo as a worktree sibling
cd ..
git clone https://github.com/oumar-code/Aku-EdgeHub
# Then use separate terminals for each repo
```

Use the service spec from `docs/services/` or `docs/components/` in this monorepo as the contract while implementing in the service repo.

---

## Useful Commands

```bash
# List all worktrees for this repo
git worktree list

# Add a new worktree from an existing branch
git worktree add <path> <branch>

# Add a new worktree and create the branch at the same time
git worktree add -b feature/new-module ../akulearn-new-module main

# Remove a worktree (must have no uncommitted changes)
git worktree remove <path>

# Remove stale worktree references
git worktree prune

# Lock a worktree so it isn't accidentally pruned
git worktree lock <path> --reason "active sprint"
```

---

## Tips

- Keep the **main worktree** on the `main` branch at all times — treat it as the production mirror.
- Add worktree paths (e.g. `../akulearn-*/`) to your global `.gitignore_global` so they are never accidentally staged.
- CI uses `fetch-depth: 0` to allow `git log`, `git diff main...HEAD`, and other history-aware commands to work correctly inside any worktree.
- For large parallel tasks (e.g. generating content while also working on API changes), separate worktrees prevent merge conflicts and keep each concern isolated.
- All service contracts (API specs, schemas, architecture decisions) live in **this repo's `docs/`** — always update the docs before or alongside the service implementation.
