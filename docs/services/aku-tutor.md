# AkuTutor

> **Status:** Phase 1 Stub → Phase 2 Full RAG Pipeline  
> **Host port (dev):** 8007 · **Container port:** 8000  
> **Docker profile:** `core`  
> **Inference:** Delegates 100% to AkuAI — runs no model locally  
> **Related:** [`api/aku-tutor-openapi.yaml`](../api/aku-tutor-openapi.yaml) · [`strategy/rag_chatbot_strategy.md`](../strategy/rag_chatbot_strategy.md)

---

## Vision

AkuTutor is the **AI tutoring service** for the Aku Platform. It answers curriculum questions from students and teachers using a **Retrieval-Augmented Generation (RAG)** pipeline:

1. **Retrieve** — embed the question via AkuAI; query Aku-EdgeHub FAISS index for top-k relevant curriculum chunks.
2. **Re-rank** — score results by trust level and recency.
3. **Generate** — send enriched context to AkuAI for prose generation.
4. **Respond** — return answer + citations (LO IDs, chunk sources).

AkuTutor never runs a model locally. All inference is delegated to AkuAI (port 8004).

---

## Architecture

```
Student / Teacher
        │
        ▼
AkuTutor (port 8007)
        │
        ├── AkuAI (8004) ─── POST /api/v1/embeddings  (question embedding)
        │                     POST /api/v1/text/generate (answer generation)
        │
        └── Aku-EdgeHub (8006) ── POST /api/v1/edge/rag/query  (chunk retrieval)
```

In Phase 1, both upstream calls fall back to stub responses when `AKU_AI_URL` is empty or the service returns a stub flag.

---

## API Endpoints

See full OpenAPI spec: [`docs/api/aku-tutor-openapi.yaml`](../api/aku-tutor-openapi.yaml).

### Phase 1

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/tutor/ask` | Submit a tutoring question; get an answer + citations |
| `GET` | `/health` | Liveness check |
| `GET` | `/ready` | Readiness — AkuAI reachable |
| `GET` | `/metrics` | Prometheus metrics |

### Phase 2

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/tutor/feedback` | Teacher marks a response as helpful/incorrect; updates chunk trust |
| `GET` | `/api/v1/tutor/sessions/{session_id}` | Retrieve a past tutoring session |
| `POST` | `/api/v1/tutor/sessions/{session_id}/hint` | Request a hint (server tracks hint counter) |

---

## Data Models

### `TutorAskRequest`

```json
{
  "learner_id": "<sha256_hashed_id>",
  "class_level": "SS2",
  "subject": "PHY",
  "exam_path": ["WAEC"],
  "language": "en",
  "response_mode": "step_by_step",
  "question": "Explain how sound waves travel through different media.",
  "session_id": "session_uuid_001"
}
```

#### `response_mode` values

| Mode | Behaviour |
|------|-----------|
| `direct` | Concise direct answer |
| `step_by_step` | Numbered steps; preferred when mastery < 60% |
| `hint_only` | Returns a hint; server tracks counter (max 3 per question) → full answer on 4th request |
| `exam_style` | Answers in WAEC/NECO marking-scheme format |
| `recap` | Summarises multiple LOs as a revision note |

### `TutorAskResponse`

```json
{
  "answer": "Sound waves are longitudinal waves that transfer energy through particle vibrations...",
  "response_mode": "step_by_step",
  "citations": [
    {
      "chunk_id": "chunk_042",
      "lo_id": "LO:NERDC:PHY:SS2:SND:001",
      "topic": "Sound and Waves",
      "trust_level": 4
    }
  ],
  "grounding_score": 0.88,
  "hint_count": 0,
  "stub": false,
  "latency_ms": 540
}
```

### `TutorFeedbackRequest` (Phase 2)

```json
{
  "session_id": "session_uuid_001",
  "response_id": "resp_uuid_001",
  "rating": "incorrect",
  "teacher_correction": "Sound waves require a medium to travel; they cannot travel through a vacuum.",
  "chunk_ids_to_penalise": ["chunk_042"]
}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development` / `staging` / `production` |
| `LOG_LEVEL` | `INFO` | Log verbosity |
| `AKU_AI_URL` | — | AkuAI base URL (e.g., `http://akuai:8000`) |
| `AKU_EDGEHUB_URL` | — | EdgeHub base URL for RAG retrieval (Phase 2) |
| `HTTP_TIMEOUT` | `30.0` | Seconds before upstream HTTP calls time out |
| `GROUNDING_SCORE_THRESHOLD` | `0.75` | Min retrieval score to include a chunk; below = off-topic guard |
| `HINT_MAX_COUNT` | `3` | Max hints before full answer is revealed |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed CORS origins |

---

## Phase 1 — Stub Implementation

In Phase 1, AkuTutor:

1. Accepts `POST /api/v1/tutor/ask` with the full request body.
2. If `AKU_AI_URL` is set, calls `POST /api/v1/text/generate` on AkuAI with the question as prompt.
3. If AkuAI returns `stub: true` (or URL is empty), substitutes: `"[STUB] AkuTutor placeholder response."`.
4. Returns the response with `stub: true` and empty `citations`.
5. Writes a structured audit log entry (no raw PII).

Audit log format (Phase 1 skeleton):

```json
{
  "timestamp": "2026-04-27T20:00:00Z",
  "service": "akututor",
  "event": "tutor_ask",
  "trace_id": "t_uuid",
  "session_id": "session_uuid_001",
  "learner_id_hash": "sha256:...",
  "subject": "PHY",
  "class_level": "SS2",
  "response_mode": "step_by_step",
  "stub": true,
  "latency_ms": 12
}
```

---

## Phase 2 — Full RAG Pipeline

```
question
    │
    ▼  [1] embed question
AkuAI POST /api/v1/embeddings  →  384-dim vector
    │
    ▼  [2] retrieve chunks
Aku-EdgeHub POST /api/v1/edge/rag/query  →  top-k chunks
    │
    ▼  [3] re-rank
    Sort by: trust_level × recency_score × cosine_similarity
    Filter:  grounding_score ≥ GROUNDING_SCORE_THRESHOLD (0.75)
    │
    ▼  [4] build prompt
    System: "You are an Akulearn tutor for {class_level} {subject} students."
    Context: top-3 chunk texts + LO descriptions
    Question: {question}
    Mode: {response_mode}
    │
    ▼  [5] generate
AkuAI POST /api/v1/text/generate  →  answer text
    │
    ▼  [6] respond
    TutorAskResponse with citations, grounding_score, latency_ms
```

### Guardrails (Phase 2)

| Guardrail | Trigger | Action |
|-----------|---------|--------|
| Grounding check | `grounding_score < 0.75` after retrieval | Respond: "I don't have enough curriculum information on this topic." |
| Off-topic classifier | Question unrelated to the session's subject | Respond: "This question is outside the {subject} curriculum scope." |
| Safety filter | Potentially harmful prompt detected | Reject with `400 Bad Request`; log event |

### Hint Counter (Phase 2)

Server-side counter per `(session_id, question_hash)` stored in Redis (DB of AkuTutor — uses AkuAI's Redis if standalone; or a dedicated counter in its own Redis namespace):

```
akututor:hint_count:<session_id>:<question_hash>  →  integer
TTL: 24 h
```

When `hint_count >= HINT_MAX_COUNT` (3), the next request with `response_mode=hint_only` automatically upgrades to `direct` mode and returns the full answer.

---

## Observability

### Prometheus Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `akututor_ask_requests_total` | Counter | Total tutoring requests by subject and mode |
| `akututor_ask_latency_seconds` | Histogram | End-to-end latency (p50/p95/p99) |
| `akututor_grounding_score` | Histogram | Distribution of grounding scores |
| `akututor_stub_responses_total` | Counter | Stub responses (AkuAI unavailable) |
| `akututor_off_topic_total` | Counter | Off-topic rejections |
| `akututor_safety_rejections_total` | Counter | Safety filter rejections |

---

## Phase 1 Exit Criteria

- [ ] Service starts healthy in `infra + core` profile
- [ ] `GET /health` returns `200 OK`
- [ ] `GET /ready` returns `200 OK`
- [ ] `POST /api/v1/tutor/ask` forwards question to AkuAI and returns response (stub acceptable)
- [ ] Audit log entry written for every request (no raw PII in log)
- [ ] Prometheus scrape target active at `akututor:8000/metrics`
- [ ] Graceful fallback to stub response when `AKU_AI_URL` is empty

## Phase 2 Exit Criteria

- [ ] Full RAG pipeline: embed → retrieve → re-rank → generate → respond
- [ ] All 5 `response_mode` values produce distinct response shapes
- [ ] `hint_only` mode enforces max 3 hints per question; 4th request returns full answer
- [ ] Grounding check rejects off-topic questions with correct message
- [ ] `grounding_score` ≥ 0.75 in ≥ 80% of integration test queries
- [ ] AkuTutor edge latency p95 ≤ 800 ms in integration test (stub AkuAI)
