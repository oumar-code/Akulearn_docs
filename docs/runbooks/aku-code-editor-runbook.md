# Aku Code Editor — Service Runbook

> **Service:** `aku-code-editor`  
> **Host port (dev):** 8013 · **Container port:** 8000  
> **Docker profile:** `editor`  
> **On-call:** Platform Engineering  
> **Last updated:** April 2026

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start (dev) | `docker compose -f docs/deployment/local/docker-compose.dev.yml --profile infra --profile core --profile editor up -d aku-code-editor` |
| Stop (dev) | `docker compose -f docs/deployment/local/docker-compose.dev.yml stop aku-code-editor` |
| Restart (dev) | `docker compose -f docs/deployment/local/docker-compose.dev.yml restart aku-code-editor` |
| Logs (dev) | `docker compose -f docs/deployment/local/docker-compose.dev.yml logs -f aku-code-editor` |
| Health check | `curl http://localhost:8013/health` |
| Readiness check | `curl http://localhost:8013/ready` |
| Metrics | `curl http://localhost:8013/metrics` |
| K8s restart | `kubectl rollout restart deployment/aku-code-editor -n aku-platform` |
| K8s logs | `kubectl logs -f -l app=aku-code-editor -n aku-platform` |

---

## Startup Procedure

1. Ensure `infra` profile is running (Postgres, Redis, Neo4j).
2. Ensure `core` profile is running (AkuAI, Akudemy) — Code Editor calls both.
3. Start Code Editor: `--profile editor up -d`.
4. Wait for `GET /ready` to return `{"status": "ready", "redis_connected": true}`.
5. Verify Prometheus scrape: `curl http://localhost:9090/targets` (if monitoring profile is running).

### Startup checks performed by the service

- Redis DB 9 connectivity (`PING`)
- AkuAI health check (`GET /health` on `AKU_AI_URL`)
- Akudemy health check (`GET /health` on `AKUDEMY_URL`)
- Postgres `code_editor` schema exists (Alembic `current` check)

If any check fails, `/ready` returns `503` and the service processes no requests until all checks pass.

---

## Shutdown Procedure

```bash
# Graceful shutdown (Docker)
docker compose -f docs/deployment/local/docker-compose.dev.yml stop aku-code-editor

# Graceful shutdown (K8s) — allows in-flight requests to complete (30s timeout)
kubectl delete pod -l app=aku-code-editor -n aku-platform
```

Active streaming sessions will be interrupted. Redis sessions persist (TTL: 7 days) — users can reconnect and continue.

---

## Rollback Procedure

### Docker (dev)

```bash
# Revert to previous image tag
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  pull aku-code-editor  # or edit the image tag in compose file

docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core --profile editor up -d --no-deps aku-code-editor
```

### Kubernetes (staging/prod)

```bash
# Rollback to previous deployment revision
kubectl rollout undo deployment/aku-code-editor -n aku-platform

# Verify rollback
kubectl rollout status deployment/aku-code-editor -n aku-platform

# Check which image is running
kubectl get deployment aku-code-editor -n aku-platform \
  -o jsonpath='{.spec.template.spec.containers[0].image}'
```

---

## Common Failure Modes

### 1. `GET /ready` returns `503` — Redis not connected

**Symptom:** `{"status": "not_ready", "redis_connected": false}`  
**Cause:** Redis is not running or `REDIS_URL` is misconfigured.

```bash
# Check Redis health
docker compose -f docs/deployment/local/docker-compose.dev.yml exec redis redis-cli ping
# Expected: PONG

# Check env var
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  exec aku-code-editor env | grep REDIS_URL
```

**Fix:** Start Redis (`--profile infra`), or correct `REDIS_URL` and restart the service.

---

### 2. `POST /api/v1/code/complete` returns `503` — AkuAI not ready

**Symptom:** `{"error": "Service unavailable", "code": "MODEL_NOT_READY"}`  
**Cause:** AkuAI is not running or not yet ready.

```bash
curl http://localhost:8004/health
curl http://localhost:8004/ready
```

**Fix:** Start AkuAI (`--profile core`). Wait for its `/ready` endpoint to return `200` before calling Code Editor.

---

### 3. `429 Token budget exceeded` for a user

**Symptom:** Users report all requests returning `429`.  
**Cause:** `CODE_EDITOR_TOKEN_BUDGET` daily limit reached.

```bash
# Check current budget for a user (replace <user_id_hash> with actual hash)
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  exec redis redis-cli -n 9 GET "code_editor:token_budget:<user_id_hash>"

# Manually reset budget (emergency only — document reason)
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  exec redis redis-cli -n 9 DEL "code_editor:token_budget:<user_id_hash>"
```

**Prevention:** Increase `CODE_EDITOR_TOKEN_BUDGET` for the institution in the admin policy API, or alert when > 80% of budget is consumed.

---

### 4. High latency on `/api/v1/code/generate`

**Symptom:** p95 latency > 4 000 ms.  
**Cause:** AkuAI inference is slow (large model load, cold start, or resource contention).

```bash
# Check AkuAI metrics
curl http://localhost:8004/metrics | grep inference_duration

# Check Code Editor latency breakdown
curl http://localhost:8013/metrics | grep request_duration
```

**Fix:** 
- In dev: ensure only `--profile core` is running (not `full`) to free up memory for AkuAI.
- In production: check AkuAI pod CPU/memory usage; scale if needed.
- If using edge model: verify `CODE_MODEL_PATH` is set; local inference is faster for this service.

---

### 5. Correction pairs not exported to DaaS

**Symptom:** `code_editor_correction_pairs_queued` metric is growing; DaaS has no new correction datasets.

```bash
# Check Redis queue depth
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  exec redis redis-cli -n 9 LLEN "code_editor:correction_queue:$(date +%Y-%m-%d)"

# Check DaaS health
curl http://localhost:8012/health

# Manually trigger export (if background job is stuck)
curl -X POST http://localhost:8013/internal/export-corrections
```

**Fix:** Restart the background export job (restart the service). Verify `AKU_DAAS_URL` is set and DaaS is healthy.

---

## Escalation

| Severity | Condition | Action |
|----------|-----------|--------|
| P1 | Service down (all requests failing) | Page on-call; rollback if last deploy < 1h ago |
| P2 | Latency p95 > 4 s for 5+ minutes | Check AkuAI; scale if needed |
| P3 | Acceptance rate < 30% for 24h | Check model version; review recent fine-tune |
| P4 | Correction export backlog > 1 000 pairs | Investigate DaaS; restart export job |

---

## Related Runbooks

- [`on-call-playbook.md`](./on-call-playbook.md) — Full incident lifecycle
- [`developer-onboarding.md`](./developer-onboarding.md) — Local setup guide
- [`akuai-runbook.md`](./akuai-runbook.md) — AkuAI (inference dependency)
