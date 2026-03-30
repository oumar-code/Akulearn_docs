# AkuAI — Shared Inference Service

AkuAI is the **centralised inference layer** for the entire Aku Platform.  
All other services (AkuLearn, AkuMentor, AkuAssess, AkuSkills, etc.) call AkuAI — it does **not** expose domain models from those services.

- **Runtime:** Python 3.11 / FastAPI  
- **Port (default):** `8004`  
- **API prefix:** `/api/v1`

---

## Directory layout

```
AkuAI/
├── app/
│   ├── routers/
│   │   ├── inference.py   # POST /inference, /text/generate, /text/classify,
│   │   │                  #      /text/summarize, /embeddings
│   │   └── models.py      # GET  /models, POST /models/gemma/infer
│   ├── schemas/
│   │   └── inference.py   # Pydantic v2 request/response models
│   └── services/
│       └── inference.py   # InferenceService (async, stub → real torch impl)
├── .env.example
├── requirements-extra.txt
└── README.md
```

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/inference` | Generic inference against any registered model |
| `POST` | `/api/v1/text/generate` | LLM text generation |
| `POST` | `/api/v1/text/classify` | Zero-shot text classification |
| `POST` | `/api/v1/text/summarize` | Document summarisation |
| `POST` | `/api/v1/embeddings` | Vector embeddings for semantic search |
| `GET`  | `/api/v1/models` | List available models and their capabilities |
| `POST` | `/api/v1/models/gemma/infer` | Gemma relay for Edge Hub containers (< 4 KB payload) |

---

## Quickstart

```bash
# 1 — Copy and configure environment
cp .env.example .env

# 2 — Install platform requirements (from repo root)
pip install -r requirements.txt

# 3 — Install AkuAI ML dependencies
pip install -r requirements-extra.txt

# 4 — Run the service
uvicorn app.main:app --reload --port 8004
```

---

## `main.py` integration snippet

Create `app/main.py` in the AkuAI service root and wire in the routers:

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import inference, models
from app.services.inference import inference_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load models into memory
    await inference_service.startup()
    yield
    # Shutdown: release model resources
    await inference_service.shutdown()


app = FastAPI(
    title="AkuAI",
    description="Shared inference layer for the Aku Platform.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten via CORS_ORIGINS env var in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inference.router)
app.include_router(models.router)


@app.get("/health", tags=["ops"])
async def health() -> dict:
    return {"status": "ok", "service": "AkuAI"}
```

---

## Service dependency

Add AkuAI to other services using standard `httpx` async calls:

```python
import httpx

AKUAI_BASE = "http://akuai:8004"

async def generate(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{AKUAI_BASE}/api/v1/text/generate",
            json={"prompt": prompt, "model": "gemma-2b", "max_tokens": 256},
            timeout=30.0,
        )
        r.raise_for_status()
        return r.json()["text"]
```

---

## Implementing real model loading

Replace the stub `TODO` sections in `app/services/inference.py`:

1. **Text generation / Gemma** — use `llama_cpp.Llama` pointed at `GEMMA_GGUF_PATH`.
2. **Summarisation / Classification** — use `transformers.pipeline(...)` with the model IDs already declared in the stub catalogue.
3. **Embeddings** — use `sentence_transformers.SentenceTransformer(model_id).encode(...)`.

Load all pipelines inside `InferenceService.startup()` and store them as instance attributes.  
The `get_inference_service` dependency injects the same singleton across all requests.

---

## Edge Hub notes

The `/api/v1/models/gemma/infer` endpoint is designed for Edge Hub containers  
that have intermittent or low-bandwidth connectivity:

- Callers **must** include `hub_id` in the request body for response routing.
- Request + response bodies are capped at **4 KB** (`GEMMA_MAX_PAYLOAD_BYTES`).
- The `prompt` field is limited to **2 048 characters**.
- Do **not** add streaming or binary payloads to this endpoint.
