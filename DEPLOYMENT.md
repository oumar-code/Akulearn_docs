# Akulearn Deployment Guide

## Documentation Site (Vercel)

The MkDocs documentation site is deployed to Vercel from the `main` branch of the GitHub repository.

### How Vercel deployment works

Vercel is connected to the `oumar-code/Akulearn_docs` GitHub repository. Every push to `main` automatically triggers a new deployment — no local directory setup is required.

The `vercel.json` in the repository root tells Vercel how to build the site:

```json
{
  "buildCommand": "mkdocs build",
  "outputDirectory": "site",
  "installCommand": "pip install mkdocs mkdocs-material"
}
```

A `.vercelignore` file at the repository root ensures Vercel only processes the `docs/` folder and `mkdocs.yml`, skipping the Python scripts, data files, and other development artifacts present in the main worktree.

### Local preview

```sh
pip install mkdocs mkdocs-material
mkdocs serve
# Open http://localhost:8000
```

### Note on git worktrees

If you have both `Akulearn_docs/` (main worktree) and `Akulearn_docs.worktrees/` (linked worktree) open in VSCode, **connect Vercel to the GitHub repository, not to either local directory.** See `GIT_WORKTREE_STRATEGY.md` for a full explanation of the two-directory setup.

---

## Backend Microservices
- Use Docker or systemd to run FastAPI microservices (ai_tutor_service, polls_service, etc.)
- Example Docker Compose:
  ```yaml
  version: '3'
  services:
    ai_tutor:
      build: ./akulearn_microservices/ai_tutor_service
      ports:
        - "8001:8000"
    polls:
      build: ./akulearn_microservices/polls_service
      ports:
        - "8002:8000"
    # Add other services similarly
  ```

## Frontend
- Build and deploy Vue app from `unconnected_stack/frontend`
- Example:
  ```sh
  npm install
  npm run build
  # Deploy dist/ to your web server
  ```

## Systemd Service Example
- For Linux/Ubuntu, create a unit file for each service:
  ```ini
  [Unit]
  Description=Akulearn AI Tutor Service
  After=network.target

  [Service]
  ExecStart=/usr/bin/python3 /path/to/ai_tutor_service/main.py
  Restart=always
  User=akulearn

  [Install]
  WantedBy=multi-user.target
  ```

## OTA Updates
- Use `ota_update.sh` to pull latest code and restart services.

---
See individual microservice and frontend docs for more details.
