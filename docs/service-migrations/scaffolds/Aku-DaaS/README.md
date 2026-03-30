# Aku-DaaS — Data-as-a-Service

Aku-DaaS is the data governance service for the Akulearn platform. It owns four critical responsibilities:

| Domain | Responsibility |
|---|---|
| **Dataset Ingestion** | Accept raw datasets via multipart upload or JSON body; store in PENDING → INGESTED state |
| **Anonymisation Pipelines** | k-anonymity pipeline run as async background tasks; status tracked per-dataset |
| **IG-Hub Metadata Publishing** | Forward anonymised dataset summaries to Aku-IGHub for platform-wide distribution |
| **Consent Management** | Per-user consent records with granular purpose control and jurisdiction tagging |

> **Migration note:** The existing Node.js stub exposed generic "device management" routes.  
> All device-management routes are **completely replaced** by the domain routes below.

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/datasets/ingest` | Ingest raw dataset (multipart file **or** JSON body) |
| `GET` | `/api/v1/datasets/{id}/status` | Poll anonymisation pipeline status |
| `POST` | `/api/v1/datasets/{id}/anonymise` | Trigger k-anonymity pipeline (async, returns 202) |
| `POST` | `/api/v1/metadata/publish` | Publish anonymised summary → Aku-IGHub |
| `GET` | `/api/v1/consent/{user_id}` | Retrieve user consent record |
| `POST` | `/api/v1/consent/{user_id}` | Create or update user consent record |

---

## Quick Start

```bash
# 1. Copy environment config
cp .env.example .env
# Edit .env — set DATABASE_URL, IGHUB_METADATA_PUBLISH_URL, REDIS_URL

# 2. Install dependencies
pip install -r requirements.txt -r requirements-extra.txt

# 3. Run (development)
uvicorn app.main:app --reload --port 8001
```

Interactive docs: http://localhost:8001/docs

---

## Project Layout

```
Aku-DaaS/
├── app/
│   ├── main.py                      # FastAPI app factory & router registration
│   ├── dependencies.py              # Shared FastAPI dependencies (auth, DB session)
│   ├── core/
│   │   └── config.py                # Pydantic-settings config (reads .env)
│   ├── routers/
│   │   ├── datasets.py              # Ingest, status, anonymise trigger
│   │   ├── metadata.py              # Publish anonymised metadata → IGHub
│   │   └── consent.py               # User consent CRUD
│   ├── schemas/
│   │   ├── datasets.py              # DatasetStatus, IngestRequest/Response, AnonymiseRequest
│   │   └── consent.py               # ConsentPurpose, ConsentRecord, ConsentUpsertRequest
│   └── services/
│       └── anonymisation.py         # AnonymisationService (k-anonymity pipeline)
├── requirements-extra.txt           # DaaS-specific extra deps (httpx, pandas, faker, …)
└── .env.example                     # Environment variable template
```

---

## Dataset Lifecycle

```
PENDING → INGESTED → ANONYMISING → ANONYMISED → PUBLISHED
                          ↓
                        FAILED  (re-triggerable from FAILED)
```

1. `POST /ingest` → status set to `INGESTED`
2. `POST /{id}/anonymise` → status set to `ANONYMISING`; pipeline runs in background
3. Pipeline completes → `ANONYMISED`; failure → `FAILED` with `error_detail`
4. `POST /metadata/publish` → status set to `PUBLISHED` after IGHub acknowledges

---

## Anonymisation Pipeline

The pipeline (`app/services/anonymisation.py`) is an async background task launched via `asyncio.create_task()`. Current steps are **stubs** (simulated with `asyncio.sleep`). Replace each step with real implementations:

| Step | Stub | Production |
|---|---|---|
| `_step_validate_schema` | pass | pandera / jsonschema |
| `_step_load_data` | sleep | `pd.read_parquet(s3://…)` |
| `_step_strip_direct_identifiers` | sleep | `df.drop(columns=PII_COLS)` |
| `_step_apply_k_anonymity` | sleep | anonympy / pycanon / custom |
| `_step_suppress_outliers` | fixed 2% rate | real suppression rate check |
| `_step_persist_result` | sleep | `df.to_parquet(s3://…)` |

Configure k-anonymity defaults via `DEFAULT_K_VALUE` and `DEFAULT_SUPPRESS_THRESHOLD` in `.env`.

---

## Consent Management

`POST /api/v1/consent/{user_id}` enforces withdrawal semantics: setting `consent_given: false` automatically clears `consent_for` regardless of submitted values — a withdrawal is total.

Supported purposes (`ConsentPurpose` enum):
- `analytics`, `research`, `personalisation`, `third_party_sharing`, `marketing`, `service_improvement`

Jurisdiction codes follow ISO 3166-1 alpha-2 (e.g. `NG`, `GB`, `DE`, `US`).

---

## Metadata Publishing

`POST /api/v1/metadata/publish` forwards the anonymised dataset summary to Aku-IGHub at `IGHUB_METADATA_PUBLISH_URL`. If IGHub is unreachable:
- The publish event is still logged locally.
- `ighub_acknowledged: false` is returned — the caller can retry.

Configure `IGHUB_METADATA_PUBLISH_URL` and `IGHUB_SERVICE_TOKEN` in `.env`.

---

## Migration Notes (Node.js → Python/FastAPI)

The existing Node.js stub exposed `/api/devices` and related "device management" routes. These **do not belong in Aku-DaaS** and have been fully replaced. Key architectural differences:

- Background jobs use `asyncio.create_task()` — no Bull/BullMQ or worker threads needed.
- Pydantic v2 validates every request/response shape and auto-generates OpenAPI docs.
- The `DatasetStatus` enum is the single source of truth for pipeline state — no ad-hoc string comparisons.
- Consent withdrawal semantics are enforced at the service layer, not left to the caller.
