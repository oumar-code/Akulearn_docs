# AkuTutor — AI Tutoring Service

AkuTutor is the curriculum-aware AI tutoring microservice in the Akulearn platform. It does **not** run its own model; all text generation is delegated to **AkuAI** via `AKU_AI_URL`.

---

## Responsibilities

| Concern | Owner |
|---|---|
| Session lifecycle (create / read) | `app/routers/sessions.py` |
| Learner Q&A and hint scaffolding | `app/services/tutor.py` |
| Curriculum-aware prompt construction | `app/services/tutor.py` |
| Learner feedback collection | `app/routers/feedback.py` |
| AkuAI HTTP calls | `app/services/tutor.py → _call_aku_ai()` |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/sessions` | Start a new tutoring session |
| `GET` | `/api/v1/sessions/{id}` | Retrieve session message history |
| `POST` | `/api/v1/sessions/{id}/ask` | Submit a question → answer from AkuAI |
| `POST` | `/api/v1/sessions/{id}/hint` | Request a hint → guided hint from AkuAI |
| `POST` | `/api/v1/feedback` | Submit session feedback (rating + comment) |

Interactive docs available at `http://localhost:8002/docs` when running locally.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements-extra.txt

# 2. Configure environment
cp .env.example .env
# Edit .env — set AKU_AI_URL to a running AkuAI instance

# 3. Run
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

---

## Project Structure

```
AkuTutor/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app factory (wire up here)
│   ├── dependencies.py          # Settings + DI providers
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── sessions.py          # Session + ask/hint endpoints
│   │   └── feedback.py          # Feedback endpoint
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── sessions.py          # Pydantic v2 models
│   └── services/
│       ├── __init__.py
│       └── tutor.py             # TutorService (prompt builder + AkuAI client)
├── .env.example
├── requirements-extra.txt
└── README.md
```

---

## Prompt Design

### Ask
```
You are a tutor for {subject} at {grade_level} level.
Explain clearly and use age-appropriate language.

Student asks: {question}
```

### Hint
```
You are a tutor for {subject} at {grade_level} level.
Give a helpful hint (not the full answer) for the following question.
Guide the student towards the answer without revealing it.

Question: {question}
```

Both prompts are constructed in `app/services/tutor.py` and posted to:
```
POST {AKU_AI_URL}/api/v1/text/generate
Body: { "prompt": "..." }
```

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `AKU_AI_URL` | `http://akuai:8001` | Base URL of the AkuAI service |
| `APP_NAME` | `AkuTutor` | Shown in OpenAPI docs |
| `LOG_LEVEL` | `INFO` | Python logging level |

---

## Session Data Model

```json
{
  "id": "uuid",
  "learner_id": "string",
  "subject": "Mathematics",
  "grade_level": "Grade 7",
  "messages": [
    { "role": "learner", "content": "What is a prime number?", "timestamp": "..." },
    { "role": "tutor",   "content": "A prime number is ...",   "timestamp": "..." }
  ],
  "created_at": "..."
}
```

---

## Production Notes

- **Session store**: The scaffold uses an in-memory dict. Replace `_sessions` in `tutor.py` with a PostgreSQL/Redis adapter before deploying.
- **Auth**: Add a JWT dependency on the router to guard learner-scoped data.
- **Timeouts**: `_call_aku_ai` defaults to 30 s. Tune `timeout` for your AkuAI SLA.
- **Retries**: Consider wrapping `_call_aku_ai` with `tenacity` for transient AkuAI failures.
