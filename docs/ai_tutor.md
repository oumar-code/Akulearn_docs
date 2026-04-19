# AI Tutor (AkuTutor)

AkuTutor is Akulearn's curriculum-grounded AI chatbot that helps students at every class level (JSS1–SS3) prepare for WAEC, NECO, JAMB, and BECE examinations.  
It uses **Retrieval-Augmented Generation (RAG)** so every answer is backed by approved lesson content, past questions, and the NERDC LO catalog — not hallucinated text.

## Strategy

The full design is documented in **[`docs/strategy/rag_chatbot_strategy.md`](strategy/rag_chatbot_strategy.md)**.

Key pillars:

| Pillar | Summary |
|--------|---------|
| **Hybrid edge + cloud** | Runs fully offline on Aku Edge Hubs; upgrades to cloud models when connected |
| **Curriculum-grounded retrieval** | Two-layer search (LO/topic filter → semantic vector search) with re-ranking |
| **Pedagogy-aware responses** | Five response modes: `direct`, `step_by_step`, `hint_only`, `exam_style`, `recap` |
| **Strong guardrails** | Grounding checks, safety filters, audit logs — no hallucinated facts |
| **Measurable outcomes** | KPIs cover retrieval quality, learning impact, and operational health |

## Architecture Overview

```
Student question
      │
      ▼
AkuTutor Service  (delegates all inference to AkuAI)
      │
      ├── Layer A: Curriculum filter  (class, subject, LO, exam path)
      ├── Layer B: Semantic search    (FAISS/Milvus + all-MiniLM-L6-v2)
      ├── Re-ranking & threshold gate (score ≥ 0.75 required)
      └── Generation                 (Gemma edge relay or cloud LLM)
                                     + citation appended
```

## Service Integration

| Dependency | Role |
|------------|------|
| `AkuAI /api/v1/embeddings` | Query embedding |
| `AkuAI /api/v1/text/generate` | Response generation |
| User Profile Service | LO mastery scores for personalisation |
| CMS + `aku-learn-sync` | Content ingestion and edge index delivery |
| LO Catalog (`lo_catalog.json`) | Curriculum metadata filter |
| Teacher Dashboard | Escalation and feedback signals |

## Rollout Phases

| Phase | Scope | Status |
|-------|-------|--------|
| 1 | English · Mathematics · Biology (en) — Zamfara pilot | Planned |
| 2 | Full subject coverage + Hausa / Igbo / Yoruba | Planned |
| 3 | Full adaptive tutoring, governance cadence | Planned |

For detailed acceptance criteria, KPI targets, and implementation tasks, see the [RAG chatbot strategy](strategy/rag_chatbot_strategy.md).
