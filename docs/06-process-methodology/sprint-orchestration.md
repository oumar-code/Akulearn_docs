# 5-Phase Sprint Orchestration — Aku Platform Services + Aku Code Editor

> **Status:** Active  
> **Last updated:** April 2026  
> **Owner:** Platform Engineering  
> **Related docs:** [`docker-compose.dev.yml`](../deployment/local/docker-compose.dev.yml) · [`aku-code-editor-strategy.md`](../strategy/aku-code-editor-strategy.md) · [`AIOPS_STRATEGY.md`](../AIOPS_STRATEGY.md) · [`strategy/rag_chatbot_strategy.md`](../strategy/rag_chatbot_strategy.md)

---

## Platform Service Map

| Profile | Service | Host Port | Key Role |
|---------|---------|-----------|----------|
| infra | Postgres 16 | 5432 | Shared relational DB (schema-per-service) |
| infra | Redis 7 | 6379 | Pub/sub, caching, DB indexes 2–9 |
| infra | Neo4j 5 | 7474 / 7687 | Knowledge graph (LO relationships, learner graph) |
| core | AkuAI | 8004 | Inference engine — embeddings + text generation |
| core | Akudemy | 8005 | Curriculum LMS + content delivery |
| core | Aku-EdgeHub | 8006 | Edge orchestrator, offline-first, SQLite in dev |
| core | AkuTutor | 8007 | RAG tutoring chatbot, delegates all inference to AkuAI |
| full | Aku-IGHub | 8008 | Idempotency gateway + event deduplication |
| full | Aku-SuperHub | 8009 | Central orchestration hub + JWT auth |
| full | AkuWorkspace | 8010 | AI productivity layer (docs, data insights) |
| full | Aku-Telhone | 8011 | eSIM / OTA / telco management |
| full | Aku-DaaS | 8012 | Data-as-a-Service, anonymized datasets |
| **editor** | **Aku-Code-Editor** | **8013** | **AI code editor — learns + generates code** |
| monitoring | Prometheus | 9090 | Metrics scraping |
| monitoring | Grafana | 3001 | Dashboards + alerting |

---

## Phase 1 — Foundation & Hardening (Sprints 1–2)

**Goal:** Every container that can be built and run is healthy, observable, and has a documented API surface.

### Infra

#### Postgres
- Define per-service schemas (`akuai`, `akudemy`, `superhub`, `daas`) with Alembic migration scripts wired into each service's startup routine.
- See: [`docs/deployment/local/postgres-schemas.md`](../deployment/local/postgres-schemas.md)
- Single shared database `aku_platform` in dev; each service connects to its own schema via `search_path`.

**Checklist:**
- [x] `akuai` schema SQL defined (`inference_log`, `model_registry`)
- [x] `akudemy` schema SQL defined (`subjects`, `class_levels`, `learning_objectives`, `content_chunks`, `exam_papers`)
- [x] `superhub` schema SQL defined (`service_registry`, `routing_policies`)
- [x] `daas` schema SQL defined (`datasets`, `ingestion_jobs`, `pipeline_status`, `access_grants`)
- [x] `code_editor` schema SQL defined (`correction_pairs`, `session_summaries`)
- [ ] Each service's Alembic `versions/` directory seeded with initial migration
- [ ] `alembic upgrade head` succeeds on a clean `aku_platform` database

#### Redis
- Document DB index ownership (DB 2–9) in [`docs/deployment/local/REDIS_KEY_TTL_POLICY.md`](../deployment/local/REDIS_KEY_TTL_POLICY.md).
- Validate `maxmemory-policy allkeys-lru` does not evict session-critical JWT or idempotency keys.
- Mitigation: move JWT session keys to DB 0 with a dedicated `volatile-lru` pool if eviction pressure is observed.

**Checklist:**
- [x] DB index ownership table documented (DB 2–10)
- [x] TTL policy per key category documented
- [x] `maxmemory 96mb allkeys-lru` in `docker-compose.dev.yml`
- [ ] Prometheus alert configured for `redis_memory_used_bytes / redis_memory_max_bytes > 0.80`
- [ ] Critical-key monitor implemented for JWT (DB 6) and idempotency keys (DB 5)

#### Neo4j
- Create the initial LO knowledge graph schema — see [`docs/infra/neo4j-lo-schema.md`](../infra/neo4j-lo-schema.md).
- Nodes: `LO`, `Topic`, `Subject`, `ExamBoard`.
- Relationships: `BELONGS_TO`, `PREREQUISITE_OF`, `ASSESSED_BY`.
- Seed with pilot subjects: ENG, MAT, BIO (JSS1–SS3).

**Checklist:**
- [x] Node types and relationship types documented in `docs/infra/neo4j-lo-schema.md`
- [x] Uniqueness constraint Cypher for `LO.lo_id` defined
- [x] Full-text index on `LO.description` defined
- [x] Pilot seed Cypher script (`ENG`, `MAT`, `BIO` subjects + ExamBoards) written
- [x] Sample LO prerequisite chain (BIO SS2 cell division) documented
- [x] Common query patterns (prerequisite chain, next-best-LO, exam-frequency) documented
- [ ] Seed script runs successfully against dev Neo4j container
- [ ] Prerequisite chain query returns correct result in < 50 ms

### AkuAI (8004)

**Stub API contract** — see [`docs/services/aku-ai.md`](../services/aku-ai.md) and [`docs/api/akuai-openapi.yaml`](../api/akuai-openapi.yaml):

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/embeddings` | Embed text to 384-dim vector (stub: zero-vector) |
| `POST` | `/api/v1/text/generate` | Generate text via Gemma GGUF or stub |
| `POST` | `/api/v1/code/generate` | Generate code from prompt (stub → Phase 2) |
| `POST` | `/api/v1/code/explain` | Explain code block (stub → Phase 2) |
| `GET` | `/health` | Liveness check |
| `GET` | `/ready` | Readiness check — model loaded |
| `GET` | `/metrics` | Prometheus metrics |

**Checklist:**
- [x] Service documented in `docs/services/aku-ai.md`
- [x] OpenAPI spec created at `docs/api/akuai-openapi.yaml`
- [x] Environment variables documented
- [x] Stub response specification defined (deterministic per endpoint)
- [x] Prometheus scrape target active at `akuai:8000/metrics` in `monitoring/prometheus.yml`
- [ ] Service starts healthy in `infra + core` profile on a 6 GB machine
- [ ] `GET /health` returns `200 OK` with `{"status": "ok"}`
- [ ] `POST /api/v1/embeddings` returns 384-dim zero-vector with `stub: true`
- [ ] All log lines emit valid JSON with required fields

### Akudemy (8005)

- Postgres schema `akudemy`: tables `subjects`, `class_levels`, `learning_objectives`, `content_chunks`, `exam_papers`.
- Seed JSS1–SS3 LO catalog (from `lo_catalog.json`), 3 pilot subjects.
- Initial endpoints: `GET /api/v1/curriculum/lo/{lo_id}`, `GET /health`, `GET /ready`, `GET /metrics`.

**Checklist:**
- [x] Postgres schema SQL defined in `docs/deployment/local/postgres-schemas.md`
- [ ] Alembic migration created and runs on startup
- [ ] `lo_catalog.json` seed file created for ENG, MAT, BIO (JSS1–SS3)
- [ ] `GET /api/v1/curriculum/lo/{lo_id}` returns LO from Postgres
- [ ] `GET /health` and `GET /ready` return `200 OK`
- [ ] Prometheus scrape target active

### Aku-EdgeHub (8006)

- SQLite schema: tables `sync_state`, `cached_chunks`, `cached_lo_catalog`, `pending_events`.
- Stub sync agent: `POST /sync/request`, `GET /sync/status`.
- Validate Docker service-name resolution to `akudemy:8000` and `akuai:8000`.

**Checklist:**
- [x] Service documented in `docs/services/aku-edgehub.md`
- [x] OpenAPI spec created at `docs/api/aku-edgehub-openapi.yaml`
- [x] SQLite schema (all 4 tables) documented
- [x] Environment variables documented
- [ ] SQLite schema created on first container startup
- [ ] `POST /sync/request` returns `{"status": "queued"}` (stub)
- [ ] `GET /sync/status` returns status for all categories
- [ ] Docker service-name resolution to `akudemy:8000` and `akuai:8000` confirmed

### AkuTutor (8007)

- Wire call to `AkuAI /api/v1/text/generate`; fall back to stub response when AkuAI path is empty.
- Implement base `POST /api/v1/tutor/ask` with context envelope.
- Add audit log skeleton: structured JSON per interaction (no raw PII).

**Checklist:**
- [x] Service documented in `docs/services/aku-tutor.md`
- [x] OpenAPI spec created at `docs/api/aku-tutor-openapi.yaml`
- [x] Phase 1 stub implementation specified (fallback when `AKU_AI_URL` empty)
- [x] Audit log JSON format documented
- [ ] `POST /api/v1/tutor/ask` forwards to AkuAI and returns response
- [ ] Graceful stub fallback when `AKU_AI_URL` is empty or AkuAI returns `stub: true`
- [ ] Audit log entry written for every request (no raw PII)
- [ ] Prometheus scrape target active

### All Services — Cross-Cutting Standards

- **Structured logging:** every service emits JSON logs with fields `trace_id`, `service`, `level`, `timestamp`, `message`.
- **Health endpoints:** `/health` (liveness) and `/ready` (readiness) on every service. Docker `healthcheck` must target `/ready` where available.
- **Prometheus scrape:** all 13 services registered as scrape targets in `monitoring/prometheus.yml`.

**Checklist:**
- [x] All 13 services registered in `monitoring/prometheus.yml`
- [x] `healthcheck` targets `/health` for all services in `docker-compose.dev.yml`
- [x] JSON structured log format documented for AkuAI, AkuTutor, Aku Code Editor
- [ ] All 13 service containers start successfully in `infra + core + full + editor` profile
- [ ] `infra + core` stack starts healthy in < 60 s on a 6 GB machine

### Phase 1 Exit Criteria

| Criterion | Status |
|-----------|--------|
| Postgres schemas defined (all 5 services) | ✅ Documented |
| Redis key-space policy documented | ✅ Documented |
| Neo4j LO schema documented + seed Cypher written | ✅ Documented |
| AkuAI stub API contract + OpenAPI spec | ✅ Documented |
| Akudemy initial endpoints + schema | ✅ Documented |
| EdgeHub SQLite schema + stub sync agent | ✅ Documented |
| AkuTutor stub ask endpoint + audit log | ✅ Documented |
| All 13 scrape targets in `prometheus.yml` | ✅ Done |
| All services `healthcheck` configured in compose | ✅ Done |
| Full `infra + core` stack starts in < 60 s | ⬜ Pending service repo implementation |

---

## Phase 2 — Core Feature Completion (Sprints 3–4)

**Goal:** Every core service delivers its primary functional path end-to-end with real data.

### AkuAI (8004)

- Real embedding: load `all-MiniLM-L6-v2` (ONNX) when `MODEL_DIR` is set → return 384-dim vectors; return zero-vector stub when unset.
- GGUF text generation: load `gemma-2b-q4.gguf` from `GEMMA_GGUF_PATH`; stub responses when path is empty.
- Rate limiting: `GEMMA_MAX_PAYLOAD_BYTES` gate → `429 Too Many Requests` on overload.
- Code inference stubs for `/api/v1/code/generate` and `/api/v1/code/explain` (wired to code model in Phase 4).

**Checklist:**
- [x] Real embedding path documented (ONNX `InferenceSession`, `MODEL_DIR` env var)
- [x] GGUF text generation path documented (`llama_cpp.Llama`, `GEMMA_GGUF_PATH`)
- [x] Rate-limiting behaviour documented (`GEMMA_MAX_PAYLOAD_BYTES` → 429)
- [x] Redis cache strategy documented (5-min TTL keyed by `sha256(text)`)
- [x] `stub: false` response behaviour documented
- [ ] Real embedding returns correct 384-dim vector for test input
- [ ] `gemma-2b-q4.gguf` generates prose when `GEMMA_GGUF_PATH` is set
- [ ] `429` returned and `Retry-After` header set when payload gate exceeded
- [ ] Inference cache hit rate > 0 in local load test
- [ ] `akuai.inference_log` table populated (no raw text stored)

### Akudemy (8005)

- Full CRUD: `POST /api/v1/content/chunks`, `PUT /api/v1/content/chunks/{id}`, `DELETE /api/v1/content/chunks/{id}`.
- LO tagging pipeline: ingest markdown/JSON chunks → auto-assign candidate `lo_ids` → `review_status=pending`.
- Content freshness: background job flags chunks older than 365 days.
- Exam-papers endpoints: `GET /api/v1/exam-papers`, `GET /api/v1/exam-papers/{id}`.

**Checklist:**
- [x] `content_chunks` table schema defined (with `review_status`, `trust_level`, `updated_at`)
- [x] `exam_papers` table schema defined
- [ ] `POST /api/v1/content/chunks` creates chunk and sets `review_status=pending`
- [ ] `PUT /api/v1/content/chunks/{id}` updates content and refreshes `updated_at`
- [ ] `DELETE /api/v1/content/chunks/{id}` soft-deletes or removes record
- [ ] LO tagging pipeline: ingest → auto-assign `lo_ids` from LO catalog match
- [ ] Background freshness job flags chunks where `updated_at < now() - 365 days`
- [ ] `GET /api/v1/exam-papers` and `GET /api/v1/exam-papers/{id}` return results from Postgres

### Aku-EdgeHub (8006)

- Full delta sync agent: on connectivity window pull updated chunks from Akudemy, merge into SQLite, refresh `lo_catalog.json`.
- FAISS index build (`IndexFlatIP`), enforcing ≤ 500 MB limit.
- `POST /api/v1/edge/rag/query` — two-layer retrieval: curriculum filter → semantic search → top-k re-rank.
- Offline mode: `OPERATING_MODE=offline` serves all requests from local index only.

**Checklist:**
- [x] Delta sync agent flow documented (pull → upsert → FAISS add → ETag update)
- [x] FAISS `IndexFlatIP` with 500 MB cap documented
- [x] Two-layer RAG query flow documented (curriculum filter → FAISS → re-rank)
- [x] Offline mode behaviour documented
- [x] `RAGQueryRequest` / `RAGQueryResponse` schemas in OpenAPI spec
- [ ] Delta sync downloads updated chunks from Akudemy `?since=<last_sync_at>`
- [ ] FAISS index builds successfully with ≤ 500 MB cap enforced
- [ ] `POST /api/v1/edge/rag/query` returns ranked results in < 200 ms on dev
- [ ] `OPERATING_MODE=offline` serves all requests from local index (no upstream calls)
- [ ] Outbound events buffer and retry correctly when upstream is unreachable

### AkuTutor (8007)

- Full RAG pipeline: question → AkuAI embed → EdgeHub rag query → re-rank (trust × recency) → AkuAI generate → response + citation.
- All 5 response modes: `direct`, `step_by_step`, `hint_only`, `exam_style`, `recap`.
- `hint_only` session counter: server-side, max 3 hints → full answer revealed.
- Guardrails: grounding check (score ≥ 0.75), off-topic classification, safety filter.

**Checklist:**
- [x] Full RAG pipeline flow documented (6-step: embed → retrieve → re-rank → prompt → generate → respond)
- [x] All 5 `response_mode` values documented with distinct behaviours
- [x] `hint_only` server-side counter documented (Redis key pattern, TTL, max → upgrade)
- [x] Guardrails documented (grounding check, off-topic, safety filter)
- [x] Teacher feedback endpoint documented (`POST /api/v1/tutor/feedback`)
- [x] `TutorFeedbackRequest` schema in OpenAPI spec (trust level increment/decrement)
- [ ] Full RAG pipeline: embed → retrieve → re-rank → generate → respond (integration test)
- [ ] All 5 `response_mode` values produce distinct response shapes
- [ ] `hint_only` enforces max 3 hints; 4th request returns full answer
- [ ] Grounding check rejects off-topic questions with correct message
- [ ] `grounding_score` ≥ 0.75 in ≥ 80% of integration test queries
- [ ] AkuTutor edge latency p95 ≤ 800 ms in integration test

### AkuWorkspace (8010) — Begin Activation

- `POST /api/v1/workspace/query` — natural language → DaaS query → chart/summary response.
- `POST /api/v1/workspace/docs/generate` — generate document via AkuAI text generation.
- Circuit-breaker on every downstream call (`AKU_AI_URL`, `AKU_DAAS_URL`, `AKUDEMY_URL`).

**Checklist:**
- [x] AkuWorkspace service document exists (`docs/services/aku-workspace.md`)
- [x] Downstream service URLs documented in `docker-compose.dev.yml` (`AKU_AI_URL`, `AKU_DAAS_URL`, `AKUDEMY_URL`)
- [ ] `POST /api/v1/workspace/query` accepts NL query, calls DaaS, returns chart/summary
- [ ] `POST /api/v1/workspace/docs/generate` calls AkuAI and returns generated document
- [ ] Circuit-breaker wraps every downstream HTTP call (open on ≥ 5 consecutive failures)
- [ ] Service starts healthy in `infra + core + full` profile

### Aku-DaaS (8012) — Begin Activation

- Postgres schema `daas`: tables `datasets`, `ingestion_jobs`, `pipeline_status`, `access_grants`.
- `POST /api/v1/datasets/ingest`, `GET /api/v1/datasets/{id}` with PII field masking anonymization hook.
- `GET /api/v1/query` — accepts natural language, returns anonymized dataset slice.

**Checklist:**
- [x] `daas` schema SQL defined (`datasets`, `ingestion_jobs`, `pipeline_status`, `access_grants`)
- [x] `is_anonymized` flag and `owner_id` hashing documented in schema
- [ ] Alembic migration for `daas` schema runs on startup
- [ ] `POST /api/v1/datasets/ingest` creates `ingestion_job` and kicks off pipeline
- [ ] `GET /api/v1/datasets/{id}` returns dataset metadata (never raw PII)
- [ ] PII field masking anonymization hook applied on ingest
- [ ] `GET /api/v1/query` returns anonymized dataset slice for NL query
- [ ] Service starts healthy in `infra + core + full` profile

### Phase 2 Exit Criteria

| Criterion | Status |
|-----------|--------|
| AkuAI real embedding (ONNX) documented | ✅ Documented |
| AkuAI GGUF text generation documented | ✅ Documented |
| Akudemy full CRUD + LO tagging documented | ✅ Documented |
| EdgeHub delta sync + FAISS RAG documented | ✅ Documented |
| AkuTutor full RAG + 5 modes documented | ✅ Documented |
| AkuWorkspace begin activation documented | ✅ Documented |
| DaaS begin activation + schema documented | ✅ Documented |
| AkuAI real embedding returns correct 384-dim vector | ⬜ Pending service repo |
| AkuTutor RAG pipeline integration test passes | ⬜ Pending service repo |
| EdgeHub FAISS index builds within 500 MB cap | ⬜ Pending service repo |

---

## Phase 3 — Full-Stack Integration & Aku Code Editor Scaffold (Sprints 5–6)

**Goal:** All 9 existing services wire together; Aku Code Editor scaffolded with full API contracts.

### Aku-SuperHub (8009)

- JWT issuance and validation middleware; `JWT_SECRET_KEY` injected via env in dev, secrets manager in prod.
- Service registry: `GET /api/v1/services` lists all registered services + health status.
- Cross-tier routing policy: EdgeHub → SuperHub → IGHub based on latency / cost / privacy configuration.

### Aku-IGHub (8008)

- `X-Idempotency-Key` header middleware; 24h TTL stored in Redis DB 5.
- SHA-256 event deduplication for content ingestion events.
- `POST /api/v1/gateway/forward` — authenticated reverse proxy to upstream services.

### Aku-Telhone (8011)

- eSIM OTA stub: `POST /api/v1/esim/provision`, `GET /api/v1/esim/status/{iccid}`.
- Idempotent provisioning requests routed through Aku-IGHub.
- SM-DP+ protocol stub: returns mocked activation codes in dev.

### Cross-Service Contract Testing

- OpenAPI contracts for all inter-service calls defined in `aku-platform-contracts/`.
- Integration test suite activated: `--profile infra --profile core --profile full`.
- Contract lint step added to `.github/workflows/service-integration-test.yml`.

### 🆕 Aku Code Editor — Scaffold (port 8013)

Added to `docker-compose.dev.yml` under the `editor` profile (128 MB dev allocation).

**API Contract** — see [`docs/api/aku-code-editor-openapi.yaml`](../api/aku-code-editor-openapi.yaml):

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/code/complete` | Tab-completion from cursor + context window |
| `POST` | `/api/v1/code/generate` | Natural language → code generation |
| `POST` | `/api/v1/code/explain` | Explain selected code block |
| `POST` | `/api/v1/code/review` | Static review: style / bugs / security / performance |
| `POST` | `/api/v1/code/debug` | Error + stack trace → suggested fix |
| `GET` | `/api/v1/code/sessions/{session_id}` | Retrieve past session context |
| `POST` | `/api/v1/code/sessions/{session_id}/feedback` | Accept/reject completion feedback |
| `WS` | `/ws/code/stream` | WebSocket streaming completions |
| `GET` | `/health` | Liveness check |
| `GET` | `/ready` | Readiness check |
| `GET` | `/metrics` | Prometheus metrics |

**Core Data Models:**

```
CodeSession       — session_id, user_id, language, framework, context_window, accepted_completions, rejected_completions
CompletionRequest — session_id, file_content, cursor_offset, language, max_tokens
GenerationRequest — session_id, prompt, subject_context, language, lo_ids
ReviewResult      — file_path, findings[{line, category, severity, message, suggestion}]
DebugRequest      — session_id, error_message, stack_trace, relevant_code
```

All Phase 3 endpoints return **deterministic stub responses** (fixtures).

---

## Phase 4 — AI Intelligence Layer & Aku Code Editor Core Engine (Sprints 7–8)

**Goal:** Real AI inference flows through every service; Aku Code Editor learns from usage patterns.

### AkuAI (8004) — Code Inference Backend

- Second model: `CodeGemma-2B-GGUF` (or `StarCoder2-3B-Q4`) loaded from `CODE_MODEL_PATH`.
- Route `/api/v1/code/*` to code model; `/api/v1/text/generate` to general model.
- Model registry metadata: `version`, `sha256`, `training_provenance`, `resource_requirements`.
- Canary A/B routing: configurable `CODE_CANARY_PERCENT` env var directs % of requests to new model version.

### AkuTutor (8007) — Adaptive Personalisation

- Pull LO mastery scores from User Profile Service; select `response_mode` dynamically (mastery < 60% → `step_by_step`).
- "Next best practice" prompt: recommend next LO after each answer.
- Multilingual skeleton: accept `language` = `ha`/`ig`/`yo`; route to multilingual embedding model when available.
- Teacher feedback: `POST /api/v1/tutor/feedback` → update chunk trust scores in Akudemy.

### 🆕 Aku Code Editor — Learning Engine

**Session Memory (Redis DB 9, TTL 7 days):**
Each `CodeSession` stores: files edited, completions accepted/rejected, errors encountered, language/framework context.

**Learning from Corrections:**
When a user edits a generated completion, record `(original_completion, user_correction)` pair.  
Batch-export correction pairs to Aku-DaaS fine-tuning queue (`POST /api/v1/datasets/ingest`).

**Context-Aware Completions:**
Pass last 2 048 tokens of the current file + `session_context` to AkuAI `code/complete`.  
Sliding context window prioritizes recently edited lines.

**Curriculum-Aware Generation:**
When `subject_context` is provided, fetch related LO descriptions from Akudemy and inject into the generation prompt — ensuring pedagogically correct examples.

**Code Review Intelligence:**
Call AkuAI `/api/v1/code/review`; categorize findings into `style`, `logic`, `security`, `performance`; return structured `ReviewResult` with line references.

**Debug Assistant:**
Parse Python/JS stack traces; embed error message + relevant code lines; retrieve similar past error resolutions from a local FAISS debug-examples index.

**Streaming:**
All completion/generation endpoints support **Server-Sent Events (SSE)** and **WebSocket** (`/ws/code/stream`) for real-time token-by-token output.

### AIOps Baseline

- Prometheus + Grafana deployed under `monitoring` profile in `docker-compose.dev.yml`.
- SLOs defined for Tier-1 services (AkuAI, AkuTutor, Aku-EdgeHub, Aku-Code-Editor):
  - Availability: 99.9%
  - AkuTutor edge latency p95: ≤ 800 ms
  - Code Editor completion latency p95: ≤ 500 ms
- Grafana dashboards: per-service latency (p50/p95/p99), error rate, model inference time, cache hit rate.
- Alertmanager on-call routing configured.

---

## Phase 5 — Production Readiness, Security & Rollout (Sprints 9–10)

**Goal:** Platform is secure, observable, fully documented, and ready for pilot deployment.

### Security Hardening (All Services)

- All `dev_secret_*` / `CHANGE_ME` env vars replaced with external secrets manager references (Vault / AWS Secrets Manager). Dev uses env injection; staging/prod uses External Secrets Operator.
- CORS: `CORS_ORIGINS` restricted to approved frontend domains only (no wildcard in staging/prod).
- TLS: enforced at Nginx (`nginx.conf`) for all external-facing services. Internal cluster traffic uses mTLS in production.
- Field-level encryption on PII columns in Postgres schemas (`learner_id`, `email`, `phone`).
- Audit log PII masking: no raw names, emails, or phone numbers in log output.

### Aku Code Editor — Production Hardening

**Guardrails:**
- Harmful code classifier: block patterns matching known shell-injection / credential-exfiltration signatures.
- License compliance: AST heuristic scan on generated code; flag GPL-incompatible patterns for review.
- Rate limiting: per-user token budget (`CODE_EDITOR_TOKEN_BUDGET` env var, default 50 000 tokens/day).

**Edge Deployment:**
- Quantized code model (≤ 1.5 GB GGUF) packaged for Aku Edge Hub K3s deployment.
- When `OPERATING_MODE=offline`, route `code/complete` to local model.

**Telemetry:**
Track `completion_acceptance_rate`, `generation_success_rate`, `p95_latency_ms`, `sessions_active`, `tokens_generated_per_day` via Prometheus.

**Privacy:**
- No raw source code stored beyond session TTL (7 days).
- Correction pairs anonymized (user ID hashed) before export to fine-tuning queue.

**Teacher/Admin Controls:**
- Per-institution language/topic restrictions via admin policy API.
- Session summary report (no raw code) available to teachers.

### Infrastructure Production Transition

| Component | Dev | Production |
|-----------|-----|-----------|
| Postgres | Single DB, multi-schema | Per-service DB (isolation) |
| Redis | Standalone, `allkeys-lru` | Redis Cluster, `volatile-lru` for session keys |
| Neo4j | Single node | Neo4j Aura / self-hosted cluster + point-in-time recovery |
| Services | Docker Compose profiles | Kubernetes manifests (`docs/deployment/k8s/`) |

Kubernetes manifests for all 13 services (including Aku-Code-Editor) live in [`docs/deployment/k8s/`](../deployment/k8s/).

### Documentation & Runbooks

| Document | Location |
|----------|----------|
| Per-service runbooks | [`docs/runbooks/`](../runbooks/) |
| On-call playbook | [`docs/runbooks/on-call-playbook.md`](../runbooks/on-call-playbook.md) |
| Developer onboarding | [`docs/runbooks/developer-onboarding.md`](../runbooks/developer-onboarding.md) |
| Code Editor ADR | [`docs/adrs/adr-005-aku-code-editor.md`](../adrs/adr-005-aku-code-editor.md) |
| Code Editor handbook | [`docs/handbooks/AkuCodeEditor_Handbook.md`](../handbooks/AkuCodeEditor_Handbook.md) |

### Go/No-Go Criteria for Pilot

| Criterion | Target |
|-----------|--------|
| All core services pass integration tests in CI | ✅ Required |
| `infra + core` stack starts healthy in < 60 s on 6 GB machine | ✅ Required |
| AkuTutor RAG hit-rate@5 | ≥ 0.82 |
| AkuTutor edge latency p95 | ≤ 800 ms |
| Aku Code Editor completion acceptance rate (internal dogfooding) | ≥ 40% |
| Aku Code Editor completion latency p95 | ≤ 500 ms |
| CodeQL critical/high findings in any service | 0 |
| SLO dashboards live + alert routing tested | ✅ Required |

---

## Sprint Velocity Guide

| Phase | Sprints | Key Deliverable |
|-------|---------|----------------|
| 1 | 1–2 | All containers healthy; API stubs documented |
| 2 | 3–4 | Core services deliver real data end-to-end |
| 3 | 5–6 | Full-stack wired; Code Editor scaffold + API contract |
| 4 | 7–8 | Real AI inference; Code Editor learning engine live |
| 5 | 9–10 | Security hardened; pilot-ready; runbooks complete |

---

*For the Aku Code Editor strategy deep-dive see [`docs/strategy/aku-code-editor-strategy.md`](../strategy/aku-code-editor-strategy.md).*  
*For service-level API documentation see [`docs/api/aku-code-editor-openapi.yaml`](../api/aku-code-editor-openapi.yaml).*
