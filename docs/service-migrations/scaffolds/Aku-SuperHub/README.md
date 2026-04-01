# Aku-SuperHub

Regional analytics hub that manages a fleet of Edge Hub devices, aggregates
learner analytics, and triggers model fine-tuning jobs.

---

## Responsibilities

| Concern | Description |
|---------|-------------|
| **Fleet management** | Register, monitor, and surface health of Edge Hub devices in a region |
| **Analytics aggregation** | Accept batched analytics events from Edge Hubs and expose regional summaries |
| **Model fine-tuning** | Enqueue and supervise regional model fine-tuning jobs |

---

## API surface

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/fleet` | List all Edge Hub devices (paginated) |
| `GET` | `/api/v1/fleet/{hub_id}/health` | Per-hub health status & telemetry |
| `POST` | `/api/v1/analytics/aggregate` | Ingest analytics batch from Edge Hubs |
| `GET` | `/api/v1/analytics/summary` | Regional analytics summary |
| `POST` | `/api/v1/models/finetune` | Trigger regional model fine-tuning job |

Interactive docs are available at `/docs` (Swagger UI) and `/redoc` once the
service is running.

---

## Project structure

```
Aku-SuperHub/
├── app/
│   ├── routers/
│   │   ├── fleet.py        # Fleet management endpoints
│   │   ├── analytics.py    # Analytics ingest & summary endpoints
│   │   └── models.py       # Model fine-tuning endpoints + job schemas
│   └── schemas/
│       ├── fleet.py        # EdgeHub, HubStatus, HubHealthMetrics, …
│       └── analytics.py    # AnalyticsEvent, AnalyticsBatch, RegionalSummary, …
├── .env.example            # Environment variable template
├── requirements-extra.txt  # Service-specific Python dependencies
└── README.md
```

---

## Getting started

### 1. Install dependencies

```bash
pip install -r requirements-extra.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set DATABASE_URL, REDIS_URL, JWT_SECRET_KEY, etc.
```

### 3. Run database migrations

```bash
alembic upgrade head
```

### 4. Start the service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Key design decisions

### Pydantic v2

All schemas use `model_config = ConfigDict(...)` — the v2 style.  
`frozen=True` is applied to response/value-object models to enforce immutability
after construction.

### Async-first

All route handlers are `async def`.  Database and cache interactions must use
async drivers (`asyncpg`, `redis[hiredis]`).

### Fine-tuning — 202 Accepted + background task

`POST /api/v1/models/finetune` returns **202 Accepted** immediately.  The job is
launched via `asyncio.create_task(...)` so the HTTP response is not blocked.
Replace `_run_finetune_job` in `app/routers/models.py` with a real call to your
ML pipeline (e.g., submit to Ray, Kubeflow, or a job queue).

### Analytics batch ingest

`POST /api/v1/analytics/aggregate` accepts up to **1 000 events** per request.
Duplicate events (matched on `event_id`) are silently skipped to support
idempotent retries from Edge Hubs.

### Enums

| Enum | Values |
|------|--------|
| `HubStatus` | `ONLINE`, `OFFLINE`, `DEGRADED`, `MAINTENANCE` |
| `FineTuneStatus` | `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED` |
| `EventType` | `SESSION_START`, `SESSION_END`, `CONTENT_VIEW`, `ASSESSMENT_SUBMIT`, `MODEL_INFERENCE` |

---

## Stub replacement checklist

Before wiring up to a real data store, replace the following stubs:

- [ ] `app/routers/fleet.py` → `_get_all_hubs`, `_get_hub_by_id`, `_get_hub_metrics`
- [ ] `app/routers/analytics.py` → `_batch_upsert_events`, `_compute_regional_summary`
- [ ] `app/routers/models.py` → `_run_finetune_job`

---

## Environment variables

See [`.env.example`](.env.example) for a fully documented list of all
configuration options.
