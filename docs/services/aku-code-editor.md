# Aku Code Editor

> **Status:** Phase 3 Scaffold (stub endpoints live) → Phase 4 Learning Engine  
> **Host port (dev):** 8013 · **Container port:** 8000  
> **Docker profile:** `editor`  
> **Redis DB:** 9 (CodeSession, streaming buffers)  
> **Related:** [`strategy/aku-code-editor-strategy.md`](../strategy/aku-code-editor-strategy.md) · [`api/aku-code-editor-openapi.yaml`](../api/aku-code-editor-openapi.yaml) · [`handbooks/AkuCodeEditor_Handbook.md`](../handbooks/AkuCodeEditor_Handbook.md)

---

## Vision

Aku Code Editor is a **curriculum-grounded, edge-deployable, privacy-first AI code assistant** tightly integrated into the Aku Platform. It is not a general-purpose IDE plugin.

Distinguishing features:

1. **Learns from usage** — accepted/rejected completions and user corrections feed a fine-tuning queue, making the model progressively more accurate for Akulearn's code style and curriculum context.
2. **Curriculum-aware generation** — when a `subject_context` is provided (e.g., "Physics simulation"), the editor fetches related LO descriptions from Akudemy and injects them into the generation prompt, ensuring pedagogically correct code examples.
3. **Offline-first** — quantized code model (≤ 1.5 GB GGUF) deployed on Aku Edge Hub so rural schools can use AI code assistance without internet.
4. **Student safety guardrails** — harmful code patterns blocked server-side; no raw source code stored beyond the session TTL; teacher/admin controls scope by institution.
5. **AkuWorkspace integration** — students can generate code and embed it into an Aku Docs document in the same session, with inline AI explanation.

---

## Architecture

```
Student / Teacher
       │
       ▼
Aku Code Editor API (port 8013)
       │
       ├── Redis DB 9 ────── CodeSession (7-day TTL), streaming buffers
       │
       ├── AkuAI (8004) ─── POST /api/v1/code/complete   ← code model
       │                     POST /api/v1/code/generate    ← code model
       │                     POST /api/v1/code/explain     ← code model
       │                     POST /api/v1/code/review      ← code model
       │
       ├── Akudemy (8005) ── GET  /api/v1/curriculum/lo/{lo_id}
       │                     (subject_context → LO descriptions for prompt grounding)
       │
       └── Aku-DaaS (8012) ─ POST /api/v1/datasets/ingest
                              (correction pairs → fine-tuning queue)
```

In offline/edge mode (`CODE_MODEL_PATH` set), all inference is served locally from the quantized GGUF model without calling AkuAI.

---

## API Endpoints

See full OpenAPI spec: [`docs/api/aku-code-editor-openapi.yaml`](../api/aku-code-editor-openapi.yaml).

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/code/complete` | Tab-completion from cursor + context window |
| `POST` | `/api/v1/code/generate` | Natural language → code generation |
| `POST` | `/api/v1/code/explain` | Explain selected code block in plain language |
| `POST` | `/api/v1/code/review` | Static review: style / bugs / security / performance |
| `POST` | `/api/v1/code/debug` | Analyze error + stack trace → suggest fix |
| `GET` | `/api/v1/code/sessions/{session_id}` | Retrieve past session context |
| `POST` | `/api/v1/code/sessions/{session_id}/feedback` | Report accepted/rejected completion |
| `WS` | `/ws/code/stream` | WebSocket streaming completions (token-by-token) |
| `GET` | `/health` | Liveness check |
| `GET` | `/ready` | Readiness check (model loaded, Redis connected) |
| `GET` | `/metrics` | Prometheus metrics |

---

## Data Models

### `CodeSession`
```json
{
  "session_id": "s_uuid",
  "user_id_hash": "sha256_of_user_id",
  "language": "python",
  "framework": "fastapi",
  "subject_context": "Physics simulation",
  "lo_ids": ["LO:NERDC:PHY:SS2:WAV:001"],
  "accepted_completions": 12,
  "rejected_completions": 3,
  "last_active_at": "2026-04-27T20:00:00Z",
  "ttl_seconds": 604800
}
```

### `CompletionRequest`
```json
{
  "session_id": "s_uuid",
  "file_content": "def calculate_wave_speed(frequency, wavelength):\n    ",
  "cursor_offset": 52,
  "language": "python",
  "max_tokens": 128
}
```

### `GenerationRequest`
```json
{
  "session_id": "s_uuid",
  "prompt": "Write a Python function to simulate projectile motion",
  "subject_context": "Physics",
  "language": "python",
  "lo_ids": ["LO:NERDC:PHY:SS2:KIN:001"]
}
```

### `ReviewResult`
```json
{
  "file_path": "main.py",
  "findings": [
    {
      "line": 14,
      "category": "security",
      "severity": "high",
      "message": "Use of eval() with unsanitized input",
      "suggestion": "Use ast.literal_eval() or a safe parser instead"
    },
    {
      "line": 22,
      "category": "style",
      "severity": "low",
      "message": "Variable name 'x' is not descriptive",
      "suggestion": "Rename to 'velocity_ms' for clarity"
    }
  ]
}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development` / `staging` / `production` |
| `LOG_LEVEL` | `info` | `debug` / `info` / `warning` / `error` |
| `AKU_AI_URL` | — | AkuAI base URL for inference calls |
| `AKUDEMY_URL` | — | Akudemy base URL for LO context lookups |
| `AKU_DAAS_URL` | — | Aku-DaaS base URL for fine-tuning queue export |
| `REDIS_URL` | — | Redis connection string (DB 9) |
| `CODE_SESSION_TTL_SECONDS` | `604800` | CodeSession TTL (7 days) |
| `CODE_MODEL_PATH` | `""` | Path to local GGUF code model; empty = delegate to AkuAI |
| `CODE_EDITOR_TOKEN_BUDGET` | `200000` | Per-user daily token budget |
| `CODE_CONTEXT_MAX_TOKENS` | `2048` | Max tokens from current file sent as context |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed CORS origins |
| `ENABLE_SSE` | `true` | Enable Server-Sent Events for streaming |
| `ENABLE_WEBSOCKET` | `true` | Enable WebSocket endpoint |
| `ENABLE_HARMFUL_CODE_FILTER` | `false` | Enable harmful code detection guardrail |
| `ENABLE_LICENSE_SCAN` | `false` | Enable GPL license compliance scan |

---

## Learning Engine (Phase 4)

### Session Memory
- `CodeSession` stored in Redis DB 9 (TTL: `CODE_SESSION_TTL_SECONDS`, default 7 days).
- Each session carries: files edited, completions accepted/rejected, language/framework context, subject context, lo_ids.

### Learning from Corrections
When a user edits a generated completion:
1. Record `(original_completion, user_correction)` pair in Redis.
2. Batch-export correction pairs (anonymized — user ID hashed) to Aku-DaaS fine-tuning queue via `POST /api/v1/datasets/ingest`.
3. Pairs are also persisted to the `code_editor.correction_pairs` Postgres table for audit and batch processing.

### Context-Aware Completions
- Pass the last `CODE_CONTEXT_MAX_TOKENS` tokens of the current file + `session_context` to AkuAI `code/complete`.
- Sliding context window: prioritize recently edited lines over earlier file content.

### Curriculum-Aware Generation
- When `subject_context` is provided, fetch related LO descriptions from Akudemy.
- Inject LO descriptions into the generation system prompt:
  ```
  You are generating a {language} code example for an Akulearn student.
  Subject: {subject_context}
  Learning objectives:
  - {lo_description_1}
  - {lo_description_2}
  Generate code that accurately illustrates these concepts.
  ```

### Debug Assistant
- Parse Python/JS stack traces using a structured regex extractor.
- Embed `error_message + relevant_code` and retrieve similar past resolutions from a local FAISS debug-examples index.
- Return a structured `DebugResult` with suggested fix + explanation.

---

## Observability

### Prometheus Metrics (exported at `/metrics`)

| Metric | Type | Description |
|--------|------|-------------|
| `code_editor_completions_total` | Counter | Total completion requests by language |
| `code_editor_completion_acceptance_rate` | Gauge | Rolling 24h acceptance rate |
| `code_editor_generation_total` | Counter | Total generation requests |
| `code_editor_review_total` | Counter | Total review requests |
| `code_editor_debug_total` | Counter | Total debug requests |
| `code_editor_sessions_active` | Gauge | Active sessions (TTL-aware) |
| `code_editor_tokens_generated_total` | Counter | Total tokens generated (by model) |
| `code_editor_request_duration_seconds` | Histogram | Request latency (p50/p95/p99) |
| `code_editor_correction_pairs_queued` | Gauge | Correction pairs pending DaaS export |

### SLO Targets (Tier 1)

| SLO | Target | Alert threshold |
|-----|--------|----------------|
| Availability | 99.9% | < 99.5% |
| Completion latency p95 | ≤ 500 ms | > 800 ms |
| Generation latency p95 | ≤ 2 000 ms | > 4 000 ms |
| Acceptance rate (dogfooding) | ≥ 40% | < 30% |
| Token budget overrun rate | ≤ 0.01% | > 0.1% |

---

## Security & Privacy

- **No raw source code stored.** Session context lives in Redis only during the session TTL. Postgres stores only anonymized session summaries and correction pairs (never raw code).
- **PII-free audit logs.** `user_id_hash` is a one-way SHA-256 hash. No name, email, or raw learner ID appears in logs or stored data.
- **Correction pairs anonymized.** Before export to DaaS fine-tuning queue, `user_id_hash` is re-hashed and code snippets are stripped of inline comments that could contain names.
- **Harmful code guardrail (Phase 5).** `ENABLE_HARMFUL_CODE_FILTER=true` activates classifier-based detection for shell injection, credential exfiltration, and known malware patterns. Blocked requests are logged and surfaced in admin dashboard.
- **Rate limiting.** `CODE_EDITOR_TOKEN_BUDGET` enforces a per-user daily token cap. Quota status is cached in Redis DB 9.

---

## Deployment

### Dev (Docker Compose)

```bash
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core --profile editor up -d
```

### Kubernetes

See: [`docs/deployment/k8s/aku-code-editor.yaml`](../deployment/k8s/aku-code-editor.yaml)

### Edge Hub (K3s)

When `CODE_MODEL_PATH` is set to a mounted GGUF path (e.g., `/aku/models/codegemma-2b-q4.gguf`), all inference runs locally without calling AkuAI. The Edge Hub K3s deployment mounts a PersistentVolume containing the model file.

---

## Runbook

See: [`docs/runbooks/aku-code-editor-runbook.md`](../runbooks/aku-code-editor-runbook.md)
