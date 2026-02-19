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

## Vercel Deployment and the Two Worktree Directories

A common question when working with two VSCode windows (one for `Akulearn_docs`, one for `Akulearn_docs.worktrees`) is: **which directory do I use to deploy to Vercel?**

**Short answer: Neither. Vercel deploys directly from GitHub, not from a local directory.**

When you connect Vercel to your repository, it watches the `main` branch on GitHub. Every push to `main` triggers a new deployment — your local directories are never involved after the initial project setup.

| Local Directory | Purpose | Used by Vercel? |
|---|---|---|
| `Akulearn_docs/` | Main worktree — day-to-day development, scripts, tests | No (Vercel reads from GitHub) |
| `Akulearn_docs.worktrees/` | Linked worktree — clean reference copy for comparison | No (local only) |

**Yes, the two directories are supposed to be separate.** `Akulearn_docs.worktrees` is a git linked worktree created with `git worktree add`. It lets you view a clean branch alongside your messy work-in-progress without cloning again.

**Do not point Vercel to `Akulearn_docs.worktrees`.** Link Vercel to the `oumar-code/Akulearn_docs` GitHub repository and deploy from the `main` branch. The repository contains a `.vercelignore` file that excludes all development scripts, Python files, and data directories so Vercel only processes the `docs/` folder and `mkdocs.yml`.

---

## CI/CD and the Main Worktree

All GitHub Actions workflows that deploy live services (`docs-deploy.yml`, `connected_backend_gcp_deploy.yml`, `projector_hub_gcp_deploy.yml`, etc.) are scoped to `branches: [main]`. This means:

- **The main worktree is the deployment gate.** Only code merged to `main` is deployed.
- Workflows use `fetch-depth: 0` where full git history is required (e.g. changelog generation, diff-based checks, worktree comparisons).
- The nightly `automation.yml` validates that the main worktree is healthy before any scheduled operations run.

### Path-Filtered Triggers

Workflows in this repo are path-filtered so that only the jobs relevant to a particular change run. This keeps CI fast and avoids unnecessary deploys from the main worktree.

| Workflow | Trigger path(s) |
|---|---|
| `docs-deploy.yml` | `docs/**`, `mkdocs.yml` |
| `connected_backend_gcp_deploy.yml` | `connected_stack/**` |
| `projector_hub_ci.yml` | `unconnected_stack/**` |
| `demo-ci.yml` | `mlops/**`, `requirements.txt` |
| `ci-data-sanitizer.yml` | `infra/examples/**`, `tests/**` |

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
