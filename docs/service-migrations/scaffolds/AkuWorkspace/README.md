# AkuWorkspace

> **AI-native productivity layer** — orchestrates AkuAI, Aku-DaaS, and Akudemy into cohesive, multi-step AI workflows.

---

## Overview

AkuWorkspace is the orchestration hub of the Akulearn platform. It exposes a clean FastAPI surface that lets clients define and execute *workflows* — ordered sequences of calls to downstream micro-services — without knowing the topology of the backend.

| Concern | Handled by |
|---|---|
| Natural-language understanding | AkuAI |
| Dataset access & querying | Aku-DaaS |
| Content & curriculum delivery | Akudemy |
| Per-user contextual memory | Redis |

---

## Architecture

```
Client
  │
  ▼
AkuWorkspace  (this service)
  ├── POST /api/v1/workflows          → define workflow
  ├── POST /api/v1/workflows/{id}/run → orchestrate steps
  ├── GET/POST /api/v1/context/{uid}  → Redis context store
  └── POST /api/v1/docs/generate      → direct AkuAI doc generation
        │
        ├──▶ AkuAI    /api/v1/text/generate  (NL → text)
        ├──▶ Aku-DaaS /api/v1/query          (NL → dataset)
        └──▶ Akudemy  /api/v1/content/search (NL → lessons)
```

---

## Workflow Types

| Type | Pipeline |
|---|---|
| `DATA_QUERY` | AkuAI NL parse → Aku-DaaS query |
| `DOC_GENERATION` | AkuAI text generation → optional Akudemy enrichment |
| `CONTENT_SEARCH` | AkuAI NL understanding → Akudemy catalogue search |
| `TUTORING_ASSIST` | Akudemy lesson lookup → AkuAI personalised explanation |

---

## Workflow Lifecycle

```
PENDING → RUNNING → COMPLETED
                  ↘ FAILED
```

---

## API Reference

### Workflows

#### `POST /api/v1/workflows`
Create a workflow definition.

```json
{
  "name": "Fetch sales report",
  "type": "DATA_QUERY",
  "steps": [
    {
      "name": "Parse intent",
      "service": "akuai",
      "endpoint": "/api/v1/nlp/parse",
      "payload": {}
    },
    {
      "name": "Query dataset",
      "service": "daas",
      "endpoint": "/api/v1/query",
      "payload": { "dataset": "sales_2024" }
    }
  ],
  "metadata": {}
}
```

**Response** `201 Created` → `WorkflowRead`

---

#### `POST /api/v1/workflows/{id}/run`
Execute a previously created workflow.

```json
{
  "input": {
    "query": "Total revenue by region for Q1"
  }
}
```

**Response** `200 OK` → `WorkflowRunResult`  
Each step's JSON response is merged into the context passed to the next step.

---

### Context

#### `GET /api/v1/context/{user_id}`
Retrieve all context entries for a user.  
Returns `{ "user_id": "...", "data": { ... }, "updated_at": "..." }`.

#### `POST /api/v1/context/{user_id}`
Upsert context entries.

```json
{
  "entries": [
    { "key": "last_topic", "value": "neural networks" },
    { "key": "skill_level", "value": "intermediate" }
  ]
}
```

Context is stored as a Redis hash at `context:{user_id}` with a 30-day TTL.

---

### Document Generation

#### `POST /api/v1/docs/generate`
Delegate to AkuAI `POST /api/v1/text/generate`.

```json
{
  "prompt": "Write a course introduction for Python beginners",
  "context": { "skill_level": "beginner" },
  "max_tokens": 512,
  "temperature": 0.7
}
```

**Response** `200 OK` → `DocGenerateResponse`

---

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt -r requirements-extra.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with real service URLs and Redis connection string
```

### 3. Run the service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

Interactive docs available at `http://localhost:8004/docs`.

---

## Project Structure

```
AkuWorkspace/
├── app/
│   ├── main.py                  # FastAPI app factory + lifespan
│   ├── config.py                # pydantic-settings config
│   ├── routers/
│   │   ├── workflows.py         # Workflow CRUD + /run
│   │   ├── context.py           # Per-user Redis context
│   │   └── docs_gen.py          # AI doc generation
│   ├── schemas/
│   │   └── workflows.py         # Pydantic v2 request/response models
│   └── services/
│       └── orchestrator.py      # Multi-service workflow orchestrator
├── requirements-extra.txt
├── .env.example
└── README.md
```

---

## Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `AKU_AI_URL` | `http://akuai:8001` | AkuAI service base URL |
| `AKU_DAAS_URL` | `http://aku-daas:8002` | Aku-DaaS service base URL |
| `AKUDEMY_URL` | `http://akudemy:8003` | Akudemy service base URL |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string |
| `HTTP_TIMEOUT` | `30.0` | Upstream HTTP timeout (seconds) |
| `LOG_LEVEL` | `info` | Uvicorn/app log level |
| `CORS_ORIGINS` | — | Comma-separated allowed origins |

---

## Development Notes

- **Orchestrator step context chaining** — each step's response JSON is shallow-merged into `accumulated_context` before the next step's payload is assembled. Design step payloads accordingly.
- **In-process workflow store** — the scaffold uses a plain `dict` on `app.state`. Replace with a PostgreSQL/SQLAlchemy model before production.
- **Redis TTL** — context hashes expire after 30 days of inactivity. Adjust `_CONTEXT_TTL_SECONDS` in `routers/context.py` as needed.
- **Auth** — add a JWT/API-key middleware layer before exposing endpoints publicly.
