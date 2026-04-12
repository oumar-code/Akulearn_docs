# Decision Report: Aku Platform — 6 GB Developer RAM Allocation

**Date:** 2026-04-11
**Scope:** All 9 Aku Platform backend services (AkuAI, Akudemy, Aku-EdgeHub, Aku-IGHub, Aku-SuperHub, AkuTutor, AkuWorkspace, Aku-Telhone, Aku-DaaS)

---

## Problem

A developer with only 6 GB of total system RAM cannot run all 9 services plus their supporting infrastructure (PostgreSQL, Redis, Neo4j) simultaneously. Without explicit `mem_limit` settings, Docker has no cap on container memory and services will compete until the host starts swapping, causing crashes or severe slowdowns.

---

## Decision: Tiered Docker Compose Profiles + Explicit Memory Limits

Rather than one flat `docker-compose.yml` that tries to boot everything, services are grouped into three **profiles** based on how often a developer needs them running at the same time.

### Profile Definitions

| Profile | Purpose | When to use |
|---|---|---|
| `infra` | Shared backbone (Postgres, Redis, Neo4j) | Always — every profile depends on it |
| `core` | The 4 highest-priority services (AkuAI, Akudemy, Aku-EdgeHub, AkuTutor) | Daily development |
| `full` | Remaining 5 services | Integration testing only |

### Memory Budget

| Layer | Allocation |
|---|---|
| Host OS | 1,000 MB (reserved, not touchable) |
| Docker daemon overhead | ~512 MB |
| **Available for containers** | **~4,500 MB** |

### Per-Container Limits

| Container | Profile | `mem_limit` | Key tuning |
|---|---|---|---|
| postgres | infra | 256 MB | shared DB for all services |
| redis | infra | 128 MB | sessions + cache |
| neo4j | infra | 512 MB | `NEO4J_dbms_memory_heap_maxSize=256m`, `pagecache=128m` |
| akuai | core | 512 MB | no model weights loaded in dev |
| akudemy | core | 256 MB | |
| aku-edgehub | core | 256 MB | SQLite mode fine for dev |
| akututor | core | 256 MB | |
| aku-ighub | full | 128 MB | |
| aku-superhub | full | 128 MB | |
| akuworkspace | full | 128 MB | |
| aku-telhone | full | 128 MB | |
| aku-daas | full | 128 MB | |

### Scenario Totals

| Scenario | Command | RAM Used | Headroom |
|---|---|---|---|
| Infra only | `--profile infra` | ~896 MB | ~3.6 GB |
| Core dev | `--profile infra --profile core` | ~2.4 GB | ~2.1 GB |
| Full stack | `--profile infra --profile core --profile full` | ~3.0 GB | ~1.5 GB |

All three scenarios fit within the 4,500 MB container budget.

---

## Key Engineering Decisions

1. **Neo4j tuning is mandatory.** By default Neo4j allocates 1–2 GB of heap. Without `NEO4J_dbms_memory_heap_maxSize=256m`, the entire budget collapses. This is the single most important change.

2. **Profiles over separate compose files.** Using Docker Compose `profiles:` keeps one canonical file and avoids environment drift between multiple override files.

3. **No nginx in dev.** Developers hit services directly on host-mapped ports. Saves 64 MB and removes a dependency layer.

4. **Docker Desktop RAM cap (Windows/Mac).** The host Docker VM must be capped at 5 GB in Docker Desktop → Settings → Resources. Without this, Docker Desktop's Linux VM will claim all 6 GB from the host OS.

5. **Linux hosts need no VM change.** Docker on Linux uses cgroups directly, so `mem_limit` in compose is the only required control.

6. **`mem_limit` without `mem_reservation`.** Setting only a hard ceiling (not a soft reservation) allows containers to burst within their limit without pre-allocating, which is correct for a dev environment where most services are idle.

---

## What This Does NOT Cover

- Production Kubernetes sizing — handled by `docs/deployment/k8s/` manifests with `resources.requests/limits` per pod.
- CI/CD resource allocation — handled by GitHub-hosted runners, not local Docker.
- The akulearn-linux-app KMP Desktop app — runs natively as a `.kexe` binary, outside Docker.

---

## Next Step

Commit the finalized `docker-compose.dev.yml` with profiles and `mem_limit` values into `docs/deployment/local/` so every developer picks it up automatically. See [`docker-compose.dev.yml`](./docker-compose.dev.yml) (to be added).
