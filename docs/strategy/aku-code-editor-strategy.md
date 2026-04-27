# Aku Code Editor — Strategy

> **Status:** Adopted  
> **Last updated:** April 2026  
> **Audience:** AI/ML Engineers, Backend Engineers, Curriculum Team, Platform Leadership  
> **Related docs:** [`services/aku-code-editor.md`](../services/aku-code-editor.md) · [`api/aku-code-editor-openapi.yaml`](../api/aku-code-editor-openapi.yaml) · [`adrs/adr-005-aku-code-editor.md`](../adrs/adr-005-aku-code-editor.md) · [`strategy/rag_chatbot_strategy.md`](./rag_chatbot_strategy.md)

---

## Executive Summary

Aku Code Editor is a **curriculum-grounded, edge-deployable, privacy-first AI code assistant** built into the Aku Platform. Unlike general-purpose code completion tools (GitHub Copilot, Cursor), Aku Code Editor is scoped exclusively to the Akulearn educational mission: helping Nigerian secondary school students and teachers write, understand, and learn from code in the context of their curriculum.

The editor is integrated with AkuWorkspace, AkuAI, Akudemy, and Aku-DaaS, and is designed to be deployable on the Aku Edge Hub for fully offline operation.

---

## Strategic Pillars

### 1. Learns from Usage

Accepted/rejected completions and user corrections feed an anonymized fine-tuning queue in Aku-DaaS. Over time, the code model becomes progressively more accurate for:
- The Akulearn code style (Python/FastAPI microservices)
- Curriculum-specific patterns (Physics simulations, Biology data analysis, Maths algorithms)
- Local coding conventions and variable naming patterns observed in student projects

**Why this matters:** Generic code models are trained on open-source code but have no awareness of a secondary school curriculum or Akulearn's architecture. A fine-tuned model will produce better suggestions for this specific context.

### 2. Curriculum-Aware Generation

When a student provides a `subject_context` (e.g., "Biology", "Physics SS2"), the Code Editor:
1. Queries Akudemy for relevant LO descriptions matching the subject and class level.
2. Injects the LO descriptions into the generation system prompt.
3. The model produces code that accurately illustrates curriculum concepts.

**Example:**
> Prompt: "Write a Python function to simulate projectile motion"  
> Subject context: "Physics SS2"  
> LO injected: `LO:NERDC:PHY:SS2:KIN:001 — "Calculate range, maximum height and time of flight for projectile motion"`

The generated code will correctly implement `g = 9.8 m/s²`, compute `range = v₀² sin(2θ) / g`, and include inline comments referencing the LO — not generic copy-pasted StackOverflow code.

### 3. Offline-First

A quantized code model (≤ 1.5 GB GGUF, e.g., CodeGemma-2B-Q4 or StarCoder2-3B-Q4) is deployed on Aku Edge Hub via K3s. When `CODE_MODEL_PATH` is set and `OPERATING_MODE=offline`, all inference runs locally:

- No network call to AkuAI or any cloud service.
- Suitable for rural schools with no internet access.
- Session context stored in Redis on the Edge Hub (local Redis instance).

Sync agent downloads updated model versions during connectivity windows (verified by SHA-256 before activation).

### 4. Student Safety Guardrails

| Guardrail | Trigger | Action |
|-----------|---------|--------|
| Harmful code classifier | Shell injection, credential exfiltration, known malware patterns | Block response + log event |
| License compliance scan | GPL-incompatible code patterns (AST heuristic) | Flag for teacher review |
| Rate limiting | Per-user daily token budget | Return `429` with budget status |
| Language/topic restriction | Admin policy per institution | Restrict to approved languages/subjects |
| Exam answer detection | Code implements published exam solution | Warn + log (not blocked — teacher discretion) |

### 5. AkuWorkspace Integration

A student can:
1. Open the Aku Code Editor inside AkuWorkspace.
2. Generate a code example (e.g., "simulate Hooke's Law").
3. Click "Embed in Document" → the code block is inserted into an Aku Docs document.
4. Click "Explain" → AkuAI generates a plain-language explanation of the code, also embedded.
5. The resulting document becomes a study artifact — code + explanation + LO citation.

---

## Model Selection

| Candidate | Size (Q4) | Language support | Edge-deployable | Notes |
|-----------|-----------|-----------------|----------------|-------|
| CodeGemma-2B | ~1.2 GB | Python, JS, C++ | ✅ | Google; good Python coverage |
| StarCoder2-3B | ~1.5 GB | 80+ languages | ✅ | BigCode; strong multi-language |
| Phi-3-mini-4k | ~2.2 GB | Python, JS | ⚠ | Too large for 1.5 GB budget |
| DeepSeek-Coder-1.3B | ~0.8 GB | Python, JS | ✅ | Fastest; less accurate |

**Decision:** Start with `CodeGemma-2B-Q4` (best Python accuracy within edge budget). Evaluate `StarCoder2-3B-Q4` for multi-language expansion in Phase 5. See [`adrs/adr-005-aku-code-editor.md`](../adrs/adr-005-aku-code-editor.md) for full rationale.

---

## Rollout Phases

### Phase 3 — Scaffold (Sprints 5–6)

**Deliverables:**
- [ ] Service added to `docker-compose.dev.yml` under `editor` profile
- [ ] OpenAPI contract defined for all 8 endpoints
- [ ] All endpoints return deterministic stub responses (fixtures)
- [ ] Registered in Aku-SuperHub service registry
- [ ] Prometheus scrape target active
- [ ] K8s manifest created (`docs/deployment/k8s/aku-code-editor.yaml`)

**Exit criteria:** All stub endpoints return `200 OK` with valid JSON matching the OpenAPI contract; service is healthy in CI integration test.

---

### Phase 4 — Learning Engine (Sprints 7–8)

**Deliverables:**
- [ ] Real inference via AkuAI code model (CodeGemma-2B-Q4)
- [ ] Session memory (Redis DB 9, 7-day TTL)
- [ ] Correction pair capture + DaaS export
- [ ] Curriculum-aware generation with Akudemy LO injection
- [ ] Code review intelligence (structured `ReviewResult`)
- [ ] Debug assistant (stack trace parsing + FAISS debug index)
- [ ] SSE + WebSocket streaming live
- [ ] Acceptance rate tracking active

**Exit criteria:** Completion acceptance rate ≥ 40% in 2-week internal dogfooding; p95 latency ≤ 500 ms.

---

### Phase 5 — Production Hardening (Sprints 9–10)

**Deliverables:**
- [ ] Harmful code classifier activated (`ENABLE_HARMFUL_CODE_FILTER=true`)
- [ ] License compliance scan activated (`ENABLE_LICENSE_SCAN=true`)
- [ ] Edge Hub K3s deployment (CodeGemma-2B-Q4 GGUF on PVC)
- [ ] Admin institution policy API (language/topic restrictions)
- [ ] Teacher session summary dashboard (no raw code)
- [ ] Zero critical/high CodeQL findings
- [ ] Full Grafana dashboard for Code Editor SLOs

**Exit criteria:** Pilot deployment to 3 schools; zero security incidents in 2-week pilot; acceptance rate ≥ 40%; no raw code present in Postgres or logs.

---

## KPI Dashboard

| Metric | Target | Alert threshold |
|--------|--------|----------------|
| Completion acceptance rate | ≥ 40% | < 30% |
| Generation success rate | ≥ 95% | < 90% |
| Completion latency p95 | ≤ 500 ms | > 800 ms |
| Generation latency p95 | ≤ 2 000 ms | > 4 000 ms |
| Active sessions | tracked | — |
| Tokens generated / day | tracked | — |
| Correction pairs exported to DaaS / week | tracked | — |
| Harmful code blocks / week | tracked | alert if > 10 |
| Token budget overrun rate | ≤ 0.01% | > 0.1% |

---

## Integration Map

| Aku Code Editor depends on | Purpose |
|---------------------------|---------|
| `AkuAI` `/api/v1/code/complete` | Tab-completion inference |
| `AkuAI` `/api/v1/code/generate` | Natural language → code generation |
| `AkuAI` `/api/v1/code/explain` | Code explanation |
| `AkuAI` `/api/v1/code/review` | Static review analysis |
| `Akudemy` `/api/v1/curriculum/lo/{lo_id}` | LO context for curriculum-aware generation |
| `Aku-DaaS` `/api/v1/datasets/ingest` | Fine-tuning queue (correction pairs) |
| `Redis DB 9` | CodeSession storage, streaming buffers, rate limit counters |
| `Postgres code_editor schema` | Correction pairs + session summaries (persistent) |

| Depends on Aku Code Editor | Purpose |
|---------------------------|---------|
| `AkuWorkspace` | Embed generated code + explanation in Aku Docs |
| `Aku-SuperHub` | Service registry + JWT validation |
