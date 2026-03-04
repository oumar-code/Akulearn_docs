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

## Vercel Deployment (secondary / preview)

Vercel is configured via `vercel.json` at the repository root:

```json
{
  "framework": null,
  "buildCommand": "python3 -m mkdocs build",
  "outputDirectory": "site",
  "installCommand": "pip install -r requirements.txt"
}
```

Vercel uses standard `pip` to install dependencies and then runs `mkdocs build`. The generated `site/` directory is served as the output.

### Excluded files

`.vercelignore` excludes source code, scripts, and data files that are not needed to build the docs, keeping build times fast.

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
| Vercel build fails: `pip: command not found` | Wrong Python version selected | Set Python version in Vercel project settings |
| Vercel build fails: `uv: not found` | Old `vercel.json` using `uv` | Ensure `installCommand` is `pip install -r requirements.txt` |
| GitHub Pages deploy fails: `Resource not accessible by integration` | Pages source not set to "GitHub Actions" | Go to Settings → Pages and change Source to "GitHub Actions" |
| `mkdocs build` exits non-zero | Missing or broken Markdown file referenced in `nav:` | Run `mkdocs build --strict` locally to see the error |
| Network map shows blank map | GeoJSON data file missing or wrong path | Ensure `docs/network-map/data/zamfara-network-data.geojson` exists |
| MkDocs warns about missing Mapbox token | Token placeholder not replaced | Replace `MAPBOX_TOKEN_PLACEHOLDER` in `docs/network-map/index.html` with your Mapbox public `pk.*` token |
