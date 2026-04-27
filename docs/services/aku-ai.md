# AkuAI

> **Status:** Phase 1 Stub → Phase 2 Real Inference  
> **Host port (dev):** 8004 · **Container port:** 8000  
> **Docker profile:** `core`  
> **Redis DB:** 2 (inference response cache, rate-limit counters)  
> **Postgres schema:** `akuai` (see [`deployment/local/postgres-schemas.md`](../deployment/local/postgres-schemas.md))  
> **Related:** [`api/akuai-openapi.yaml`](../api/akuai-openapi.yaml) · [`runbooks/akuai-runbook.md`](../runbooks/akuai-runbook.md)

---

## Vision

AkuAI is the **shared AI/ML inference engine** for the Aku Platform. All other services delegate model inference to AkuAI — no other service runs a model of its own in cloud mode. AkuAI exposes a unified HTTP API covering:

- **Embeddings** — 384-dimensional semantic vectors (all-MiniLM-L6-v2)
- **Text generation** — curriculum-grounded prose (Gemma-2B-Q4 GGUF)
- **Code inference** — code completion, generation, and explanation (CodeGemma-2B-Q4)

In offline/edge mode the Aku-EdgeHub runs its own FAISS index for retrieval but still calls AkuAI for generation when connectivity is available.

---

## Architecture

```
Clients (AkuTutor, Aku Code Editor, AkuWorkspace, Aku-EdgeHub)
        │
        ▼
  AkuAI (port 8004)
        │
        ├── Redis DB 2 ──── Inference response cache (5-min TTL), rate-limit counters
        │
        ├── Postgres (akuai schema) ── inference_log, model_registry
        │
        ├── all-MiniLM-L6-v2 (ONNX) ── embedding model  [MODEL_DIR]
        ├── gemma-2b-q4.gguf         ── text generation  [GEMMA_GGUF_PATH]
        └── codegemma-2b-q4.gguf     ── code inference   [CODE_MODEL_PATH]  (Phase 4)
```

In Phase 1, `MODEL_DIR`, `GEMMA_GGUF_PATH`, and `CODE_MODEL_PATH` are all empty in dev. All endpoints return **deterministic stub responses**.

---

## API Endpoints

See full OpenAPI spec: [`docs/api/akuai-openapi.yaml`](../api/akuai-openapi.yaml).

### Phase 1 — Stub Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/embeddings` | Embed text → 384-dim vector (stub: zero-vector) |
| `POST` | `/api/v1/text/generate` | Generate prose from prompt (stub: canned response) |
| `POST` | `/api/v1/code/generate` | Generate code from prompt (stub → Phase 2 real) |
| `POST` | `/api/v1/code/explain` | Explain code block (stub → Phase 2 real) |
| `GET` | `/health` | Liveness check |
| `GET` | `/ready` | Readiness — model loaded and DB connected |
| `GET` | `/metrics` | Prometheus metrics |

### Phase 2 — Additional Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/code/complete` | Tab-completion (delegates from Aku Code Editor) |
| `POST` | `/api/v1/code/review` | Static code review: style/bugs/security/performance |

---

## Data Models

### `EmbeddingRequest`

```json
{
  "text": "Explain the properties and behaviour of waves",
  "model": "all-MiniLM-L6-v2"
}
```

### `EmbeddingResponse`

```json
{
  "embedding": [0.021, -0.044, 0.103, "..."],  // 384-dim float32
  "model": "all-MiniLM-L6-v2",
  "stub": true
}
```

> `stub: true` is present in Phase 1 responses when real model weights are not loaded. Clients MUST handle the stub flag gracefully (zero-vector is valid for dev; do not store stub embeddings in FAISS).

### `TextGenerationRequest`

```json
{
  "prompt": "Explain how sound waves travel.",
  "system_prompt": "You are a helpful Akulearn tutor for secondary school students.",
  "max_tokens": 256,
  "temperature": 0.7,
  "trace_id": "t_uuid_001"
}
```

### `TextGenerationResponse`

```json
{
  "text": "Sound waves are longitudinal waves that travel through a medium...",
  "model": "gemma-2b-q4",
  "tokens_generated": 48,
  "latency_ms": 320,
  "stub": false
}
```

### `CodeGenerationRequest`

```json
{
  "prompt": "Write a Python function to simulate projectile motion",
  "language": "python",
  "subject_context": "Physics",
  "lo_descriptions": ["Calculate range, maximum height and time of flight"],
  "max_tokens": 256,
  "session_id": "s_uuid_001"
}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development` / `staging` / `production` |
| `LOG_LEVEL` | `info` | `debug` / `info` / `warning` / `error` |
| `DATABASE_URL` | — | PostgreSQL connection string (schema: `akuai`) |
| `REDIS_URL` | `redis://redis:6379/2` | Redis DB 2 connection string |
| `MODEL_DIR` | `""` | Path to ONNX embedding model directory; empty = zero-vector stub |
| `GEMMA_GGUF_PATH` | `""` | Path to Gemma GGUF file; empty = canned stub response |
| `CODE_MODEL_PATH` | `""` | Path to CodeGemma GGUF file; empty = stub (Phase 4) |
| `GEMMA_MAX_PAYLOAD_BYTES` | `4096` | Max request body bytes for text generation (→ 429 if exceeded) |
| `AKUAI_API_SECRET` | — | Shared secret for service-to-service authentication |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed CORS origins |
| `CODE_CANARY_PERCENT` | `0` | Percentage of code requests routed to canary model version (Phase 4) |

---

## Phase 1 — Stub Response Specification

All Phase 1 stub responses are **deterministic** — identical input produces identical output. This allows downstream services to write reliable unit tests without loading real model weights.

| Endpoint | Stub behaviour |
|----------|---------------|
| `POST /api/v1/embeddings` | Returns 384-element zero-vector `[0.0, ..., 0.0]`; `stub: true` |
| `POST /api/v1/text/generate` | Returns fixed string: `"[STUB] This is a placeholder response from AkuAI."`; `stub: true` |
| `POST /api/v1/code/generate` | Returns fixed Python snippet; `stub: true` |
| `POST /api/v1/code/explain` | Returns `"[STUB] This code performs the described operation."`; `stub: true` |
| `GET /health` | `{"status": "ok"}` |
| `GET /ready` | `{"status": "ok", "model_loaded": false, "db_connected": true}` |

---

## Phase 2 — Real Inference

### Embedding Model (`all-MiniLM-L6-v2`)

When `MODEL_DIR` is set to a directory containing the ONNX model:

1. Load `all-MiniLM-L6-v2.onnx` on service startup (lifespan event).
2. Run ONNX inference synchronously via `onnxruntime.InferenceSession`.
3. Return 384-dim `float32` vector; `stub: false`.
4. Cache response in Redis DB 2 for 5 minutes: key = `akuai:inference_cache:emb:<sha256(text)>`.

### Text Generation (`gemma-2b-q4.gguf`)

When `GEMMA_GGUF_PATH` is set:

1. Load GGUF via `llama_cpp.Llama` on startup.
2. Cap payload via `GEMMA_MAX_PAYLOAD_BYTES` gate (→ `429` on overload).
3. Run inference; stream tokens to caller via SSE or return full response.
4. Log to `akuai.inference_log` (input/output hashed, never raw text).

### Rate Limiting

```
akuai:rate_limit:<user_or_service_id>  →  integer (requests in current 60s window)
TTL: 60 s (sliding window)
```

Returns `HTTP 429` with `Retry-After: 60` header when limit exceeded.

---

## Observability

### Prometheus Metrics (at `/metrics`)

| Metric | Type | Description |
|--------|------|-------------|
| `akuai_embedding_requests_total` | Counter | Total embedding requests |
| `akuai_text_generation_requests_total` | Counter | Total text generation requests |
| `akuai_code_requests_total` | Counter | Total code inference requests by endpoint |
| `akuai_request_duration_seconds` | Histogram | Latency by endpoint (p50/p95/p99) |
| `akuai_model_loaded` | Gauge | 1 if model weights loaded; 0 if stub mode |
| `akuai_cache_hits_total` | Counter | Redis inference cache hits |
| `akuai_tokens_generated_total` | Counter | Total tokens generated (by model) |

### Structured Log Fields

```json
{
  "timestamp": "2026-04-27T20:00:00Z",
  "service": "akuai",
  "level": "info",
  "trace_id": "t_uuid",
  "endpoint": "/api/v1/embeddings",
  "input_hash": "sha256:abc123",
  "model": "all-MiniLM-L6-v2",
  "latency_ms": 14,
  "stub": false,
  "message": "embedding served"
}
```

---

## Deployment

### Dev (Docker Compose)

```bash
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core up -d
```

With real model weights (Phase 2+):

```bash
# Mount local model directory
MODEL_DIR=/path/to/models GEMMA_GGUF_PATH=/path/to/gemma-2b-q4.gguf \
  docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core up -d
```

### Kubernetes

See: [`docs/deployment/k8s/akuai.yaml`](../deployment/k8s/akuai.yaml)

---

## Phase 1 Exit Criteria

- [ ] Service starts healthy in `infra + core` profile on a 6 GB machine
- [ ] `GET /health` returns `200 OK`
- [ ] `GET /ready` returns `200 OK` with `model_loaded: false` in stub mode
- [ ] `POST /api/v1/embeddings` returns 384-dim zero-vector with `stub: true`
- [ ] `POST /api/v1/text/generate` returns deterministic stub response
- [ ] `POST /api/v1/code/generate` returns deterministic stub response
- [ ] Prometheus scrape target active at `akuai:8000/metrics`
- [ ] All log lines emit valid JSON with `trace_id`, `service`, `level`, `timestamp`

## Phase 2 Exit Criteria

- [ ] Real embedding: 384-dim vector returned when `MODEL_DIR` is set
- [ ] GGUF text generation: prose returned when `GEMMA_GGUF_PATH` is set
- [ ] `429` returned when `GEMMA_MAX_PAYLOAD_BYTES` exceeded
- [ ] Inference cache hit rate > 0 in local load test
- [ ] `akuai.inference_log` table populated (no raw text stored)
- [ ] `stub: false` in responses when real model is loaded
