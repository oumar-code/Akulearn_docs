# aku-platform-contracts — Structural Recommendation

> **Status:** Proposed — implement once all 9 services complete Python/FastAPI migration  
> **Owner:** Platform Architecture  
> **Tracking:** [`automation_progress.md`](../automation_progress.md)

---

## Problem: API Contract Duplication Across 9 Repos

As the 9 backend services migrate to Python/FastAPI, each will define:
- Pydantic request/response schemas (e.g. `InferenceRequest`, `ContentItem`, `CredentialRecord`)
- OpenAPI YAML specs for their published endpoints
- Kafka event schemas (e.g. `content.sync.requested`, `credential.issued`)

Without a shared contracts library, the same types will be **duplicated or diverge** across consuming repos. For example:

| Schema | Defined in... | Consumed by... |
|--------|--------------|----------------|
| `InferenceRequest` | AkuAI | AkuTutor, AkuWorkspace, Akudemy, Aku-EdgeHub |
| `CredentialRecord` | Aku-IGHub | Akudemy, Aku-Telhone |
| `ContentItem` | Akudemy | Aku-EdgeHub, AkuWorkspace |
| `DatasetMetadata` | Aku-DaaS | Aku-IGHub, AkuWorkspace |

Without a contracts repo, a field rename in `InferenceRequest` requires changes in **5 repos**. With diverged copies, subtle type mismatches cause runtime errors that are hard to trace.

---

## Proposed Solution: `oumar-code/aku-platform-contracts`

A single lightweight Python package, published on GitHub Packages (or PyPI private), that every service installs as a dependency:

```bash
pip install aku-platform-contracts
```

### Package Structure

```
aku-platform-contracts/
├── aku_contracts/
│   ├── __init__.py
│   ├── inference/
│   │   ├── __init__.py
│   │   └── schemas.py        # InferenceRequest, InferenceResponse, ModelInfo
│   ├── content/
│   │   ├── __init__.py
│   │   └── schemas.py        # ContentItem, LessonSummary, SyncPayload
│   ├── credentials/
│   │   ├── __init__.py
│   │   └── schemas.py        # CredentialRecord, IssuanceRequest, VerifyResult
│   ├── clearing/
│   │   ├── __init__.py
│   │   └── schemas.py        # ClearingTransaction, SettlementRequest
│   ├── esim/
│   │   ├── __init__.py
│   │   └── schemas.py        # ESIMProfile, ProvisionRequest, NetworkSwitch
│   ├── datasets/
│   │   ├── __init__.py
│   │   └── schemas.py        # DatasetMetadata, IngestionRequest, ConsentRecord
│   ├── events/
│   │   ├── __init__.py
│   │   └── kafka_topics.py   # All Kafka topic name constants
│   └── openapi/
│       ├── aku-ai.yaml
│       ├── akudemy.yaml
│       ├── aku-ighub.yaml
│       └── ...               # One OpenAPI YAML per service
├── pyproject.toml
├── README.md
└── .github/
    └── workflows/
        └── publish.yml       # Publish to GitHub Packages on tag push
```

### Example: `aku_contracts/inference/schemas.py`

```python
from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    model: str = Field(..., description="Model identifier, e.g. 'gemma-2b'")
    prompt: str = Field(..., max_length=8192)
    max_tokens: int = Field(256, ge=1, le=4096)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    stream: bool = False


class InferenceResponse(BaseModel):
    model: str
    generated_text: str
    tokens_used: int
    latency_ms: float
```

### How Services Use It

In `AkuTutor/requirements.txt`:
```
aku-platform-contracts @ git+https://github.com/oumar-code/aku-platform-contracts.git@v0.1.1
```

In `AkuTutor/app/routers/sessions.py`:
```python
from aku_contracts.inference.schemas import InferenceRequest, InferenceResponse

@router.post("/sessions/{id}/ask")
async def ask(session_id: str, body: InferenceRequest) -> InferenceResponse:
    ...
```

---

## Benefits

| Benefit | Detail |
|---------|--------|
| **Single source of truth for types** | Change a field in one place; all consumers get it via semver update |
| **Auto-generated OpenAPI docs** | FastAPI reads Pydantic schemas directly — contracts repo is the API spec |
| **Kafka topic name constants** | No more hardcoded topic strings scattered across repos |
| **Breaking change detection** | Semver in CI: bump major for breaking changes, minor for additions |
| **No runtime surprises** | Consumers pin a contracts version; incompatible changes fail at import time |

---

## Implementation Checklist

- [ ] Create `oumar-code/aku-platform-contracts` repository
- [ ] Scaffold `aku_contracts/` package with `pyproject.toml` and `__init__.py`
- [ ] Define initial Pydantic schemas for: `inference`, `content`, `credentials`
- [ ] Define Kafka topic name constants in `aku_contracts/events/kafka_topics.py`
- [ ] Add `publish.yml` GitHub Actions workflow (build + publish to GitHub Packages on tag)
- [ ] Tag `v0.1.0` release
- [ ] Update `AkuAI/requirements.txt` to depend on `aku-platform-contracts`
- [ ] Update each consuming service's `requirements.txt` as it completes migration
- [ ] Add `aku-platform-contracts` to this ecosystem map

---

## When to Create This Repo

**Recommended timing:** After Priority 1 (AkuAI) migration is complete and working in production.  
AkuAI defines the `inference` contract that everything else consumes — having a working AkuAI service makes it natural to extract that contract first.

Do NOT wait for all 9 services to migrate before creating this repo — the longer you wait, the more duplication accumulates.

---

## Tracking

Add to `automation_progress.md` once work begins. Link from `docs/ecosystem-map.md` Contracts & API Specs section.
