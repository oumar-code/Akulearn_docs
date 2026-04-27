# Postgres Per-Service Schema Definitions

> **Last updated:** April 2026  
> **Database:** `aku_platform` (single database, schema-per-service in dev)  
> **Migration tool:** Alembic (each service runs `alembic upgrade head` on startup)

---

## Overview

All services share a single Postgres database (`aku_platform`) in dev. Each service owns exactly one schema and uses `SET search_path = <schema>` to isolate its tables. This avoids running 4+ separate Postgres instances on a 6 GB developer machine.

In production, each service connects to its own dedicated database for full isolation. See [`dev-ram-allocation-decision.md`](./dev-ram-allocation-decision.md) for the rationale.

---

## Schema: `akuai`

**Owner service:** AkuAI (port 8004)  
**Redis DB:** 2

```sql
CREATE SCHEMA IF NOT EXISTS akuai;
SET search_path = akuai;

-- Model inference request/response audit log
CREATE TABLE IF NOT EXISTS inference_log (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trace_id    TEXT NOT NULL,
    model_name  TEXT NOT NULL,
    endpoint    TEXT NOT NULL,         -- e.g. '/api/v1/embeddings'
    input_hash  TEXT NOT NULL,         -- SHA-256 of input (no raw text stored)
    output_hash TEXT NOT NULL,         -- SHA-256 of output
    latency_ms  INTEGER NOT NULL,
    status_code INTEGER NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Model registry: tracks all deployed model versions
CREATE TABLE IF NOT EXISTS model_registry (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name       TEXT NOT NULL,
    version          TEXT NOT NULL,
    model_type       TEXT NOT NULL,    -- 'embedding' | 'text_generation' | 'code'
    file_path        TEXT,
    sha256           TEXT,
    training_provenance TEXT,
    resource_requirements JSONB,
    is_active        BOOLEAN NOT NULL DEFAULT FALSE,
    deployed_at      TIMESTAMPTZ,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (model_name, version)
);
```

---

## Schema: `akudemy`

**Owner service:** Akudemy (port 8005)  
**Redis DB:** 3

```sql
CREATE SCHEMA IF NOT EXISTS akudemy;
SET search_path = akudemy;

CREATE TABLE IF NOT EXISTS subjects (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code        TEXT NOT NULL UNIQUE,  -- e.g. 'PHY', 'MAT', 'ENG'
    name        TEXT NOT NULL,
    language    TEXT NOT NULL DEFAULT 'en',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS class_levels (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code        TEXT NOT NULL UNIQUE,  -- e.g. 'JSS1', 'SS3'
    label       TEXT NOT NULL,
    sort_order  INTEGER NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS learning_objectives (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lo_id           TEXT NOT NULL UNIQUE, -- e.g. 'LO:NERDC:PHY:SS2:WAV:001'
    subject_id      UUID NOT NULL REFERENCES subjects(id),
    class_level_id  UUID NOT NULL REFERENCES class_levels(id),
    topic           TEXT NOT NULL,
    description     TEXT NOT NULL,
    difficulty      TEXT NOT NULL DEFAULT 'medium',
    curriculum      TEXT NOT NULL DEFAULT 'NERDC',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS content_chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id        TEXT NOT NULL UNIQUE,
    lo_id           TEXT NOT NULL,
    subject_id      UUID REFERENCES subjects(id),
    class_level_id  UUID REFERENCES class_levels(id),
    topic           TEXT NOT NULL,
    language        TEXT NOT NULL DEFAULT 'en',
    content_text    TEXT NOT NULL,
    embedding_vec   BYTEA,              -- serialized 384-dim float32 FAISS vector
    asset_type      TEXT NOT NULL,      -- 'lesson' | 'past_question' | 'summary'
    trust_level     INTEGER NOT NULL DEFAULT 3,
    review_status   TEXT NOT NULL DEFAULT 'pending', -- 'pending' | 'teacher_approved' | 'rejected'
    reviewed_by     TEXT,
    reviewed_at     TIMESTAMPTZ,
    source_path     TEXT,
    version         TEXT NOT NULL DEFAULT '1.0',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS exam_papers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_board      TEXT NOT NULL,      -- 'WAEC' | 'NECO' | 'JAMB' | 'BECE'
    year            INTEGER NOT NULL,
    subject_id      UUID REFERENCES subjects(id),
    class_level_id  UUID REFERENCES class_levels(id),
    question_text   TEXT NOT NULL,
    answer_text     TEXT,
    lo_ids          TEXT[],             -- array of LO IDs this question covers
    marks           INTEGER,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index for freshness policy job
CREATE INDEX IF NOT EXISTS idx_chunks_updated ON content_chunks(updated_at);
CREATE INDEX IF NOT EXISTS idx_chunks_lo_id ON content_chunks(lo_id);
```

---

## Schema: `superhub`

**Owner service:** Aku-SuperHub (port 8009)  
**Redis DB:** 6

```sql
CREATE SCHEMA IF NOT EXISTS superhub;
SET search_path = superhub;

CREATE TABLE IF NOT EXISTS service_registry (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_name    TEXT NOT NULL UNIQUE,
    base_url        TEXT NOT NULL,
    health_path     TEXT NOT NULL DEFAULT '/health',
    last_health_at  TIMESTAMPTZ,
    is_healthy      BOOLEAN NOT NULL DEFAULT FALSE,
    registered_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS routing_policies (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_name     TEXT NOT NULL UNIQUE,
    source_service  TEXT NOT NULL,
    target_tier     TEXT NOT NULL,      -- 'edge' | 'superhub' | 'ighub' | 'cloud'
    priority        INTEGER NOT NULL DEFAULT 1,
    conditions      JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## Schema: `daas`

**Owner service:** Aku-DaaS (port 8012)  
**Redis DB:** 8

```sql
CREATE SCHEMA IF NOT EXISTS daas;
SET search_path = daas;

CREATE TABLE IF NOT EXISTS datasets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    description     TEXT,
    owner_id        TEXT NOT NULL,      -- hashed institution or user ID
    schema_def      JSONB,
    row_count       BIGINT DEFAULT 0,
    is_anonymized   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ingestion_jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id      UUID REFERENCES datasets(id),
    source_type     TEXT NOT NULL,      -- 'file' | 'api' | 'stream'
    status          TEXT NOT NULL DEFAULT 'queued', -- 'queued' | 'running' | 'completed' | 'failed'
    rows_ingested   BIGINT DEFAULT 0,
    error_message   TEXT,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS pipeline_status (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id          UUID REFERENCES ingestion_jobs(id),
    stage           TEXT NOT NULL,
    status          TEXT NOT NULL,
    details         JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS access_grants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id      UUID REFERENCES datasets(id),
    grantee_id      TEXT NOT NULL,      -- hashed user or service ID
    permissions     TEXT[] NOT NULL,    -- ['read'] | ['read', 'write']
    expires_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## Schema: `code_editor`

**Owner service:** Aku-Code-Editor (port 8013)  
**Redis DB:** 9

```sql
CREATE SCHEMA IF NOT EXISTS code_editor;
SET search_path = code_editor;

-- Persistent correction pairs for fine-tuning queue
CREATE TABLE IF NOT EXISTS correction_pairs (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id           TEXT NOT NULL,
    user_id_hash         TEXT NOT NULL,   -- hashed; no raw PII
    language             TEXT NOT NULL,
    original_completion  TEXT NOT NULL,
    user_correction      TEXT NOT NULL,
    subject_context      TEXT,
    lo_ids               TEXT[],
    exported_to_daas     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Anonymized session summaries (raw code never stored)
CREATE TABLE IF NOT EXISTS session_summaries (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id       TEXT NOT NULL UNIQUE,
    user_id_hash     TEXT NOT NULL,
    institution_id   TEXT,
    language         TEXT,
    framework        TEXT,
    total_completions  INTEGER DEFAULT 0,
    accepted_completions INTEGER DEFAULT 0,
    review_requests  INTEGER DEFAULT 0,
    debug_requests   INTEGER DEFAULT 0,
    started_at       TIMESTAMPTZ NOT NULL,
    ended_at         TIMESTAMPTZ,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_correction_pairs_unexported
    ON correction_pairs(created_at) WHERE exported_to_daas = FALSE;
```

---

## Migration Strategy

Each service runs Alembic (or a lightweight startup migration) on container start:

```python
# Typical FastAPI startup (lifespan event)
async def startup():
    await run_migrations()  # Alembic: alembic upgrade head
```

The migration scripts live in each service's repository under `alembic/versions/`. The shared `aku_platform` database is created by Postgres on first start (via `POSTGRES_DB=aku_platform` in compose).

**Schema creation order (if running raw SQL):**
1. Create schemas: `akuai`, `akudemy`, `superhub`, `daas`, `code_editor`
2. Run each service's `alembic upgrade head`
3. Run seed scripts for pilot data (ENG, MAT, BIO subjects + LO catalog)

---

## Production Migration Path

When migrating from single-DB/multi-schema (dev) to per-service DB (production):

1. Create one Postgres database per service: `aku_platform_akuai`, `aku_platform_akudemy`, etc.
2. Update `DATABASE_URL` secrets to point to the new DB.
3. Run `pg_dump --schema=<schema>` on dev DB → restore into dedicated production DB.
4. Validate with `alembic current` on each service before cutover.
5. Drop schemas from shared dev DB (optional cleanup).

See the production Kubernetes secrets template in [`docs/deployment/k8s/secrets.yaml`](../k8s/secrets.yaml).
