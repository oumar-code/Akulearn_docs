# Aku-EdgeHub

> **Status:** Phase 1 Stub → Phase 2 Delta Sync + RAG  
> **Host port (dev):** 8006 · **Container port:** 8000  
> **Docker profile:** `core`  
> **Storage (dev):** SQLite (`/data/edge_hub.db`) · **Storage (prod):** Postgres  
> **Redis DB:** 4 (pending sync events queue, connectivity state)  
> **Related:** [`api/aku-edgehub-openapi.yaml`](../api/aku-edgehub-openapi.yaml) · [`deployment/local/docker-compose.dev.yml`](../deployment/local/docker-compose.dev.yml)

---

## Vision

Aku-EdgeHub is the **Tier 1 offline-first orchestrator** deployed at every school edge site (Raspberry Pi / J4125 mini-PC running K3s). It enables students and teachers to access AI-assisted learning **without internet connectivity** by:

1. Maintaining a local SQLite database of cached curriculum chunks and LO catalog.
2. Running a local **FAISS vector index** for semantic search over the cached chunks.
3. Synchronising delta content updates from Akudemy during connectivity windows.
4. Proxying inference requests to the local GGUF model when offline, or upstream to AkuAI when online.

---

## Architecture

```
Students / Teachers (local network)
        │
        ▼
Aku-EdgeHub (port 8006)
        │
        ├── SQLite (/data/edge_hub.db) ─── sync_state, cached_chunks,
        │                                   cached_lo_catalog, pending_events
        │
        ├── FAISS IndexFlatIP ────────────── ≤ 500 MB semantic search index
        │                                   built from cached_chunks embeddings
        │
        ├── Redis DB 4 ──────────────────── pending sync events queue,
        │                                   connectivity state flag
        │
        ├── Akudemy (8005) ───── GET /api/v1/curriculum/lo/{lo_id}
        │                        GET /api/v1/content/chunks  (delta sync)
        │
        └── AkuAI (8004) ──────  POST /api/v1/embeddings    (online mode only)
                                 POST /api/v1/text/generate  (online mode only)
```

In `OPERATING_MODE=offline`, the EdgeHub serves **all requests from local index only** with no upstream calls.

---

## SQLite Schema (Phase 1)

The EdgeHub uses SQLite in dev (async via `aiosqlite`). In staging/production it switches to Postgres.

```sql
-- Tracks last sync timestamp per content category
CREATE TABLE IF NOT EXISTS sync_state (
    id              TEXT PRIMARY KEY,         -- e.g. 'content_chunks' | 'lo_catalog'
    last_sync_at    DATETIME,
    last_etag       TEXT,                     -- HTTP ETag from Akudemy for conditional GETs
    sync_status     TEXT NOT NULL DEFAULT 'idle', -- 'idle' | 'syncing' | 'error'
    error_message   TEXT,
    updated_at      DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- Local cache of curriculum content chunks (mirrored from Akudemy)
CREATE TABLE IF NOT EXISTS cached_chunks (
    id              TEXT PRIMARY KEY,         -- mirrors Postgres chunk_id
    lo_id           TEXT NOT NULL,
    subject_code    TEXT NOT NULL,
    class_level     TEXT NOT NULL,
    topic           TEXT NOT NULL,
    language        TEXT NOT NULL DEFAULT 'en',
    content_text    TEXT NOT NULL,
    asset_type      TEXT NOT NULL,            -- 'lesson' | 'past_question' | 'summary'
    trust_level     INTEGER NOT NULL DEFAULT 3,
    faiss_index_id  INTEGER,                  -- row ID in the FAISS index (NULL until indexed)
    synced_at       DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    version         TEXT NOT NULL DEFAULT '1.0'
);

-- Compact lo_catalog snapshot (loaded into memory on startup)
CREATE TABLE IF NOT EXISTS cached_lo_catalog (
    lo_id           TEXT PRIMARY KEY,
    subject_code    TEXT NOT NULL,
    class_level     TEXT NOT NULL,
    topic           TEXT NOT NULL,
    description     TEXT NOT NULL,
    difficulty      TEXT NOT NULL DEFAULT 'medium',
    synced_at       DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- Outbound events buffered when upstream is unreachable
CREATE TABLE IF NOT EXISTS pending_events (
    id              TEXT PRIMARY KEY,         -- UUID
    event_type      TEXT NOT NULL,            -- 'learner_progress' | 'attendance' | 'feedback'
    payload         TEXT NOT NULL,            -- JSON blob
    target_service  TEXT NOT NULL,            -- 'akudemy' | 'superhub'
    retry_count     INTEGER NOT NULL DEFAULT 0,
    created_at      DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    last_attempted_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_chunks_lo_id    ON cached_chunks(lo_id);
CREATE INDEX IF NOT EXISTS idx_chunks_subject  ON cached_chunks(subject_code, class_level);
CREATE INDEX IF NOT EXISTS idx_events_pending  ON pending_events(retry_count, created_at);
```

---

## API Endpoints

See full OpenAPI spec: [`docs/api/aku-edgehub-openapi.yaml`](../api/aku-edgehub-openapi.yaml).

### Phase 1 — Stub Sync Agent

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/sync/request` | Trigger a manual sync request (stub: returns `{"status": "queued"}`) |
| `GET` | `/sync/status` | Returns current sync state for all categories |
| `GET` | `/health` | Liveness check |
| `GET` | `/ready` | Readiness — SQLite accessible, FAISS index built |
| `GET` | `/metrics` | Prometheus metrics |

### Phase 2 — Full Feature Set

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/edge/rag/query` | Two-layer RAG: curriculum filter → semantic search → top-k |
| `GET` | `/api/v1/edge/lo/{lo_id}` | Look up a cached LO by ID |
| `GET` | `/api/v1/edge/chunks` | List cached chunks (filterable by subject, class level, topic) |
| `POST` | `/api/v1/edge/events` | Buffer an outbound event for later sync to upstream |
| `GET` | `/api/v1/edge/events/pending` | List pending events and their retry counts |

---

## Data Models

### `SyncStatus`

```json
{
  "category": "content_chunks",
  "last_sync_at": "2026-04-27T18:00:00Z",
  "sync_status": "idle",
  "chunks_cached": 1420,
  "faiss_index_size": 1420
}
```

### `RAGQueryRequest` (Phase 2)

```json
{
  "question": "Explain how mitosis differs from meiosis",
  "subject_code": "BIO",
  "class_level": "SS2",
  "top_k": 5,
  "min_trust_level": 2
}
```

### `RAGQueryResponse` (Phase 2)

```json
{
  "results": [
    {
      "chunk_id": "chunk_001",
      "lo_id": "LO:NERDC:BIO:SS2:CDIV:002",
      "topic": "Cell Division",
      "content_text": "Mitosis produces two identical daughter cells...",
      "score": 0.91,
      "trust_level": 4
    }
  ],
  "retrieval_mode": "local_faiss",
  "latency_ms": 38
}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development` / `staging` / `production` |
| `LOG_LEVEL` | `info` | Log verbosity |
| `OPERATING_MODE` | `online` | `online` (use upstream services) / `offline` (local only) |
| `DATABASE_URL` | `sqlite+aiosqlite:////data/edge_hub.db` | DB connection string (SQLite in dev, Postgres in prod) |
| `REDIS_URL` | `redis://redis:6379/4` | Redis DB 4 connection |
| `AKUDEMY_BASE_URL` | — | Akudemy service URL for delta sync |
| `AKUAI_BASE_URL` | — | AkuAI service URL for embedding calls (online mode) |
| `AKUDEMY_API_KEY` | — | Service-to-service key for Akudemy calls |
| `AKUAI_API_KEY` | — | Service-to-service key for AkuAI calls |
| `FAISS_MAX_BYTES` | `524288000` | FAISS index size cap (500 MB) |
| `SYNC_INTERVAL_SECONDS` | `300` | How often the background sync agent polls Akudemy |
| `FAISS_TOP_K` | `10` | Default top-k results returned from FAISS search |

---

## Phase 2 — Delta Sync Agent

On each connectivity window (or manually via `POST /sync/request`):

1. Call `GET /api/v1/content/chunks?since=<last_sync_at>` on Akudemy.
2. Upsert new/updated chunks into `cached_chunks`.
3. For each new chunk without `faiss_index_id`:
   - Call `AkuAI POST /api/v1/embeddings` to get its embedding.
   - Add to FAISS `IndexFlatIP` index; record `faiss_index_id`.
4. Refresh `cached_lo_catalog` if ETag has changed.
5. Update `sync_state.last_sync_at`.
6. Enforce FAISS size cap: if index exceeds `FAISS_MAX_BYTES`, evict oldest/lowest-trust-level chunks.

### Two-Layer RAG Query

`POST /api/v1/edge/rag/query` executes:

1. **Curriculum filter:** `SELECT * FROM cached_chunks WHERE subject_code = ? AND class_level = ? AND trust_level >= ?`
2. **Semantic search:** embed the question via AkuAI (online) or a local stub vector (offline); search FAISS index restricted to filtered chunk IDs.
3. **Re-rank:** sort by `trust_level × recency_score × cosine_similarity`; return top-k.

---

## Observability

### Prometheus Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `edgehub_chunks_cached_total` | Gauge | Total cached chunks in SQLite |
| `edgehub_faiss_index_size_bytes` | Gauge | FAISS index size in bytes |
| `edgehub_sync_duration_seconds` | Histogram | Delta sync duration |
| `edgehub_rag_query_latency_seconds` | Histogram | RAG query latency |
| `edgehub_pending_events_total` | Gauge | Buffered outbound events awaiting sync |
| `edgehub_operating_mode` | Gauge | `1` = online, `0` = offline |

---

## Phase 1 Exit Criteria

- [ ] Service starts healthy in `infra + core` profile
- [ ] SQLite schema created on first startup (all 4 tables present)
- [ ] `GET /health` returns `200 OK`
- [ ] `GET /ready` returns `200 OK`
- [ ] `POST /sync/request` returns `{"status": "queued"}` (stub)
- [ ] `GET /sync/status` returns status for all sync categories
- [ ] Docker service-name resolution to `akudemy:8000` and `akuai:8000` confirmed
- [ ] Prometheus scrape target active at `aku-edgehub:8000/metrics`

## Phase 2 Exit Criteria

- [ ] Delta sync agent downloads updated chunks from Akudemy on connectivity event
- [ ] FAISS index builds successfully with `≤ 500 MB` cap enforced
- [ ] `POST /api/v1/edge/rag/query` returns ranked results in < 200 ms on dev hardware
- [ ] `OPERATING_MODE=offline` serves all requests from local index (no upstream calls)
- [ ] Outbound events buffer and retry correctly when upstream is unreachable
