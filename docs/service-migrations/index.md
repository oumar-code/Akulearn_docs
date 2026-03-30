# Service Migration Index

Priority-ordered tracker for migrating all 9 Aku Platform backend services from Node.js stubs to **Python 3.11 / FastAPI**.

> **Source of truth:** [`docs/ecosystem-map.md`](../ecosystem-map.md)  
> **Bootstrap script:** [`docs/service-migrations/bootstrap.sh`](bootstrap.sh)  
> **Full playbook:** [`docs/service-templates/python-fastapi-bootstrap.md`](../service-templates/python-fastapi-bootstrap.md)

---

## How to Apply a Migration

```bash
# 1. Clone the target service repo alongside this docs repo
cd ..
git clone https://github.com/oumar-code/<service-name>
cd <service-name>

# 2. Copy the bootstrap script from Akulearn_docs
cp ../Akulearn_docs/docs/service-migrations/bootstrap.sh .

# 3. Run it — this scaffolds the full Python/FastAPI project structure
chmod +x bootstrap.sh
./bootstrap.sh <service-name>

# 4. Apply service-specific domain endpoints (see per-service notes below)
# 5. Commit and open a PR in the service repo
git checkout -b feat/python-fastapi-migration
git add .
git commit -m "feat: migrate to Python 3.11 / FastAPI"
git push origin feat/python-fastapi-migration
```

---

## Migration Priority & Status

| Priority | Repo | Tier / Role | Domain Realignment Needed | Status |
|----------|------|-------------|--------------------------|--------|
| 1 | [AkuAI](https://github.com/oumar-code/AkuAI) | Core — shared inference layer | No | ⬜ Pending |
| 2 | [Akudemy](https://github.com/oumar-code/Akudemy) | Core — content delivery, offline sync | No | ⬜ Pending |
| 3 | [Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub) | Tier 1 — offline edge server, local AI | No | ⬜ Pending |
| 4a | [Aku-IGHub](https://github.com/oumar-code/Aku-IGHub) | Tier 3 — global gateway, Aku Coin | **Yes** — stub has generic gateway routes | ⬜ Pending |
| 4b | [Aku-Telhone](https://github.com/oumar-code/Aku-Telhone) | Core — eSIM provisioning | **Yes** — stub has generic telephony CRUD | ⬜ Pending |
| 5a | [Aku-SuperHub](https://github.com/oumar-code/Aku-SuperHub) | Tier 2 — regional analytics | No | ⬜ Pending |
| 5b | [AkuTutor](https://github.com/oumar-code/AkuTutor) | Core — AI Tutor (calls AkuAI) | No | ⬜ Pending |
| 5c | [AkuWorkspace](https://github.com/oumar-code/AkuWorkspace) | Core — AI productivity suite | No | ⬜ Pending |
| 5d | [Aku-DaaS](https://github.com/oumar-code/Aku-DaaS) | Core — data governance pipelines | **Yes** — stub has "device management" routes | ⬜ Pending |

---

## Priority 1 — AkuAI

**Why first:** every other AI-consuming service (AkuTutor, AkuWorkspace, Akudemy) depends on AkuAI's inference API. Migrating it first unblocks all downstream work.

### Domain Endpoints to Implement

```
POST  /api/v1/inference          # generic inference (model, prompt, params)
POST  /api/v1/text/generate      # LLM text generation
POST  /api/v1/text/classify      # text classification
POST  /api/v1/text/summarize     # summarisation
POST  /api/v1/embeddings         # vector embeddings for semantic search
GET   /api/v1/models             # list available models
POST  /api/v1/models/gemma/infer # Gemma local inference relay for Edge Hubs
```

### Key implementation notes
- Uses `torch`, `transformers`, `llama-cpp-python` — add to `requirements.txt`
- `POST /api/v1/models/gemma/infer` is called by Aku-EdgeHub containers; keep payload small (< 4 KB)
- All other services call AkuAI via `settings.aku_ai_url` — they do NOT bundle their own models
- See `docs/ai_tutor.md` and `docs/ml_training_pipeline.md` for the full inference spec

---

## Priority 2 — Akudemy

### Domain Endpoints to Implement

```
GET   /api/v1/content/sync       # offline content sync (called by Edge Hubs) — ?since=<ISO timestamp>
GET   /api/v1/content/{id}       # single content item
POST  /api/v1/content            # create/update content item (admin)
GET   /api/v1/lessons            # lesson catalogue
POST  /api/v1/credentials/issue  # blockchain credential issuance → Polygon
GET   /api/v1/credentials/{id}/verify
```

### Key implementation notes
- `GET /api/v1/content/sync` is the most latency-sensitive call — add a Redis cache layer
- Credential issuance calls Polygon via the PolygonService from `docs/tech_stack.md`
- Add `web3.py` to `requirements.txt` for Polygon integration
- See `docs/services/aku-learn.md` for the complete spec

---

## Priority 3 — Aku-EdgeHub

### Domain Endpoints to Implement

```
GET   /api/v1/health/offline     # offline health check (no external calls)
POST  /api/v1/sync/trigger       # push sync request to cloud (Akudemy)
GET   /api/v1/cache/status       # local SQLite content cache status
POST  /api/v1/devices/register   # device registration
GET   /api/v1/devices/{id}       # device lookup
POST  /api/v1/ai/infer           # local AI inference relay → Gemma
```

### Key implementation notes
- Uses **SQLite** (`aiosqlite`) for offline local store — swap `asyncpg` for `aiosqlite` in offline container
- Has two modes: online (sync to cloud) and offline (fully local)
- The `Dockerfile` needs two targets: `online` (PostgreSQL) and `offline` (SQLite)
- See `docs/01-architecture/index.md` and `docs/components/aku-edge-hub.md`

---

## Priority 4a — Aku-IGHub ⚠️ Domain Realignment Required

The existing Node.js/TypeScript stub has generic API gateway routes. These must be **completely replaced**.

### Domain Endpoints to Implement

```
POST  /api/v1/credentials/issue        # issue verifiable credential
GET   /api/v1/credentials/{id}/verify  # verify credential
POST  /api/v1/clearing/settle          # Aku Coin financial clearing
GET   /api/v1/clearing/{tx_id}         # clearing transaction status
POST  /api/v1/metadata/publish         # anonymised metadata exchange (→ Aku-DaaS)
GET   /api/v1/metadata/{id}            # retrieve published metadata
POST  /api/v1/compliance/check         # cross-border policy/compliance check
```

### Key implementation notes
- Acts as the global API gateway — all Tier 1 & 2 hub traffic routes through it
- JWT validation here is the system-wide auth boundary
- `POST /api/v1/clearing/settle` must be idempotent (add `Idempotency-Key` header check)
- See `docs/components/aku-ig-hub.md`

---

## Priority 4b — Aku-Telhone ⚠️ Domain Realignment Required

The existing stub has generic telephony (calls/SMS) CRUD. These must be **completely removed and replaced** with eSIM provisioning.

### Domain Endpoints to Implement

```
POST  /api/v1/esim/provision            # provision a new eSIM profile
GET   /api/v1/esim/{iccid}              # get eSIM profile status
PATCH /api/v1/esim/{iccid}/switch-network  # OTA network switching (MVNO)
DELETE /api/v1/esim/{iccid}             # deactivate eSIM
POST  /api/v1/esim/{iccid}/ota-push     # trigger OTA push (background task)
POST  /api/v1/devices/{id}/attest       # device attestation → Aku-IGHub
```

### Key implementation notes
- OTA push is a long-running operation — implement as `asyncio.create_task` background job
- Device attestation calls `Aku-IGHub` via `settings.aku_ighub_url`
- See `docs/services/aku-esim.md` and `docs/handbooks/eSIM_Provisioning_Handbook.md`

---

## Priority 5a — Aku-SuperHub

```
GET   /api/v1/fleet                     # list all Edge Hub devices in region
GET   /api/v1/fleet/{hub_id}/health     # per-hub health status
POST  /api/v1/analytics/aggregate       # ingest analytics from Edge Hubs
GET   /api/v1/analytics/summary         # regional analytics summary
POST  /api/v1/models/finetune           # trigger regional model fine-tuning job
```

---

## Priority 5b — AkuTutor

```
POST  /api/v1/sessions              # start a new tutoring session
GET   /api/v1/sessions/{id}         # get session history
POST  /api/v1/sessions/{id}/ask     # submit a question → calls AkuAI
POST  /api/v1/sessions/{id}/hint    # request a hint → calls AkuAI
POST  /api/v1/feedback              # learner feedback on session
```

- Consumes `settings.aku_ai_url` — does NOT run its own model
- See `docs/ai_tutor.md`

---

## Priority 5c — AkuWorkspace

```
POST  /api/v1/workflows             # create a new AI workflow
POST  /api/v1/workflows/{id}/run    # execute workflow → orchestrates AkuAI + Akudemy + Aku-DaaS
GET   /api/v1/context/{user_id}     # retrieve contextual memory for user
POST  /api/v1/context/{user_id}     # save context update
POST  /api/v1/docs/generate         # AI-assisted document generation
```

- See `docs/services/aku-workspace.md`

---

## Priority 5d — Aku-DaaS ⚠️ Domain Realignment Required

The existing stub has "device management" routes. These must be **completely replaced** with data governance endpoints.

```
POST  /api/v1/datasets/ingest       # ingest raw dataset
GET   /api/v1/datasets/{id}/status  # anonymisation pipeline status
POST  /api/v1/datasets/{id}/anonymise  # trigger anonymisation
POST  /api/v1/metadata/publish      # publish anonymised metadata → Aku-IGHub
GET   /api/v1/consent/{user_id}     # get user consent record
POST  /api/v1/consent/{user_id}     # update consent
```

- See `docs/services/aku-daas.md`

---

## After Migration: Update This Repo

When a service migration PR is merged, update the status in this table AND in [`automation_progress.md`](../../automation_progress.md) from ⬜ Pending to ✅ Done.
