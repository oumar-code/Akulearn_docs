# Aku Code Editor — Engineering Handbook

> **Version:** 0.1  
> **Last updated:** April 2026  
> **Audience:** Backend Engineers, AI/ML Engineers, DevOps  
> **Related:** [`services/aku-code-editor.md`](../services/aku-code-editor.md) · [`api/aku-code-editor-openapi.yaml`](../api/aku-code-editor-openapi.yaml) · [`adrs/adr-005-aku-code-editor.md`](../adrs/adr-005-aku-code-editor.md) · [`runbooks/aku-code-editor-runbook.md`](../runbooks/aku-code-editor-runbook.md)

---

## 1. Overview

Aku Code Editor (`aku-code-editor`) is a FastAPI microservice that provides AI-powered code assistance scoped to the Akulearn curriculum. It runs on port 8013 in dev (container port 8000) and communicates with AkuAI, Akudemy, and Aku-DaaS for inference, curriculum context, and fine-tuning data export respectively.

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Framework | FastAPI + Uvicorn |
| Async | asyncio + httpx (service calls) |
| Session store | Redis (aioredis) |
| Streaming | FastAPI StreamingResponse (SSE) + WebSocket |
| Inference (cloud) | AkuAI HTTP client |
| Inference (edge) | llama-cpp-python (GGUF) |
| FAISS index | faiss-cpu (debug-examples index) |
| Logging | structlog (JSON output) |
| Metrics | prometheus-fastapi-instrumentator |
| Testing | pytest + pytest-asyncio + httpx.AsyncClient |

---

## 2. Repository Structure

```
aku-code-editor/
├── app/
│   ├── main.py               ← FastAPI app factory, lifespan events
│   ├── api/
│   │   ├── v1/
│   │   │   ├── code.py       ← /api/v1/code/* endpoints
│   │   │   └── sessions.py   ← /api/v1/code/sessions/* endpoints
│   │   └── ws/
│   │       └── stream.py     ← /ws/code/stream WebSocket endpoint
│   ├── core/
│   │   ├── config.py         ← Settings (pydantic-settings)
│   │   ├── logging.py        ← structlog JSON logger setup
│   │   └── metrics.py        ← Prometheus counter/histogram registration
│   ├── models/
│   │   ├── code_session.py   ← CodeSession Pydantic model
│   │   ├── requests.py       ← CompletionRequest, GenerationRequest, etc.
│   │   └── responses.py      ← CompletionResponse, ReviewResult, etc.
│   ├── services/
│   │   ├── akuai_client.py   ← HTTP client for AkuAI inference calls
│   │   ├── akudemy_client.py ← HTTP client for Akudemy LO lookups
│   │   ├── daas_client.py    ← HTTP client for DaaS fine-tuning export
│   │   ├── session_store.py  ← Redis-backed CodeSession CRUD
│   │   ├── inference.py      ← Dispatch: AkuAI (cloud) or llama-cpp (edge)
│   │   ├── review.py         ← ReviewResult construction from AkuAI response
│   │   ├── debug.py          ← Stack trace parser + FAISS debug index
│   │   └── guardrails.py     ← Harmful code classifier, license scan, rate limit
│   └── db/
│       ├── postgres.py       ← asyncpg session + migration runner
│       └── migrations/       ← Alembic migration versions
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
├── requirements.txt
└── alembic.ini
```

---

## 3. Local Development Setup

### Prerequisites

- Docker + Docker Compose (with `editor` profile)
- Python 3.11+ (for running tests outside Docker)
- Access to `ghcr.io/oumar-code/aku-code-editor:v0.1.0` (or build locally)

### Start the service

```bash
# Start infra + core + editor
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core --profile editor up -d

# Check health
curl http://localhost:8013/health
curl http://localhost:8013/ready

# View logs
docker compose -f docs/deployment/local/docker-compose.dev.yml logs -f aku-code-editor
```

### Environment variables (dev defaults)

All defaults are set in `docker-compose.dev.yml`. Key variables for local overrides:

```bash
# Force local GGUF inference (Phase 4+ only; model file must be present)
CODE_MODEL_PATH=/path/to/codegemma-2b-q4.gguf

# Enable guardrails (normally off in dev)
ENABLE_HARMFUL_CODE_FILTER=true
ENABLE_LICENSE_SCAN=true

# Reduce token budget for testing rate limiting
CODE_EDITOR_TOKEN_BUDGET=1000
```

---

## 4. API Usage Examples

### Tab-completion (Python)

```bash
curl -X POST http://localhost:8013/api/v1/code/complete \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "s_test_001",
    "file_content": "def calculate_wave_speed(frequency, wavelength):\n    ",
    "cursor_offset": 52,
    "language": "python",
    "max_tokens": 64
  }'
```

### Curriculum-grounded code generation

```bash
curl -X POST http://localhost:8013/api/v1/code/generate \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "s_test_001",
    "prompt": "Simulate projectile motion",
    "subject_context": "Physics",
    "language": "python",
    "lo_ids": ["LO:NERDC:PHY:SS2:KIN:001"]
  }'
```

### Code review

```bash
curl -X POST http://localhost:8013/api/v1/code/review \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "s_test_001",
    "file_path": "main.py",
    "file_content": "def run(cmd): return eval(cmd)",
    "language": "python"
  }'
```

### Submit feedback (correction)

```bash
curl -X POST http://localhost:8013/api/v1/code/sessions/s_test_001/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "completion_id": "c_uuid_001",
    "action": "corrected",
    "original_completion": "return frequency * wavelength",
    "user_correction": "return float(frequency) * float(wavelength)"
  }'
```

### SSE streaming (code generation)

```bash
curl -X POST http://localhost:8013/api/v1/code/generate \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"session_id": "s_test_001", "prompt": "Bubble sort in Python", "language": "python"}'
```

### WebSocket streaming

```python
import asyncio, websockets, json

async def stream():
    async with websockets.connect("ws://localhost:8013/ws/code/stream") as ws:
        await ws.send(json.dumps({
            "type": "completion",
            "session_id": "s_test_001",
            "file_content": "def add(a, b):\n    ",
            "cursor_offset": 20,
            "language": "python"
        }))
        async for msg in ws:
            data = json.loads(msg)
            if data["type"] == "stream_end":
                break
            print(data["token"], end="", flush=True)

asyncio.run(stream())
```

---

## 5. Inference Dispatch Logic

```python
# services/inference.py (simplified)

async def dispatch_completion(request: CompletionRequest, settings: Settings) -> CompletionResponse:
    if settings.CODE_MODEL_PATH:
        # Edge mode: local llama-cpp inference
        return await _local_inference(request, settings.CODE_MODEL_PATH)
    else:
        # Cloud mode: delegate to AkuAI
        return await akuai_client.code_complete(request)
```

The edge path uses `llama_cpp.Llama` (llama-cpp-python) with the GGUF file.  
The cloud path calls `AkuAI POST /api/v1/code/complete` over HTTP.

---

## 6. Session Memory Pattern

```python
# services/session_store.py (simplified)

import json
from redis.asyncio import Redis

REDIS_DB = 9

async def get_session(redis: Redis, session_id: str) -> CodeSession | None:
    raw = await redis.get(f"code_editor:session:{session_id}")
    if raw is None:
        return None
    return CodeSession.model_validate_json(raw)

async def upsert_session(redis: Redis, session: CodeSession, ttl: int) -> None:
    await redis.setex(
        f"code_editor:session:{session.session_id}",
        ttl,
        session.model_dump_json()
    )
```

All Redis keys follow the naming convention: `code_editor:<entity_type>:<id>`.  
See [`REDIS_KEY_TTL_POLICY.md`](../deployment/local/REDIS_KEY_TTL_POLICY.md) for full policy.

---

## 7. Correction Pair Export

When `action=corrected` is received at `POST /api/v1/code/sessions/{id}/feedback`:

1. Anonymize: re-hash `user_id_hash` with a salt; strip inline comments from code strings.
2. Append to Redis queue: `LPUSH code_editor:correction_queue:<date> <json_pair>`.
3. Background job (daily cron): batch-read queue → `POST /api/v1/datasets/ingest` to Aku-DaaS.
4. After successful export: persist to `code_editor.correction_pairs` Postgres table with `exported_to_daas=true`.

---

## 8. Guardrails Implementation

### Harmful Code Filter (`ENABLE_HARMFUL_CODE_FILTER=true`)

Pattern-based classifier over the generated code string. Blocks responses matching:
- Shell injection patterns: `` `...` ``, `subprocess.call("...${...}...")`, `os.system(...)`
- Credential exfiltration: `requests.get("http://...")` with env var access
- File system traversal: `open("../../...`
- Eval with user input: `eval(input(...))`, `exec(request.data)`

Blocked responses are logged with `trace_id`, `session_id` (hashed), and the blocking rule — never the raw code.

### License Compliance Scan (`ENABLE_LICENSE_SCAN=true`)

AST-based heuristic: detect function signatures that are exact matches to known GPL-licensed algorithms (e.g., GPL'd sorting implementations). Flags (does not block) for teacher review.

### Rate Limiting

Per-user daily token budget stored in Redis as a counter with 24h TTL:

```
code_editor:token_budget:<user_id_hash>  →  integer (tokens used today)
TTL: reset at midnight UTC
```

When counter exceeds `CODE_EDITOR_TOKEN_BUDGET`, return HTTP 429 with remaining quota in response body.

---

## 9. Testing

```bash
# Unit tests (no external services needed)
cd aku-code-editor
pytest tests/unit/ -v

# Integration tests (requires infra + core + editor running)
pytest tests/integration/ -v \
  --base-url http://localhost:8013 \
  --akuai-url http://localhost:8004

# Test streaming endpoint
pytest tests/integration/test_streaming.py -v -s
```

### Key test cases

| Test | Type | What it verifies |
|------|------|-----------------|
| `test_complete_stub` | Unit | Stub response matches OpenAPI schema |
| `test_complete_rate_limit` | Unit | 429 when budget exceeded |
| `test_session_crud` | Unit | Redis set/get/expire works correctly |
| `test_feedback_correction` | Unit | Correction pair is queued in Redis |
| `test_generate_with_lo_context` | Integration | Akudemy LO injection in generation prompt |
| `test_review_security_finding` | Integration | eval() code gets high-severity security finding |
| `test_sse_streaming` | Integration | SSE stream delivers tokens then stream_end |
| `test_ws_streaming` | Integration | WebSocket delivers tokens then stream_end |

---

## 10. Observability

### Prometheus Metrics

All metrics exposed at `GET /metrics`. Key metrics:

```
code_editor_completions_total{language="python"}
code_editor_completion_acceptance_rate
code_editor_request_duration_seconds{endpoint="/api/v1/code/complete",quantile="0.95"}
code_editor_tokens_generated_total{model="codegemma-2b-q4"}
code_editor_sessions_active
code_editor_correction_pairs_queued
```

### Grafana Dashboard

Import `docs/monitoring/grafana-dashboards/aku-code-editor.json` (Phase 4 deliverable).  
Dashboard panels:
- Completion acceptance rate (24h rolling)
- Request latency heatmap (p50/p95/p99)
- Tokens generated per day
- Active sessions gauge
- Harmful code blocks per week
- Error rate by endpoint

### Structured Log Fields

Every log line emits JSON:

```json
{
  "timestamp": "2026-04-27T20:00:00Z",
  "service": "aku-code-editor",
  "level": "info",
  "trace_id": "t_uuid",
  "session_id_hash": "sha256_of_session_id",
  "endpoint": "/api/v1/code/complete",
  "language": "python",
  "latency_ms": 210,
  "model_used": "codegemma-2b-q4",
  "message": "completion served"
}
```

No raw code, user IDs, or file contents appear in logs.

---

## 11. Deployment Reference

| Environment | Command / Manifest |
|-------------|-------------------|
| Dev | `docker compose --profile infra --profile core --profile editor up -d` |
| Staging/Prod | `kubectl apply -f docs/deployment/k8s/aku-code-editor.yaml` |
| Edge Hub (offline) | Mount GGUF PVC; set `CODE_MODEL_PATH` in ConfigMap |

See [`docs/deployment/k8s/aku-code-editor.yaml`](../deployment/k8s/aku-code-editor.yaml) for the full K8s manifest.
