# Aku Workspace (PWA Shell)

This folder contains a lightweight Progressive Web App (PWA) shell for Aku Workspace designed with a mobile-first, responsive approach. It intentionally keeps dependencies minimal so you can pick your preferred toolchain (Vite/CRA) to boot the app.

Getting started (recommended: Vite)

1. Install Node.js (16+)
2. From `web/` run:

```bash
npm init vite@latest . -- --template react
npm install
# Copy the `src/` and `public/` contents from this repo into the new app if not already populated.
npm run dev
```

Notes & decisions

- Mobile-first styles are in `src/styles.css`. The layout uses CSS Grid/Flexbox and is responsive by default.
- A simple service worker and `manifest.json` are provided under `public/` to enable PWA capabilities. For production use, replace with Workbox or Vite PWA plugin.
- The repo already includes `src/components/ZamfaraNetworkMap.js` which uses Mapbox GL; set `REACT_APP_MAPBOX_ACCESS_TOKEN` when running locally.
- For a production-ready Workspace, add:
  - Tailwind CSS or design-system tokens
  - Accessibility audits and keyboard navigation
  - Code-splitting and lazy-loading for heavy components
  - Proper OAuth/OIDC integration for auth and session management

What's included

- `src/App.jsx` - Mobile-first app shell and layout
- `src/index.jsx` - App entry and service worker registration
- `src/styles.css` - Mobile-first responsive styles
- `public/manifest.json` - Web app manifest
- `public/service-worker.js` - Simple caching service worker (demo)

Next steps

- Integrate the Workspace UI with the IG-Hub and DaaS APIs (examples exist in `infra/examples`)
- Add PWA build plugin (Vite PWA) and offline caching strategies
- Implement accessibility improvements, unit/integration tests, and CI linting
