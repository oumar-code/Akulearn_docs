# Aku-EdgeHub

Offline edge server for the Akulearn platform. Stores content locally in **SQLite** via `aiosqlite` and operates in two modes:

| Mode | Behaviour |
|------|-----------|
| `online` | Syncs to Akudemy cloud; relays AI inference to AkuAI |
| `offline` | Fully local — no outbound calls attempted |

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│  Aku-EdgeHub  (FastAPI + SQLite/aiosqlite)       │
│                                                  │
│  /api/v1/health/offline   ← no external deps    │
│  /api/v1/sync/trigger     → Akudemy             │
│  /api/v1/cache/status     ← SQLite query        │
│  /api/v1/devices/register → SQLite write        │
│  /api/v1/devices/{id}     ← SQLite read         │
│  /api/v1/ai/infer         → AkuAI (Gemma)       │
└─────────────────────────────────────────────────┘
```

---

## Project layout

```
Aku-EdgeHub/
├── app/
│   ├── main.py                  # FastAPI app factory + lifespan
│   ├── core/
│   │   └── config.py            # Pydantic-settings (reads .env)
│   ├── db/
│   │   └── session_sqlite.py    # aiosqlite async engine + get_db dep
│   ├── routers/
│   │   ├── edge.py              # health, sync, cache, AI infer
│   │   └── devices.py           # device register + lookup
│   ├── schemas/
│   │   ├── edge.py              # Pydantic v2 edge models
│   │   └── devices.py           # Pydantic v2 device models
│   └── services/
│       └── sync.py              # httpx calls to Akudemy & AkuAI
├── requirements-extra.txt       # aiosqlite, httpx
├── .env.example                 # environment variable template
├── Dockerfile.offline           # multi-stage, non-root (uid 1001)
└── README.md
```

---

## Quick start

```bash
# 1. Install dependencies (merge with your base requirements.txt first)
pip install fastapi uvicorn[standard] pydantic-settings sqlalchemy \
    $(cat requirements-extra.txt | grep -v '#')

# 2. Configure environment
cp .env.example .env
$EDITOR .env          # set API keys, operating mode, etc.

# 3. Run
uvicorn app.main:app --reload --port 8000
```

Interactive API docs: <http://localhost:8000/docs>

---

## Docker (offline image)

```bash
# Build
docker build -f Dockerfile.offline -t aku-edgehub:offline .

# Run — mount a host volume so the SQLite DB survives container restarts
docker run -d \
  --name edgehub \
  -p 8000:8000 \
  -v edgehub-data:/data \
  --env-file .env \
  aku-edgehub:offline
```

The container runs as non-root user `aku` (uid 1001). The SQLite file is written to `/data/edge_hub.db` inside the container — mount a named volume or host path there.

---

## API reference

### `GET /api/v1/health/offline`
Offline-safe health check. Probes the local SQLite connection and returns current operating mode. No external calls.

### `POST /api/v1/sync/trigger`
Triggers a content sync job against Akudemy. Gracefully returns `accepted: false` when the hub is in offline mode or Akudemy is unreachable.

```json
{ "force": false, "scope": ["topic-123"] }
```

### `GET /api/v1/cache/status`
Returns the number of cached content items, the last sync timestamp, and the SQLite file size on disk.

### `POST /api/v1/devices/register`
Registers a device in the local SQLite store. Idempotent — re-registering an existing `device_id` updates `last_seen_at`.

```json
{
  "device_id": "rpi-abc123",
  "name": "Classroom Pi #1",
  "firmware_version": "1.2.0",
  "capabilities": ["video", "audio"],
  "metadata": { "location": "Block A" }
}
```

### `GET /api/v1/devices/{device_id}`
Returns the full device record from SQLite. Returns `404` if not found.

### `POST /api/v1/ai/infer`
Relays a small inference request to **AkuAI**'s `/api/v1/models/gemma/infer` endpoint. Returns `503` if AkuAI is unreachable (expected in fully offline mode).

```json
{ "prompt": "Explain photosynthesis simply.", "max_tokens": 256, "temperature": 0.7 }
```

---

## Configuration reference

| Variable | Default | Description |
|----------|---------|-------------|
| `OPERATING_MODE` | `online` | `online` or `offline` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./edge_hub.db` | SQLite connection string |
| `DB_ECHO` | `false` | Log all SQL statements |
| `AKUDEMY_BASE_URL` | — | Akudemy cloud base URL |
| `AKUDEMY_API_KEY` | — | API key for Akudemy |
| `SYNC_TIMEOUT_SECONDS` | `30` | httpx timeout for sync calls |
| `AKUAI_BASE_URL` | — | AkuAI service base URL |
| `AKUAI_API_KEY` | — | API key for AkuAI |
| `INFER_TIMEOUT_SECONDS` | `60` | httpx timeout for inference calls |

See `.env.example` for a complete annotated template.
