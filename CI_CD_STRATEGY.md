# CI/CD Workflow Strategy & Fixes

## Overview

This document outlines the strategy for fixing and maintaining GitHub Actions workflows in the Akulearn_docs repository.

## Analysis of Failed Workflows

### Current Status (February 2026)

Analysis of 1343 workflow runs shows:
- **13 failures** across various workflows
- **13 action_required** statuses
- **3 successes**

### Root Causes Identified

#### 1. **Render Mermaid Diagrams** - FIXED ✅
**Problem**: Puppeteer sandbox issues with Node 18 in GitHub Actions
**Error**: `Failed to launch the browser process! No usable sandbox!`
**Solution**: 
- Upgraded Node.js from 18 to 20
- Added `--no-sandbox` and `--disable-setuid-sandbox` flags to mmdc commands
**Files Changed**: `.github/workflows/render-mermaid.yml`

#### 2. **Demo Visualization CI** - FIXED ✅
**Problem**: Missing `runs/` directory for output files
**Solution**: Added step to create `runs/` directory before running scripts
**Files Changed**: `.github/workflows/demo-ci.yml`

#### 3. **Deploy MkDocs to GitHub Pages** - FIXED ✅
**Problem**: Incorrect navigation paths in mkdocs.yml (paths had `docs/` prefix)
**Solution**: Fixed in previous commit - removed `docs/` prefix from navigation paths
**Files Changed**: `mkdocs.yml` (already fixed)

#### 4. **Akulearn Automation** - IMPROVED ✅
**Problem**: Placeholder workflow with only echo commands that don't do anything useful
**Solution**: 
- Simplified to a health check
- Added `workflow_dispatch` for manual testing
**Files Changed**: `.github/workflows/automation.yml`

## Workflow Categories

### 1. Documentation Workflows (Active & Relevant)
- ✅ `docs-deploy.yml` - Deploy MkDocs to GitHub Pages
- ✅ `render-mermaid.yml` - Render Mermaid diagrams
- ⚠️ `automation.yml` - Nightly automation (placeholder)

### 2. Application Workflows (May need path filters)
- `demo-ci.yml` - Demo visualization CI
- `fullstack_ci_cd.yml` - Fullstack CI/CD
- `akulearn_fullstack_ci_cd.yml` - Akulearn Fullstack CI/CD
- `connected_backend_gcp_deploy.yml` - Backend GCP deployment
- `fastapi_microservice.yml` - FastAPI microservice CI/CD
- `projector_hub_ci.yml` - Projector Hub CI/CD
- `projector_hub_gcp_deploy.yml` - Projector Hub GCP deployment
- `projector_hub_ota.yml` - Projector Hub OTA updates
- `kotlin_mobile_ci.yml` - Kotlin mobile CI/CD

### 3. Testing Workflows
- `ci-data-sanitizer.yml` - Data sanitizer tests
- `ci-ig-hub.yml` - IG Hub tests
- `ci-e2e-ig-hub.yml` - IG Hub end-to-end tests
- `hardware-pr-gate.yml` - Hardware PR gate

## Recommendations

### Immediate Actions ✅ DONE
1. ✅ Fix Render Mermaid workflow (Node 20 + sandbox flags)
2. ✅ Fix Demo CI workflow (create runs directory)
3. ✅ Simplify automation workflow
4. ✅ MkDocs deployment paths fixed

### Short-term Actions (Recommended)
1. **Add path filters** to workflows so they only run when relevant files change
   - Example: docs workflows should only run on `docs/**` or `mkdocs.yml` changes
   - Application workflows should only run on their specific directories
   
2. **Consolidate duplicate workflows**
   - `fullstack_ci_cd.yml` and `akulearn_fullstack_ci_cd.yml` appear to be duplicates
   
3. **Add workflow documentation**
   - Document what each workflow does
   - Document when it should run
   - Document required secrets/variables

### Long-term Strategy
1. **Implement a monorepo strategy** if this repo contains multiple applications
2. **Use workflow matrices** for testing across multiple environments
3. **Add caching** to speed up workflows (pip cache, npm cache, etc.)
4. **Implement proper environment segregation** (dev, staging, prod)
5. **Add workflow status badges** to README.md

## Path Filters Example

For documentation workflows:
```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - '.github/workflows/docs-deploy.yml'
```

For backend workflows:
```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'connected_stack/**'
      - 'requirements.txt'
      - '.github/workflows/connected_backend_gcp_deploy.yml'
```

## Monitoring & Maintenance

### Weekly Tasks
- Review failed workflow runs
- Update dependencies in workflows
- Check for deprecated GitHub Actions versions

### Monthly Tasks
- Audit workflow efficiency (runtime, costs)
- Remove unused workflows
- Update documentation

### Quarterly Tasks
- Review entire CI/CD strategy
- Update Node.js, Python, and other runtime versions
- Security audit of workflow permissions

## Key Learnings

1. **Puppeteer in CI**: Always use `--no-sandbox` flags in containerized environments
2. **Node.js versions**: Stay current (Node 20+) to avoid deprecated package issues
3. **Path filters**: Essential for monorepos to avoid unnecessary workflow runs
4. **Explicit directory creation**: Always create output directories before use
5. **MkDocs paths**: Navigation paths are relative to the `docs/` directory

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Puppeteer Troubleshooting](https://pptr.dev/troubleshooting)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Mermaid CLI Documentation](https://github.com/mermaid-js/mermaid-cli)

## Contact

For questions about these workflows, contact the DevOps team or create an issue in the repository.

---

**Last Updated**: February 18, 2026
**Status**: Active improvements in progress
