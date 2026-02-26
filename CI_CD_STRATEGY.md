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

### Immediate Actions ✅ ALL DONE
1. ✅ Fix Render Mermaid workflow (Node 20 + sandbox flags)
2. ✅ Fix Demo CI workflow (create runs directory)
3. ✅ Simplify automation workflow
4. ✅ MkDocs deployment paths fixed
5. ✅ Add path filters to key workflows

### Short-term Actions (Recommended for Future)
1. **Add path filters to remaining workflows** ✅ PARTIALLY DONE
   - ✅ docs-deploy.yml - Only on docs/** changes
   - ✅ projector_hub_ci.yml - Only on unconnected_stack/** changes
   - ✅ connected_backend_gcp_deploy.yml - Only on connected_stack/** changes
   - ✅ kotlin_mobile_ci.yml - Only on Kotlin/mobile code changes
   - ✅ fastapi_microservice.yml - Only on microservices/** changes
   - ⏳ Remaining workflows can be optimized as needed
   
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

## Path Filters - IMPLEMENTED ✅

Path filters have been added to key workflows to prevent unnecessary runs:

### Documentation Workflows
```yaml
# docs-deploy.yml
on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - '.github/workflows/docs-deploy.yml'
```

### Backend Workflows
```yaml
# connected_backend_gcp_deploy.yml
on:
  push:
    branches: [ main ]
    paths:
      - 'connected_stack/**'
      - '.github/workflows/connected_backend_gcp_deploy.yml'
```

### Mobile Workflows
```yaml
# kotlin_mobile_ci.yml
on:
  push:
    branches: [ main ]
    paths:
      - 'KOTLIN MULTIPLATFORM/**'
      - 'src/mobile_app/**'
      - '.github/workflows/kotlin_mobile_ci.yml'
```

### Microservices Workflows
```yaml
# fastapi_microservice.yml
on:
  push:
    branches: [ main ]
    paths:
      - 'akulearn_microservices/**'
      - '.github/workflows/fastapi_microservice.yml'
```

### IoT/Hardware Workflows
```yaml
# projector_hub_ci.yml
on:
  push:
    branches: [ main ]
    paths:
      - 'unconnected_stack/**'
      - '.github/workflows/projector_hub_ci.yml'
```

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
**Status**: ✅ Major improvements completed - workflows optimized and documented  
**Next Steps**: Monitor workflow runs and add filters to remaining workflows as needed
