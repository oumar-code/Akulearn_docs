# RAG Chatbot Strategy — Hybrid, Curriculum-Grounded

> **Status:** Adopted  
> **Audience:** AI/ML Engineers, Backend Engineers, Curriculum Team, Product  
> **Last updated:** April 2026  
> **Related docs:** [`ai_tutor.md`](../ai_tutor.md) · [`LO_TAGGING_SCHEMA.md`](../LO_TAGGING_SCHEMA.md) · [`handbooks/MLOps_AI_Engineering_Handbook.md`](../handbooks/MLOps_AI_Engineering_Handbook.md) · [`AIOPS_STRATEGY.md`](../AIOPS_STRATEGY.md)

---

## Executive Summary

Akulearn's AI chatbot ("AkuTutor") uses **Retrieval-Augmented Generation (RAG)** grounded in the NERDC/WAEC/NECO/JAMB curriculum corpus.  
The system is **edge-first**: every Aku Edge Hub can answer student questions fully offline using a compact local index and quantised language model.  
When internet connectivity is available the hub falls back to cloud-scale retrieval and larger models hosted on the Aku Super Hub / IG-Hub.

---

## 1. Tutor Contract

### 1.1 Scope

The chatbot is scoped exclusively to academic support:

| In scope | Out of scope |
|----------|-------------|
| Curriculum Q&A (JSS1–SS3, WAEC/NECO/JAMB) | General-purpose internet search |
| Worked-step explanations | Off-topic conversation |
| Revision flashcards and quick recaps | Medical, legal, or financial advice |
| Exam technique and past-question walkthroughs | Any content not in the approved knowledge base |
| Study schedule guidance per LO mastery gap | Social media or entertainment |

### 1.2 Response Context Tags

Every request and response must carry the following context envelope:

```json
{
  "learner_id": "<hashed>",
  "class_level": "SS2",
  "subject": "PHY",
  "exam_path": ["WAEC", "NECO"],
  "language": "en",
  "response_mode": "step_by_step",
  "lo_ids": ["LO:NERDC:PHY:SS2:WAV:001"]
}
```

| Field | Values |
|-------|--------|
| `class_level` | `JSS1`–`JSS3`, `SS1`–`SS3` |
| `subject` | Standard subject codes (MAT, PHY, CHE, BIO, ENG, …) — see `LO_TAGGING_SCHEMA.md` |
| `exam_path` | `WAEC`, `NECO`, `JAMB`, `BECE`, `State` |
| `language` | `en`, `ha`, `ig`, `yo` |
| `response_mode` | `direct`, `step_by_step`, `hint_only`, `exam_style`, `recap` |

### 1.3 Citation Requirement

Factual answers **must** reference at least one knowledge-base source:

```
Answer: ...
Source: LO:NERDC:PHY:SS2:WAV:001 — "Akulearn Physics SS2 Waves" (v1.2, reviewed 2026-03)
```

If no source with confidence ≥ threshold is retrieved, the bot must refuse to answer and escalate (see §4.3).

---

## 2. Knowledge Base

### 2.1 Source Prioritisation

Sources are ingested in the following trust order.  Higher-trust sources are preferred during retrieval re-ranking:

| Priority | Source | Format | Trust level |
|----------|--------|---------|-------------|
| 1 | Akulearn-produced lesson content | Markdown / JSON | **Highest** |
| 2 | Teacher-reviewed explanations | JSON | High |
| 3 | WAEC / NECO / JAMB past questions with model answers | JSON | High |
| 4 | NERDC approved textbook extracts | PDF chunks | Medium |
| 5 | Supplementary OERs (e.g., CK-12, OpenStax) | Markdown | Low |

### 2.2 Source Metadata Schema

Every document chunk stored in the knowledge base carries:

```json
{
  "chunk_id": "phy-ss2-wav-001-c03",
  "lo_ids": ["LO:NERDC:PHY:SS2:WAV:001"],
  "curriculum": "NERDC",
  "subject": "PHY",
  "class_level": "SS2",
  "topic": "Waves",
  "language": "en",
  "difficulty": "medium",
  "asset_type": "lesson",
  "version": "1.2",
  "review_status": "teacher_approved",
  "reviewed_by": "teacher_username",
  "reviewed_at": "2026-03-15",
  "source_path": "content/textbooks/phy_ss2/chapter4_waves.md",
  "trust_level": 1
}
```

### 2.3 Content Freshness Policy

| Condition | Action |
|-----------|--------|
| Curriculum revision by NERDC / WAEC | Re-tag affected LOs, flag chunks for re-review |
| chunk age > 12 months | Auto-flag for reviewer; suppress in top-k if unreviewed |
| Reviewer corrects or rejects a chunk | Remove from active index; log rejection reason |
| New exam past questions available | Ingest within 30 days of official release |

### 2.4 Reviewer Workflow

1. **Auto-ingest** — content pipeline creates chunks, generates embeddings, sets `review_status=pending`.
2. **AI pre-screening** — classify topic, assign candidate `lo_ids`, set `confidence` score.
3. **Teacher / curriculum expert review** — approve, correct, or reject via the LO Mapper UI.
4. **Publish** — `review_status=teacher_approved`; chunk becomes eligible for retrieval.
5. **Audit** — all reviewer actions are logged with timestamp and username.

---

## 3. Two-Layer Retrieval Design

```
Student question
      │
      ▼
┌─────────────────────────────────────────────────────┐
│  Layer A — Structured Curriculum Filter             │
│  Filter by: class_level, subject, exam_path, lo_id  │
│  Result: candidate chunk pool (exact metadata match) │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│  Layer B — Semantic Retrieval                       │
│  Embed question with all-MiniLM-L6-v2 (384-dim)    │
│  ANN search over filtered pool → top-k chunks      │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│  Re-ranking & Threshold Gate                        │
│  Score = semantic_similarity × trust_weight         │
│  Enforce curriculum_match ≥ 0.75; drop below         │
└─────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│  Generation (LLM)                                   │
│  Prompt = system_prompt + context_chunks + question │
│  Output: response + source citations                 │
└─────────────────────────────────────────────────────┘
```

### 3.1 Embeddings

| Component | Detail |
|-----------|--------|
| Model | `all-MiniLM-L6-v2` (384-dim) — edge-compatible |
| Chunk size | 256 tokens, 32-token overlap |
| Index format | FAISS `IndexFlatIP` for edge (exact); HNSW for cloud |
| Vector store | Edge: FAISS flat files on hub filesystem; Cloud: Milvus / Pinecone |

### 3.2 Re-ranking

```python
final_score = semantic_similarity * trust_weight(chunk) * recency_weight(chunk)

# trust_weight: 1.0 (Akulearn lesson), 0.9 (teacher-reviewed), 0.8 (past questions),
#               0.6 (NERDC textbook extract), 0.4 (OER)
# recency_weight: 1.0 if reviewed within 6 months, 0.85 if 6–12 months, 0.5 if >12 months
```

Chunks below `curriculum_match = 0.75` are excluded from the generation context regardless of semantic score.

---

## 4. Edge-Local RAG (Offline-First)

### 4.1 Edge Hub Index

| Asset | Location on hub | Size target |
|-------|----------------|-------------|
| FAISS index | `/aku/rag/index.faiss` | ≤ 500 MB |
| Chunk metadata | `/aku/rag/chunks.jsonl` | ≤ 200 MB |
| LO catalog | `/aku/rag/lo_catalog.json` | ≤ 10 MB |
| Quantised LLM (GGUF) | `/aku/models/gemma-2b-q4.gguf` | ≤ 1.5 GB |
| Embedding model | `/aku/models/all-minilm-l6-v2.onnx` | ≤ 25 MB |

### 4.2 Sync Protocol

During a connectivity window the Aku Edge Hub sync agent (`aku-learn-sync`) performs:

1. **Delta index download** — only chunks updated or added since `last_sync_ts`.
2. **FAISS index merge** — apply delta with `IndexFlatIP.add()` and rebuild on next maintenance window.
3. **LO catalog refresh** — replace `lo_catalog.json` atomically.
4. **Model update** — download new GGUF if `model_version` on Super Hub is newer; verify SHA-256 before activation.
5. **Policy sync** — guardrail rules, blocklists, threshold overrides.

Sync is scheduled during off-peak hours and uses exponential back-off on failure.

### 4.3 Fallback Behaviour

| Condition | Behaviour |
|-----------|-----------|
| Retrieval confidence < 0.75 | Return "I don't have enough information on this topic yet. Ask your teacher or try rephrasing." + show 3 related topics |
| No chunks match LO filter | Suggest the closest LO topic; do not hallucinate |
| Model load failure | Return static exam tips from `lo_catalog.json` |
| Connectivity lost mid-session | Complete current turn from edge index; notify UI to show offline badge |
| Teacher escalation trigger | Log event; surface in teacher dashboard |

---

## 5. Pedagogy-Aware Generation

### 5.1 Response Modes

| Mode | When to use | Behaviour |
|------|-------------|-----------|
| `direct` | Factual recall, definitions | Short precise answer + citation |
| `step_by_step` | Calculation, multi-step reasoning | Numbered steps, show working |
| `hint_only` | Active practice question | One hint per turn; withhold full answer until 3 attempts |
| `exam_style` | Exam prep | WAEC/JAMB format response with mark scheme language |
| `recap` | End-of-topic revision | Bullet-point summary of key LO takeaways |

### 5.2 Adaptive Personalisation

- Pull learner's LO mastery scores from the User Profile Service.
- Increase `step_by_step` depth for LOs where mastery < 60 %.
- Surface "next best practice" prompt after each answer:  
  *"You've reviewed Waves. Try a practice question on Wave Speed Calculations (LO:NERDC:PHY:SS2:WAV:003)."*
- For practice questions, apply `hint_only` mode; never dump the full answer on the first attempt.

### 5.3 System Prompt Template

```
You are AkuTutor, the AI tutor for the Akulearn platform.
You help Nigerian secondary school students (class: {{class_level}}, subject: {{subject}})
prepare for {{exam_path}} examinations.
Respond in {{language}}.
Use only the retrieved context below. Do not invent information.
Response mode: {{response_mode}}.

Retrieved context:
{{context_chunks}}

Student question:
{{question}}

End your response with:
Source: <lo_id> — "<source_title>" (v<version>, reviewed <reviewed_at>)
```

---

## 6. Guardrails

### 6.1 Grounding Check

Before returning a response, verify:

- At least one context chunk with `final_score ≥ 0.75` is present.
- The generated answer does not introduce entities absent from the retrieved context (post-generation entailment check using a lightweight NLI classifier).

If either check fails → refuse and use fallback message.

### 6.2 Safety Filters

| Filter | Method |
|--------|--------|
| Off-topic detection | Zero-shot classification against allowed topic list |
| Harmful content | Moderation classifier (e.g., Perspective API or local toxic-bert) |
| Exam answer dumping | `hint_only` mode enforced server-side; cannot be overridden by student |
| Language gate | Only `en`, `ha`, `ig`, `yo` responses generated; reject other languages |

### 6.3 Audit Logging

Each interaction is logged (on Edge Hub, synced to cloud):

```json
{
  "session_id": "<uuid>",
  "learner_id": "<hashed>",
  "timestamp": "2026-04-19T18:00:00Z",
  "class_level": "SS2",
  "subject": "PHY",
  "lo_ids": ["LO:NERDC:PHY:SS2:WAV:001"],
  "response_mode": "step_by_step",
  "retrieved_chunk_ids": ["phy-ss2-wav-001-c03"],
  "top_score": 0.87,
  "grounding_check_passed": true,
  "safety_check_passed": true,
  "fallback_triggered": false,
  "teacher_escalated": false,
  "latency_ms": 340
}
```

No raw question text or learner name is stored in the audit log.

---

## 7. KPI Dashboard

### 7.1 Retrieval Quality

| Metric | Target | Alert threshold |
|--------|--------|----------------|
| Hit rate @ k=5 | ≥ 0.85 | < 0.75 |
| Curriculum alignment score (avg `final_score`) | ≥ 0.80 | < 0.72 |
| Citation coverage (% responses with valid source) | ≥ 0.95 | < 0.90 |
| Grounding check pass rate | ≥ 0.97 | < 0.93 |

### 7.2 Learning Impact

| Metric | Target | Measurement |
|--------|--------|-------------|
| LO mastery improvement (pre/post) | +15 % per 4-week cohort | User Profile Service mastery scores |
| Quiz uplift (after chatbot session) | +10 % score vs. baseline | Aku Learn quiz engine |
| Hint-to-correct-answer rate | ≥ 0.70 | Ratio of correct answers after hint vs. total hint sessions |
| Teacher escalation rate | ≤ 0.05 | Fallback log |

### 7.3 Operations

| Metric | Target | Alert threshold |
|--------|--------|----------------|
| Edge response latency (p95) | ≤ 800 ms | > 1 500 ms |
| Cloud response latency (p95) | ≤ 2 000 ms | > 4 000 ms |
| Offline uptime (edge RAG available) | ≥ 99.5 % | < 98 % |
| Index sync freshness | ≤ 24 h behind cloud | > 48 h |
| Fallback trigger rate | ≤ 0.08 | > 0.15 |
| Teacher override rate | ≤ 0.03 | > 0.08 |

---

## 8. Rollout Phases

### Phase 1 — English-Language Pilot (JSS/SS, top 3 subjects)

**Scope:** English, Mathematics, Biology · Edge pilots at low-connectivity schools in Zamfara  
**Deliverables:**

- [ ] Ingest and tag content for ENG, MAT, BIO (JSS1–SS3)
- [ ] Build initial FAISS index; deploy to pilot Edge Hubs
- [ ] `hint_only` and `step_by_step` modes live in AkuTutor service
- [ ] Audit logging active; KPI dashboard baseline
- [ ] Teacher escalation flow in Teacher Dashboard

**Exit criteria:** Hit rate@5 ≥ 0.82, latency p95 ≤ 800 ms on edge hardware.

---

### Phase 2 — Multilingual Expansion + Teacher Feedback Loop

**Scope:** Add Hausa (`ha`), Igbo (`ig`), Yoruba (`yo`) · Expand to all JSS/SS subjects  
**Deliverables:**

- [ ] Multilingual embeddings (extend to `paraphrase-multilingual-MiniLM-L12-v2`)
- [ ] Translated lesson chunks ingested and reviewed for HA/IG/YO
- [ ] Teacher feedback UI: thumbs up/down on AkuTutor responses feeds back into chunk trust scores
- [ ] Automated re-ranking weight updates from feedback signal
- [ ] Expand pilot to additional schools / states

**Exit criteria:** Curriculum alignment score ≥ 0.80 across all 4 languages.

---

### Phase 3 — Full Adaptive Tutoring + Governance

**Scope:** Full subject coverage · Continuous evaluation cadence · Policy governance  
**Deliverables:**

- [ ] Full LO mastery integration → personalised `response_mode` selection
- [ ] "Next best practice" prompt engine tied to LO mastery gaps
- [ ] Quarterly content review cadence (curriculum freshness policy enforced)
- [ ] Model fine-tuning pipeline on Akulearn-specific curriculum data (Super Hub GPU)
- [ ] Red-team evaluation: adversarial prompt testing, bias audit
- [ ] Stakeholder governance board reviews KPIs quarterly

**Exit criteria:** LO mastery improvement ≥ 15 % per 4-week cohort across all subjects.

---

## Appendix A — Service Integration Points

| AkuTutor depends on | Purpose |
|--------------------|---------|
| `AkuAI` `/api/v1/embeddings` | Generate query embeddings |
| `AkuAI` `/api/v1/text/generate` or Gemma edge relay | Response generation |
| User Profile Service | Learner LO mastery scores |
| Content Management Service (CMS) | Chunk ingestion pipeline |
| LO Catalog (`lo_catalog.json`) | Curriculum filter metadata |
| Aku Learn Sync (`aku-learn-sync`) | Delta index delivery to edge |
| Teacher Dashboard | Escalation events, feedback signals |

---

## Appendix B — Vector Store Decision Matrix

| Environment | Store | Index type | Why |
|-------------|-------|-----------|-----|
| Edge Hub (offline) | FAISS (local file) | `IndexFlatIP` | Zero-dependency, ≤ 500 MB, no network |
| Super Hub (regional) | Milvus (self-hosted) | HNSW | High throughput, metadata filtering, open-source |
| IG-Hub / Cloud | Pinecone or Weaviate | HNSW | Managed, global scale, multi-tenant |

---

## Appendix C — Guardrail Thresholds (configurable via policy sync)

| Parameter | Default | Env var |
|-----------|---------|---------|
| Minimum retrieval score | 0.75 | `RAG_MIN_SCORE` |
| Top-k chunks | 5 | `RAG_TOP_K` |
| Max context tokens | 1 800 | `RAG_MAX_CONTEXT_TOKENS` |
| Max response tokens | 512 | `RAG_MAX_RESPONSE_TOKENS` |
| Hint-mode max attempts before answer | 3 | `RAG_HINT_MAX_ATTEMPTS` |
| Chunk max age before re-review flag | 365 days | `RAG_CHUNK_MAX_AGE_DAYS` |
