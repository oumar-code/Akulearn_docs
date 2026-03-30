# Aku-Telhone — eSIM Provisioning & MVNO Connectivity Service

Aku-Telhone is the eSIM provisioning and MVNO connectivity service for the Akulearn platform. It manages the full eSIM profile lifecycle — from SM-DP+ provisioning through OTA network switching — and delegates device attestation to **Aku-IGHub**.

> **Migration note:** The prior Node.js stub contained generic telephony CRUD (calls, SMS). All such endpoints have been **removed**. This Python/FastAPI scaffold replaces them entirely with the eSIM provisioning domain described below.

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/esim/provision` | Provision a new eSIM profile → returns `iccid`, `activation_code`, `qr_code_url` |
| `GET` | `/api/v1/esim/{iccid}` | Get eSIM profile status (`PENDING` \| `ACTIVE` \| `SWITCHING` \| `DEACTIVATED`) |
| `PATCH` | `/api/v1/esim/{iccid}/switch-network` | OTA network switch (MVNO) — **202 Accepted**, background task |
| `DELETE` | `/api/v1/esim/{iccid}` | Deactivate eSIM profile |
| `POST` | `/api/v1/esim/{iccid}/ota-push` | Trigger direct OTA push — **202 Accepted**, background task |
| `POST` | `/api/v1/devices/{id}/attest` | Device attestation → proxies to Aku-IGHub |

---

## Quick Start

```bash
# 1. Copy environment config
cp .env.example .env
# Edit .env — set SMDP_API_KEY, OTA_PLATFORM_API_KEY, AKU_IGHUB_API_KEY, JWT_PUBLIC_KEY_PATH

# 2. Install dependencies
pip install -r requirements.txt -r requirements-extra.txt

# 3. Run (development)
uvicorn app.main:app --reload --port 8001
```

Interactive docs: http://localhost:8001/docs

---

## Project Layout

```
Aku-Telhone/
├── app/
│   ├── main.py                        # FastAPI app factory & router registration
│   ├── core/
│   │   └── config.py                  # Pydantic-settings config (reads .env)
│   ├── routers/
│   │   ├── esim.py                    # eSIM lifecycle endpoints
│   │   └── devices.py                 # Device attestation → Aku-IGHub proxy
│   ├── schemas/
│   │   └── esim.py                    # Pydantic v2 request/response models + ESIMStatus enum
│   └── services/
│       ├── esim.py                    # ESIMService — provisioning, status, deactivation
│       └── ota.py                     # OTAService — async background OTA push & network switch
├── requirements-extra.txt             # Telhone-specific extra deps
└── .env.example                       # Environment variable template
```

---

## eSIM Provisioning Flow

```
Client                    Aku-Telhone               SM-DP+              Device (LPA)
  │                            │                       │                      │
  │ POST /esim/provision        │                       │                      │
  │ ──────────────────────────► │                       │                      │
  │                            │── allocate profile ──► │                      │
  │                            │◄── iccid + AC$ ────── │                      │
  │ ◄── 201 { iccid,           │                       │                      │
  │          activation_code,  │                       │                      │
  │          qr_code_url }     │                       │                      │
  │                            │                       │                      │
  │                            │                       │◄── profile download ─ │
  │                            │                       │── profile data ──────► │
```

---

## OTA Background Tasks

`PATCH /{iccid}/switch-network` and `POST /{iccid}/ota-push` both return **HTTP 202 Accepted** immediately. The delivery is performed by `app/services/ota.py` running as an `asyncio.create_task()` background coroutine within the event loop.

Each task is assigned a `task_id` (`ota-<uuid4>`) returned in the response. Poll `GET /api/v1/esim/{iccid}` to confirm the operation completed (`ACTIVE` status).

In production, replace the in-process task registry and profile store in `ota.py` with Redis-backed persistence for durability across restarts.

---

## Device Attestation

`POST /api/v1/devices/{id}/attest` proxies the attestation token to **Aku-IGHub** at `AKU_IGHUB_URL/api/v1/devices/attest`. Configure `AKU_IGHUB_URL` and `AKU_IGHUB_API_KEY` in `.env`.

IGHub returns a trust level (`FULL | LIMITED | UNTRUSTED`) used to gate eSIM provisioning in production flows.

---

## ESIMStatus Lifecycle

```
  PENDING ──► ACTIVE ──► SWITCHING ──► ACTIVE
                │
                └──────────────────────────── DEACTIVATED (terminal)
```

| Status | Meaning |
|---|---|
| `PENDING` | Profile allocated; device has not yet downloaded it via LPA |
| `ACTIVE` | Profile downloaded and active on the device |
| `SWITCHING` | OTA network switch in progress |
| `DEACTIVATED` | Profile permanently deactivated (terminal state) |

---

## Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | Runtime environment |
| `JWT_ALGORITHM` | `RS256` | JWT verification algorithm |
| `JWT_PUBLIC_KEY_PATH` | `/secrets/jwt_public.pem` | PEM path for token verification |
| `SMDP_BASE_URL` | — | SM-DP+ server base URL |
| `SMDP_API_KEY` | `changeme` | SM-DP+ API key |
| `MVNO_OPERATOR_ID` | `akulearn-mvno` | Operator ID registered with MVNO |
| `QR_BASE_URL` | — | QR code image service base URL |
| `OTA_PLATFORM_URL` | — | MVNO OTA push platform endpoint |
| `OTA_PLATFORM_API_KEY` | `changeme` | OTA platform API key |
| `OTA_TIMEOUT_SECONDS` | `30` | OTA acknowledgment timeout |
| `AKU_IGHUB_URL` | — | Aku-IGHub service URL |
| `AKU_IGHUB_API_KEY` | `changeme` | Service-to-service key for IGHub |
| `IGHUB_TIMEOUT_SECONDS` | `10` | IGHub call timeout |
| `ALLOWED_ORIGINS` | — | Comma-separated CORS allowed origins |
| `RATE_LIMIT_PER_MINUTE` | `60` | API rate limit per client per minute |

---

## Migration Notes (Node.js → Python/FastAPI)

- **Generic telephony CRUD removed** — calls and SMS endpoints in the Node.js stub are not ported.
- Auth moves from Express middleware to FastAPI `Depends(get_current_user)` — injected per-router.
- `asyncio.create_task()` replaces Node.js worker threads / `setImmediate` for OTA background work.
- Pydantic v2 `ConfigDict` style is used throughout — no `class Config` blocks.
- All `httpx` calls use `async with` context managers; timeouts are enforced via `settings`.
