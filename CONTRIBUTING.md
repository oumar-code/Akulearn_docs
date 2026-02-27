# Contributing to Akulearn Docs

Thank you for your interest in contributing! This guide explains how to get started.

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/Akulearn_docs.git
   cd Akulearn_docs
   ```
3. Create a new **feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Making Changes

- Keep commits focused and atomic.
- Write clear commit messages (e.g. `Add Wave3 API client stub`).
- Follow the existing code style for the area you are editing.

## Pushing and Opening a PR

1. Fetch and merge the latest changes from `main` **before** pushing to avoid a non-fast-forward rejection:
   ```bash
   git fetch origin
   git merge origin/main
   ```
2. Push your branch:
   ```bash
   git push -u origin feature/your-feature-name
   ```
3. Open a **Pull Request** on GitHub against the `main` branch.

## What NOT to Commit

The following are excluded by `.gitignore` and must never be committed:

| Pattern | Reason |
|---|---|
| `.gradle/` | Gradle build cache — regenerated automatically |
| `local.properties` | Local SDK paths — different on every machine |
| `*.env` | Secrets and environment variables |
| `site/` | MkDocs build output |

If you accidentally staged these files, remove them from tracking:
```bash
git rm --cached -r .gradle/ local.properties
```
Then commit the removal before pushing.

## Deploying the Docs Site

See the deployment instructions in [`README.md`](README.md) for Vercel deployment steps.

## Questions

Open an issue or start a discussion on GitHub if you have questions.
