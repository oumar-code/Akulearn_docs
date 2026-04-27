# Redis Key-Space Ownership & TTL Policy

> **Last updated:** April 2026  
> **Applies to:** All Aku Platform services using the shared Redis 7 instance.

---

## DB Index Ownership

Each service exclusively owns its Redis database index. Never write keys into another service's DB.

| DB Index | Owner Service | Purpose | `maxmemory-policy` concern |
|----------|--------------|---------|---------------------------|
| 0 | *(reserved)* | Shared infrastructure / platform-level keys | — |
| 1 | *(reserved)* | *(available for future use)* | — |
| 2 | **AkuAI** | Inference response cache, rate-limit counters | `allkeys-lru` safe — caches are regenerable |
| 3 | **Akudemy** | Content-sync cache, LO catalog TTL | `allkeys-lru` safe — cache of DB data |
| 4 | **Aku-EdgeHub** | Pending sync events queue, connectivity state | ⚠ Session-critical — see note below |
| 5 | **Aku-IGHub** | Idempotency key store (24 h TTL) | ⚠ Session-critical — see note below |
| 6 | **Aku-SuperHub** | JWT session tokens, service registry heartbeats | ⚠ Session-critical — see note below |
| 7 | **AkuWorkspace** | Per-user conversation context (contextual memory) | `allkeys-lru` acceptable — context is resumable |
| 8 | **Aku-DaaS** | Pipeline status pub/sub, distributed locks | ⚠ Lock keys must not be evicted |
| 9 | **Aku-Code-Editor** | `CodeSession` objects (7-day TTL), streaming buffers | `allkeys-lru` acceptable — sessions have explicit TTL |
| 10 | **Aku-Telhone** | eSIM provisioning state cache | ⚠ Session-critical — see note below |

> **Note: DB 0 is not used by application services.** It is reserved for platform-level infrastructure tooling (e.g., Redis Sentinel coordination, health-check scripts).

---

## TTL Policy by Key Category

| Category | Default TTL | Notes |
|----------|------------|-------|
| Inference response cache (AkuAI) | 5 minutes | Keyed by `sha256(model + prompt)` |
| LO catalog cache (Akudemy) | `REDIS_SYNC_TTL_SECONDS` (default: 30 s) | Short TTL; refreshed on sync |
| Idempotency keys (IGHub) | `IDEMPOTENCY_TTL_SECONDS` (default: 86 400 s = 24 h) | Must survive full request retry window |
| JWT session tokens (SuperHub) | Token `exp` claim + 60 s buffer | Eviction before expiry = forced re-login |
| CodeSession (Code Editor) | 7 days | Configurable via `CODE_SESSION_TTL_SECONDS` |
| Pipeline lock keys (DaaS) | `PIPELINE_STATUS_TTL_SECONDS` (default: 604 800 s = 7 days) | Must not be evicted mid-pipeline |
| Rate-limit counters (AkuAI) | 60 s sliding window | Safe to evict — worst case: rate limit resets early |
| Streaming token buffers (Code Editor) | 30 s from last write | Auto-cleaned by TTL |

---

## `maxmemory-policy` Risk Analysis

The shared Redis instance is configured with:

```
maxmemory 96mb
maxmemory-policy allkeys-lru
```

`allkeys-lru` evicts **any** key (regardless of TTL) when memory pressure is reached. This is a risk for session-critical keys.

### Mitigations

1. **Explicit TTLs on all keys.** Every key written by any service MUST have a TTL set via `EXPIRE` or `SET ... EX`. Keys without TTLs accumulate indefinitely and are the primary cause of memory pressure.

2. **Monitor memory usage.** Add a Prometheus alert when `redis_memory_used_bytes / redis_memory_max_bytes > 0.80`.

3. **Production upgrade path.** In production, move to Redis Cluster with dedicated instances per service group (or per DB index mapped to separate Redis instances). This eliminates cross-service eviction risk entirely.

4. **Critical-key monitor.** For JWT tokens (DB 6) and idempotency keys (DB 5), implement a key-existence check before serving cached data; fall back to the authoritative source (Postgres) on cache miss.

5. **Dev environment.** Dev Redis is capped at 96 MB (`maxmemory 96mb` in compose). With only a few developers and no real model weights, eviction pressure is unlikely. This policy is primarily a production concern.

---

## Key Naming Convention

All keys must follow the format:

```
<service>:<entity_type>:<identifier>[:<sub-key>]
```

**Examples:**

| Key | Owner | TTL |
|-----|-------|-----|
| `akuai:inference_cache:sha256:abc123` | AkuAI | 300 s |
| `akudemy:lo_catalog:version` | Akudemy | 30 s |
| `ighub:idempotency:sha256:xyz789` | IGHub | 86 400 s |
| `superhub:jwt_session:user_id:u001` | SuperHub | token `exp` + 60 s |
| `code_editor:session:s_uuid_001` | Code Editor | 604 800 s |
| `daas:pipeline_lock:job_id:j001` | DaaS | 604 800 s |

---

## Related Documents

- [`docker-compose.dev.yml`](./docker-compose.dev.yml) — Redis container configuration
- [`docs/deployment/k8s/secrets.yaml`](../deployment/k8s/secrets.yaml) — production Redis URL per service
- [`AIOPS_STRATEGY.md`](../AIOPS_STRATEGY.md) — observability and alerting
