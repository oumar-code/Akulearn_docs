# Aku-IGHub — Global API Gateway

Aku-IGHub is the system-wide API gateway for the Akulearn platform. It owns three critical domains:

| Domain | Responsibility |
|---|---|
| **Verifiable Credentials** | Issue and verify W3C VCs (learning achievements, skill badges, certificates) |
| **Aku Coin Clearing** | Idempotent financial settlement between platform wallets |
| **Anonymised Metadata** | PII-free event exchange forwarded to Aku-DaaS for analytics |
| **Compliance** | Cross-border regulatory policy checks (GDPR, NDPR, FERPA, PDPA, …) |

All endpoints are protected by JWT authentication — IGHub is the **auth boundary** for the entire Aku service mesh.

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/credentials/issue` | Issue a signed verifiable credential |
| `GET` | `/api/v1/credentials/{id}/verify` | Verify credential signature, expiry, revocation |
| `POST` | `/api/v1/clearing/settle` | Settle an Aku Coin transaction (**idempotent**) |
| `GET` | `/api/v1/clearing/{tx_id}` | Get clearing transaction status |
| `POST` | `/api/v1/metadata/publish` | Publish anonymised metadata → Aku-DaaS |
| `GET` | `/api/v1/metadata/{id}` | Retrieve a published metadata record |
| `POST` | `/api/v1/compliance/check` | Cross-border regulatory compliance check |

---

## Quick Start

```bash
# 1. Copy environment config
cp .env.example .env
# Edit .env — set JWT_PUBLIC_KEY_PATH, DAAS_INGEST_URL, REDIS_URL

# 2. Install dependencies
pip install -r requirements.txt -r requirements-extra.txt

# 3. Run (development)
uvicorn app.main:app --reload --port 8000
```

Interactive docs: http://localhost:8000/docs

---

## Project Layout

```
Aku-IGHub/
├── app/
│   ├── main.py                  # FastAPI app factory & router registration
│   ├── dependencies.py          # get_current_user JWT dependency
│   ├── core/
│   │   └── config.py            # Pydantic-settings config (reads .env)
│   ├── routers/
│   │   ├── credentials.py       # VC issue / verify
│   │   ├── clearing.py          # Aku Coin settlement (idempotent)
│   │   ├── metadata.py          # Anonymised metadata → DaaS
│   │   └── compliance.py        # Cross-border policy check
│   └── schemas/
│       ├── credentials.py       # CredentialIssueRequest/Response, CredentialVerifyResponse
│       ├── clearing.py          # ClearingStatus, ClearingSettleRequest/Response
│       └── metadata.py          # MetadataPublishRequest/Response, MetadataRecord
├── requirements-extra.txt       # IGHub-specific extra deps (JWT, Redis, httpx, …)
└── .env.example                 # Environment variable template
```

---

## Idempotency (Clearing)

`POST /api/v1/clearing/settle` **requires** an `Idempotency-Key` header:

```http
POST /api/v1/clearing/settle
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "from_wallet": "did:web:wallet.alice.example",
  "to_wallet":   "did:web:wallet.bob.example",
  "amount":      "10.00",
  "currency":    "AKU"
}
```

- **HTTP 201** — new transaction accepted and settled.
- **HTTP 200** — duplicate key detected; original response replayed (no double-debit).

In production, back the idempotency store with Redis (`REDIS_URL`) and set `IDEMPOTENCY_TTL_SECONDS` (default 24 h).

---

## JWT Authentication

IGHub validates bearer tokens at the gateway boundary so downstream services can trust the forwarded identity. Configure:

```
JWT_ALGORITHM=RS256
JWT_PUBLIC_KEY_PATH=/secrets/jwt_public.pem
```

The `get_current_user` dependency (in `app/dependencies.py`) is injected into every router. It decodes the token, verifies the signature, and exposes the claims dict to route handlers.

---

## Metadata & PII Policy

`POST /api/v1/metadata/publish` enforces a schema-level PII guard. Payloads containing keys named `name`, `email`, `phone`, `dob`, `ssn`, `passport`, or `address` are rejected with HTTP 422. Strip all PII before publishing.

Published records are forwarded to Aku-DaaS at `DAAS_INGEST_URL`. If DaaS is unreachable, the record is still persisted locally and `daas_ingested: false` is returned.

---

## Compliance Check

`POST /api/v1/compliance/check` evaluates a cross-border data operation against auto-detected regulatory frameworks:

```json
{
  "operation": "credential.share",
  "source_jurisdiction": "NG",
  "target_jurisdiction": "DE",
  "context": { "data_category": "education_records" }
}
```

Frameworks are inferred from jurisdictions (GDPR for EU, NDPR for Nigeria, FERPA/COPPA for US, etc.) or supplied explicitly via `applicable_policies`. A production integration should replace the stub logic with an OPA or Cedar policy sidecar.

---

## Migration Notes (Node.js → Python/FastAPI)

The existing Node.js stub exposed generic gateway routes. All such routes **must be removed** and replaced with the domain routes above. Key differences:

- Auth moves from Express middleware to FastAPI's `Depends(get_current_user)` — injected per-router, not globally, so each domain's auth requirement is explicit and auditable.
- Idempotency is enforced at the FastAPI layer using `Header()` — not Express body parsing.
- Pydantic v2 validates and documents every request/response shape automatically.
