# ADR-005: Aku Code Editor — Model Selection, Learning Engine Design & Edge Deployment

> **Status:** Accepted  
> **Date:** April 2026  
> **Author:** Platform Engineering  
> **Supersedes:** N/A  
> **Related:** [`services/aku-code-editor.md`](../services/aku-code-editor.md) · [`strategy/aku-code-editor-strategy.md`](../strategy/aku-code-editor-strategy.md)

---

## Context

Akulearn needs an AI code assistant to help Nigerian secondary school students and teachers write, understand, and learn from code within the curriculum context. The assistant must:

1. Work offline on Aku Edge Hub hardware (ARM64, ~4 GB RAM total, ≤ 1.5 GB available for model).
2. Be curriculum-aware — code examples should reference and illustrate NERDC/WAEC learning objectives.
3. Learn from corrections to improve over time.
4. Operate within student safety guardrails (no harmful code, no raw code stored after session).
5. Integrate with existing Aku Platform services (AkuAI, Akudemy, Aku-DaaS).

Three key decisions were required:
- **D1:** Which code model to use at the edge?
- **D2:** How should the learning/fine-tuning loop be designed?
- **D3:** How should the service be deployed across cloud and edge tiers?

---

## Decision 1: Code Model Selection

### Options Considered

| Model | Size (Q4_K_M) | Python acc. | Multi-lang | Edge RAM fit | License |
|-------|--------------|-------------|------------|-------------|---------|
| CodeGemma-2B | ~1.2 GB | ⭐⭐⭐⭐ | ⭐⭐ | ✅ | Apache 2.0 |
| StarCoder2-3B | ~1.5 GB | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ (tight) | BigCode OpenRAIL-M |
| Phi-3-mini-4k | ~2.2 GB | ⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | MIT |
| DeepSeek-Coder-1.3B | ~0.8 GB | ⭐⭐ | ⭐⭐⭐ | ✅ | Apache 2.0 |
| WizardCoder-3B | ~1.7 GB | ⭐⭐⭐ | ⭐⭐ | ❌ | Apache 2.0 |

### Decision

**Use `CodeGemma-2B-Q4_K_M` as the primary edge code model.**

**Rationale:**
- Best Python accuracy within the 1.5 GB edge budget. Python is the dominant language in Akulearn curriculum exercises.
- Apache 2.0 license — no usage restrictions for educational deployment.
- Fits comfortably in the edge RAM budget (1.2 GB), leaving 300 MB headroom for the runtime and OS.
- Google's code-specific fine-tune; outperforms generic 2B models on code completion benchmarks.

**StarCoder2-3B** is the designated **Phase 5 evaluation target** for multi-language expansion (JavaScript, C++). If the 1.5 GB budget is exceeded, the model will be deployed on SuperHub only (not Edge Hub).

### Consequences
- AkuAI must support loading a second GGUF model (`CODE_MODEL_PATH`) alongside the general `gemma-2b-q4.gguf`.
- Edge Hub K3s deployment requires a `PersistentVolumeClaim` (1.5 GB minimum) for the model file.
- Model updates are signed with SHA-256 and verified before activation.

---

## Decision 2: Learning Engine Design

### Options Considered

**Option A — Federated Fine-Tuning (on-device)**
- Train a LoRA adapter on each Edge Hub using accepted/rejected correction pairs.
- Merge adapters back to SuperHub periodically.
- **Rejected:** Too computationally intensive for Edge Hub hardware; LoRA training requires a GPU.

**Option B — Centralized Fine-Tuning via DaaS Queue (chosen)**
- Collect anonymized correction pairs (`original_completion`, `user_correction`) in a DaaS ingestion queue.
- Batch fine-tuning runs on SuperHub/IGHub GPU (or cloud) on a weekly cadence.
- Distribute updated model GGUF to Edge Hubs via sync agent.

**Option C — RLHF with Accept/Reject Signals**
- Use accept/reject signals as reward model training data.
- **Deferred to Phase 6:** Requires a separate reward model and RLHF pipeline. Too complex for Phase 4.

### Decision

**Option B: Centralized fine-tuning via anonymized DaaS correction queue.**

**Rationale:**
- Technically feasible on existing hardware (SuperHub GPU or spot cloud instance).
- Correction pairs provide high signal-to-noise data (user directly showed the correct output).
- Privacy-preserving: user IDs are hashed, raw code is never stored beyond session TTL.
- Aligns with existing DaaS data pipeline architecture.

### Fine-Tuning Cadence

| Volume | Action |
|--------|--------|
| < 100 pairs / week | No fine-tuning run |
| 100–1 000 pairs / week | LoRA fine-tune on SuperHub GPU (4h run) |
| > 1 000 pairs / week | Full fine-tune or LoRA on cloud instance |

### Consequences
- `Aku-Code-Editor` depends on `Aku-DaaS` for fine-tuning queue export.
- Fine-tuning pipeline must be built in DaaS (Phase 5 deliverable).
- Correction pairs must be anonymized before export (user ID re-hashed, inline comments stripped).
- A `model_registry` table in `akuai` schema tracks model versions and their provenance.

---

## Decision 3: Deployment Architecture

### Options Considered

**Option A — Cloud-only (no edge inference)**
- All inference routed to AkuAI on SuperHub/IGHub.
- Simple; no edge model management.
- **Rejected:** Breaks offline requirement. Rural schools have no internet.

**Option B — Edge-only (no cloud fallback)**
- All inference on Edge Hub local model.
- Maximally private; no cloud dependency.
- **Rejected:** Cloud-scale models provide better completions when connectivity is available. Students should benefit from better models when connected.

**Option C — Hybrid edge/cloud with fallback (chosen)**
- Online mode: delegate inference to AkuAI (which can use larger cloud models).
- Offline mode: use local CodeGemma-2B-Q4 GGUF.
- Mode controlled by `CODE_MODEL_PATH` env var:
  - Empty → delegate to AkuAI
  - Path set → local inference
- `OPERATING_MODE` from EdgeHub propagates to Code Editor at runtime.

### Decision

**Option C: Hybrid edge/cloud with `CODE_MODEL_PATH` toggle.**

**Rationale:**
- Best of both: maximum capability when connected, full offline when not.
- Single codebase — no separate cloud and edge service implementations.
- Consistent with AkuTutor's RAG fallback pattern (online cloud → offline edge index).

### Consequences
- AkuAI must support a code-specific `/api/v1/code/*` endpoint group routed to its code model.
- Edge Hub K3s deployment mounts a PVC with the GGUF file.
- Sync agent delivers model updates during connectivity windows.
- `CODE_MODEL_PATH` must be documented in all deployment configs.

---

## Consequences Summary

| Area | Impact |
|------|--------|
| AkuAI | Add second model slot (`CODE_MODEL_PATH`), code endpoint group, canary routing |
| Aku-DaaS | Add fine-tuning queue ingestion endpoint; anonymization pipeline |
| Aku-EdgeHub | Add model sync for GGUF files (SHA-256 verify + atomic activation) |
| Aku-SuperHub | Register Code Editor in service registry; propagate `OPERATING_MODE` |
| Postgres | New schema `code_editor` for correction pairs + session summaries |
| Redis DB 9 | CodeSession storage; no other service may use DB 9 |
| K8s | New PVC spec for model volume (Edge Hub only); standard 2-replica cloud deployment |

---

## Review & Revisit Triggers

This ADR should be revisited if:
- CodeGemma-2B is deprecated or its Apache 2.0 license changes.
- Edge Hub hardware is upgraded to support larger models (> 1.5 GB budget).
- Fine-tuning produces < 5% improvement in acceptance rate after 3 months (reconsider approach).
- A better edge-compatible code model becomes available.
