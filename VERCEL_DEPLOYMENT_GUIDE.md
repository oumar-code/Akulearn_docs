# Vercel Deployment Guide – Akulearn Dashboard

## Overview

The Akulearn Dashboard (`akulearn-dashboard/`) is a **Next.js 16** application deployed to Vercel. Deployment is handled automatically via the GitHub Actions workflow at `.github/workflows/vercel-deploy.yml`. The workflow builds the MkDocs documentation, copies it into the Next.js `public/docs/` directory, then deploys the combined bundle to Vercel.

---

## Architecture

```
Akulearn_docs/ (monorepo root)
├── akulearn-dashboard/    ← Next.js 16 app (deployed to Vercel)
│   ├── app/               ← Next.js App Router pages
│   ├── lib/               ← Shared utilities (supabaseClient.ts)
│   ├── public/            ← Static assets
│   │   └── docs/          ← MkDocs output copied here at build time
│   ├── package.json
│   └── vercel.json        ← Vercel CLI config (used by CI)
├── docs/                  ← MkDocs source files
├── mkdocs.yml             ← MkDocs config
├── requirements.txt       ← Python deps for MkDocs
├── vercel.json            ← Root config for Vercel GitHub integration
└── .vercelignore          ← Files excluded from Vercel uploads
```

---

## How Deployment Works

### Trigger

The `vercel-deploy.yml` workflow fires on any push to `main` that touches:
- `akulearn-dashboard/**` – dashboard source
- `docs/**` or `mkdocs.yml` or `requirements.txt` – documentation source
- `vercel.json` or `.vercelignore` – Vercel config
- `.github/workflows/vercel-deploy.yml` – workflow itself

It can also be triggered manually via `workflow_dispatch`.

### Build steps

1. **MkDocs build** – installs Python deps and runs `mkdocs build`, producing `site/`.
2. **Copy docs** – copies `site/` into `akulearn-dashboard/public/docs/` so docs are served as static files under `/docs/`.
3. **Dashboard install** – runs `npm ci` inside `akulearn-dashboard/`.
4. **Vercel CLI deploy** – runs `vercel pull`, `vercel build --prod`, `vercel deploy --prebuilt --prod`.

---

## Configuration Files

### `akulearn-dashboard/vercel.json` (used by CI)

```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "installCommand": "npm ci",
  "rewrites": [
    { "source": "/docs",         "destination": "/docs/index.html" },
    { "source": "/docs/",        "destination": "/docs/index.html" },
    { "source": "/docs/:path+/", "destination": "/docs/:path+/index.html" },
    { "source": "/docs/:path+",  "destination": "/docs/:path+/index.html" }
  ]
}
```

### `vercel.json` (root – Vercel GitHub integration fallback)

```json
{
  "framework": "nextjs",
  "buildCommand": "cd akulearn-dashboard && npm run build",
  "installCommand": "npm install --include=dev && cd akulearn-dashboard && npm ci",
  "outputDirectory": "akulearn-dashboard/.next",
  "rewrites": [ ... ]
}
```

The root `vercel.json` targets the `akulearn-dashboard/` subdirectory so that Vercel's GitHub integration does not mis-detect this monorepo as a Python/FastAPI project.

---

## Required Secrets

Set the following in **GitHub → Settings → Secrets and variables → Actions**:

| Secret | Description |
|--------|-------------|
| `VERCEL_TOKEN` | Vercel personal access token |
| `VERCEL_ORG_ID` | Vercel org/team ID (from `.vercel/project.json` locally) |
| `VERCEL_PROJECT_ID` | Vercel project ID (from `.vercel/project.json` locally) |

Set the following in **Vercel → Project → Settings → Environment Variables** (Production):

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon (public) key |

> **Note:** The `NEXT_PUBLIC_` prefix is required for browser-side access. These are safe to expose; never commit your `service_role` key.

---

## Local Development

```bash
cd akulearn-dashboard
npm install
npm run dev        # http://localhost:3000

# Build and preview locally
npm run build
npm start
```

---

## Deploy via Vercel CLI (manual)

```bash
npm install -g vercel

# Link to the project the first time
cd akulearn-dashboard
vercel link

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| "No Next.js version detected" | Vercel GitHub integration can't find Next.js in the root | Root `package.json` `devDependencies` must include `next` at the same version as the dashboard |
| "Canceled by Ignored Build Step" | Root `vercel.json` includes an `ignoreCommand` that exits `0` | Remove `ignoreCommand` (or make it return non-zero) so builds run |
| Supabase client throws at runtime | `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY` not set | Add both variables in Vercel project environment settings |
| `/docs/` returns 404 | MkDocs output wasn't copied to `public/docs/` | Re-run the CI workflow; check the "Copy MkDocs output" step |
| Double deployments | Both GitHub integration and CI workflow deploy simultaneously | If using CI workflow as primary, disable the Vercel GitHub integration in the Vercel project settings |

---

**Last Updated**: 2026-04
**Main Branch**: All production deployments go to `main`.
