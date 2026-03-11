# Akulearn Documentation Deployment Guide

This guide explains how to build, preview, and deploy the Akulearn documentation site.

## Overview

The Akulearn documentation is built with [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It is deployed automatically to **GitHub Pages** on every push to `main` that touches `docs/`, `mkdocs.yml`, or `requirements.txt`.

A secondary **Vercel** deployment is also configured for preview builds and pull-request previews.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.9+ |
| MkDocs | 1.6.1 (pinned in `requirements.txt`) |
| mkdocs-material | 9.7.3 (pinned in `requirements.txt`) |

---

## Local Development

```bash
# 1. Clone the repository
git clone https://github.com/oumar-code/Akulearn_docs.git
cd Akulearn_docs

# 2. Install dependencies
pip install -r requirements.txt

# 3. Serve the docs locally with live reload
mkdocs serve
```

Open <http://localhost:8000> in your browser.

> **Tip:** Use `mkdocs build --strict` to treat all warnings as errors before pushing, matching CI behaviour.

---

## GitHub Pages Deployment (primary)

Deployment is fully automated via `.github/workflows/docs-deploy.yml`.

### Trigger

The workflow runs automatically when a push to `main` touches:
- `docs/**`
- `mkdocs.yml`
- `requirements.txt`
- `.github/workflows/docs-deploy.yml`
- `.github/workflows/docs-deploy.yml`

It can also be triggered manually via **Actions → Deploy MkDocs to GitHub Pages → Run workflow**.

### How it works

1. **Build** job: Checks out the repo, installs Python dependencies, runs `mkdocs build`, and uploads the `site/` directory as a GitHub Pages artifact.
2. **Deploy** job: Publishes the artifact to the `github-pages` environment.

### Required repository settings

In **Settings → Pages**, the source must be set to **"GitHub Actions"** (not a branch). This is required for the `actions/deploy-pages` action to work.

### Permissions required

The workflow uses:
- `pages: write` — to publish to GitHub Pages
- `id-token: write` — for OIDC authentication with the Pages service
- `contents: read` — to check out the repository

---

## Vercel Deployment (Next.js Dashboard)

The `akulearn-dashboard/` Next.js app is deployed to Vercel via the `.github/workflows/vercel-deploy.yml` workflow. The root `vercel.json` declares the framework:

```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "installCommand": "npm install"
}
```

All Vercel CLI commands run from the `akulearn-dashboard/` working directory, so the Next.js project and its `package.json` are found automatically.

### Required environment variables

Set the following in the **Vercel project dashboard** (under Settings → Environment Variables). They are downloaded by `vercel pull` during the CI build:

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL (starts with `https://`) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous public key |

### Deployment trigger

The `.github/workflows/vercel-deploy.yml` workflow deploys to Vercel on every push to `main` that touches `akulearn-dashboard/**`, `vercel.json`, or the workflow file itself. It can also be triggered manually via **Actions → Deploy Next.js Dashboard to Vercel → Run workflow**.

### Required secrets

| Secret | Description |
|--------|-------------|
| `VERCEL_TOKEN` | Personal access token from the Vercel dashboard |
| `VERCEL_ORG_ID` | Organisation/team ID from Vercel |
| `VERCEL_PROJECT_ID` | Project ID from the Vercel dashboard |

---

## Network Map & Mapbox Token

The interactive Zamfara network map (`docs/network-map/index.html`) requires a [Mapbox public access token](https://docs.mapbox.com/help/getting-started/access-tokens/) to render tiles. The token placeholder in the file is `MAPBOX_TOKEN_PLACEHOLDER`.

**To activate the map:**

1. Create a free Mapbox account and copy your public access token (starts with `pk.`).
2. In `docs/network-map/index.html`, replace `MAPBOX_TOKEN_PLACEHOLDER` with your token.
3. Do **not** commit your token to source control — consider using a build-time substitution or scoping the token to your deployed domain in the Mapbox dashboard.

The map loads node data from `docs/network-map/data/zamfara-network-data.geojson`. To update the map nodes:

1. Edit `docs/network-map/data/zamfara-network-data.geojson` with the correct GeoJSON `FeatureCollection`.
2. Commit and push — the map updates automatically on the next deploy.

---

## Dependency Pinning

`requirements.txt` pins exact versions of all dependencies to ensure reproducible builds:

```
mkdocs==1.6.1
mkdocs-material==9.7.3
```

To upgrade dependencies:
1. Update the version numbers in `requirements.txt`.
2. Test locally with `mkdocs build --strict`.
3. Open a pull request — GitHub Pages CI will validate the build before merge.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Vercel build fails: `No Next.js version detected` | `vercel build` runs from the wrong directory | Ensure all Vercel CLI steps use `working-directory: akulearn-dashboard` in the workflow |
| Vercel build fails: `supabaseUrl is required` | `NEXT_PUBLIC_SUPABASE_URL` not set in Vercel project env vars | Add `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` to the Vercel project dashboard under Settings → Environment Variables |
| Vercel build fails: `uv: not found` | Old `vercel.json` using `uv` | Use the current `vercel.json` which uses standard `npm` |
| GitHub Pages deploy fails: `Resource not accessible by integration` | Pages source not set to "GitHub Actions" | Go to Settings → Pages and change Source to "GitHub Actions" |
| `mkdocs build` exits non-zero | Missing or broken Markdown file referenced in `nav:` | Run `mkdocs build --strict` locally to see the error |
| Network map shows blank map | GeoJSON data file missing or wrong path | Ensure `docs/network-map/data/zamfara-network-data.geojson` exists |
| MkDocs warns about missing Mapbox token | Token placeholder not replaced | Replace `MAPBOX_TOKEN_PLACEHOLDER` in `docs/network-map/index.html` with your Mapbox public `pk.*` token |
