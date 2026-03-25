# Akudemy Static Site – Deployment Guide

## Overview

This directory contains the Akudemy static site — a JAMB exam preparation landing page built with plain HTML and inline CSS. No build step is required; the files are served directly.

## File Structure

```
public/
├── index.html          Landing page (hero, features, subjects, pricing, testimonials)
├── about.html          About & mission page (team, values, FAQ, contact)
├── blog.html           Blog landing page (6 sample articles + newsletter)
├── pricing.html        Detailed pricing page (plans, comparison table, FAQ)
├── vercel.json         Vercel routing & security-header config for this static site
└── DEPLOYMENT_GUIDE.md This file
```

## Deploy to Vercel (Recommended)

### Step 1 – Push to GitHub

```bash
git add public/
git commit -m "Add Akudemy website"
git push
```

### Step 2 – Import on Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click **"Import Git Repository"** and select `oumar-code/Akulearn_docs`
3. In the **Configure Project** screen set:
   - **Framework Preset:** `Other`
   - **Root Directory:** `public`
   - **Build Command:** *(leave empty)*
   - **Output Directory:** `.` *(current directory)*
4. Click **"Deploy"**

### Step 3 – Set Custom Domain (Optional)

In the Vercel project dashboard:
1. Go to **Settings → Domains**
2. Add `akudemy.ng` (or your preferred domain)
3. Update your DNS records as instructed by Vercel

---

## Root-Level `vercel.json` Update

The root `vercel.json` has been updated to serve the `public/` directory as a static site instead of running the MkDocs build. This means Akudemy will be the deployed output at the repository's Vercel URL.

## Local Preview

No build step is needed. Open any HTML file directly in your browser:

```bash
# macOS
open public/index.html

# Linux
xdg-open public/index.html

# Windows
start public/index.html
```

Or use a simple local server:

```bash
cd public
python3 -m http.server 8080
# then open http://localhost:8080
```

## Pages

| File | URL path | Description |
|---|---|---|
| `index.html` | `/` | Main landing page |
| `about.html` | `/about` | About & mission |
| `blog.html` | `/blog` | Blog articles |
| `pricing.html` | `/pricing` | Pricing plans |

## Security Headers

The `vercel.json` inside `public/` adds the following security headers to all responses:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

## Future Services

The following services are planned for future deployment phases and are **not** part of this initial release:

- **Telhone** – Telecom/VoIP service
- **DaaS** – Device-as-a-Service
- **Akulearn Workspace** – Collaborative learning workspace
