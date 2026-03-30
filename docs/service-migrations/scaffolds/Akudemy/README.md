# Akudemy — Content Delivery & Offline-Sync Service

Akudemy is the **offline-first content delivery** microservice of the Aku Platform.  
It serves learning content to Edge Hubs operating in low-connectivity environments and issues tamper-proof blockchain credentials via the Polygon network.

---

## Architecture Overview

```
Edge Hubs  ──GET /api/v1/content/sync──▶  Akudemy  ──▶  Redis (sync cache)
                                              │
Admin CMS  ──POST /api/v1/content──────────▶  │          PostgreSQL
                                              │
Learner App ──POST /api/v1/credentials/issue▶  │  ──▶  Polygon (web3.py)
```

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/content/sync` | **Offline sync** — returns items updated since `?since=<ISO-8601>`. Redis-cached (30 s TTL). Primary Edge Hub polling call. |
| `GET` | `/api/v1/content/{id}` | Fetch a single content item by UUID. |
| `POST` | `/api/v1/content` | Create or update a content item (admin only). |
| `GET` | `/api/v1/lessons` | Lesson catalogue. |
| `POST` | `/api/v1/credentials/issue` | Mint a blockchain credential on Polygon. Returns `202 Accepted` with a `tx_hash`. |
| `GET` | `/api/v1/credentials/{id}/verify` | Verify an issued credential on-chain. |

Interactive docs: `http://localhost:8000/docs`

---

## Project Layout

```
Akudemy/
├── app/
│   ├── routers/
│   │   ├── content.py          # Content & lesson endpoints
│   │   └── credentials.py      # Polygon credential endpoints
│   ├── schemas/
│   │   ├── content.py          # Pydantic v2 content models
│   │   └── credentials.py      # Pydantic v2 credential models
│   ├── services/
│   │   └── content.py          # Business logic + Redis cache layer
│   └── main.py                 # FastAPI app entry-point (see below)
├── .env.example
├── requirements-extra.txt      # Akudemy-specific deps (web3, redis[asyncio])
└── README.md
```

> **`app/main.py`** is not scaffolded here as it lives in the shared platform base.  
> Wire the routers as shown in the *Quick Start* section below.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt          # platform base
pip install -r requirements-extra.txt   # Akudemy extras (web3, redis[asyncio])
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set POLYGON_RPC_URL, POLYGON_PRIVATE_KEY, REDIS_URL, etc.
```

### 3. Register routers in `app/main.py`

```python
from fastapi import FastAPI
from app.routers.content import router as content_router
from app.routers.credentials import router as credentials_router

app = FastAPI(title="Akudemy")
app.include_router(content_router)
app.include_router(credentials_router)
```

### 4. Run

```bash
uvicorn app.main:app --reload --port 8000
```

---

## Offline Sync Design

Edge Hubs poll `GET /api/v1/content/sync?since=<last_sync_ts>` on a configurable interval (recommended: every 5 minutes when connected).

- **Redis cache** (30 s TTL) absorbs burst traffic from many hubs syncing simultaneously.  
- The response includes a `next_sync_token` (ISO-8601 timestamp) that the hub should persist and pass on the next poll.  
- `offline_available: true` items include `size_bytes` so hubs can pre-calculate storage requirements before downloading assets.

---

## Blockchain Credentials (Polygon)

Credentials are ERC-721/ERC-1155 tokens minted on Polygon.

1. `POST /api/v1/credentials/issue` — builds and signs the mint transaction via `web3.py`, broadcasts to the configured RPC endpoint, and returns a `202` with the `tx_hash`.
2. `GET /api/v1/credentials/{id}/verify` — fetches the transaction receipt and returns the on-chain verification status.

**Stub mode**: The `_issue_on_polygon` function in `app/routers/credentials.py` is currently a stub that returns a mock `tx_hash`. Replace it with the production `web3.py` implementation once the smart contract is deployed.

### Required env vars for Polygon

| Variable | Description |
|----------|-------------|
| `POLYGON_RPC_URL` | Alchemy / Infura / QuickNode HTTPS endpoint |
| `POLYGON_NETWORK` | `amoy` (testnet) or `polygon` (mainnet) |
| `POLYGON_PRIVATE_KEY` | Issuer wallet private key — **use a secrets manager in production** |
| `POLYGON_ISSUER_ADDRESS` | Corresponding public address |
| `CREDENTIAL_CONTRACT_ADDRESS` | Deployed credential NFT contract |

---

## Development Notes

- Python **3.11+** required.
- Schemas use **Pydantic v2** (`model_config = ConfigDict(...)` style).
- The in-memory stores in `app/services/content.py` and `app/routers/credentials.py` are **stubs** — replace with async SQLAlchemy / Supabase queries.
- Override the `get_redis` dependency in tests to inject a fake Redis client.
