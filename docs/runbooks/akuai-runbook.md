# AkuAI — Service Runbook

> **Service:** `akuai`  
> **Host port (dev):** 8004 · **Container port:** 8000  
> **Docker profile:** `core`  
> **Last updated:** April 2026

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start (dev) | `docker compose -f docs/deployment/local/docker-compose.dev.yml --profile infra --profile core up -d akuai` |
| Restart (dev) | `docker compose restart akuai` |
| Logs | `docker compose logs -f akuai` |
| Health | `curl http://localhost:8004/health` |
| Readiness | `curl http://localhost:8004/ready` |
| Metrics | `curl http://localhost:8004/metrics` |
| K8s restart | `kubectl rollout restart deployment/akuai -n aku-platform` |

---

## Startup Checks

AkuAI performs these checks on start:
- Postgres connectivity (`akuai` schema reachable)
- Redis DB 2 connectivity
- If `MODEL_DIR` is set: verify embedding model file exists
- If `GEMMA_GGUF_PATH` is set: verify GGUF file exists + SHA-256 matches registry
- If `CODE_MODEL_PATH` is set (Phase 4+): verify code GGUF file + register in `model_registry`

`/ready` returns `200` only when all configured models are loaded.

---

## Common Failure Modes

### 1. `GET /ready` returns `503` — model loading

In dev, `MODEL_DIR` and `GEMMA_GGUF_PATH` are empty by default, so no models are loaded and stub responses are returned. `/ready` should still return `200` in stub mode.

If `/ready` returns `503` in stub mode:
```bash
docker compose logs akuai | tail -50
# Look for connection errors to Postgres or Redis
```

### 2. High inference latency

```bash
# Check resource usage
docker stats akuai
# If CPU > 80% or memory near mem_limit (512 MB in dev), reduce concurrent requests
```

### 3. `429` returned to callers

AkuAI enforces `GEMMA_MAX_PAYLOAD_BYTES`. If callers are sending large payloads:
```bash
# Check current limit
docker compose exec akuai env | grep GEMMA_MAX_PAYLOAD_BYTES
# Default: 4096 bytes
```

---

## Rollback

```bash
# K8s
kubectl rollout undo deployment/akuai -n aku-platform
kubectl rollout status deployment/akuai -n aku-platform
```

---

## Key Environment Variables

| Variable | Dev default | Description |
|----------|------------|-------------|
| `MODEL_DIR` | `""` | Path to ONNX embedding model directory |
| `GEMMA_GGUF_PATH` | `""` | Path to Gemma GGUF file |
| `CODE_MODEL_PATH` | `""` | Path to code GGUF file (Phase 4) |
| `GEMMA_MAX_PAYLOAD_BYTES` | `4096` | Max payload size per request |
| `AKUAI_API_SECRET` | `dev_secret_change_in_production` | Service-to-service auth secret |

---

## Dependencies

- **Upstream:** Postgres (schema `akuai`), Redis DB 2
- **Called by:** AkuTutor, Aku-Code-Editor, AkuWorkspace, Aku-EdgeHub

AkuAI does not call any other Aku service.
