<!--
COPILOT_PROMPT:
Describe Transformer integration per-tier: on-device inference, federated fine-tuning at Super Hubs,
global model orchestration at IG-Hub. Include privacy guardrails and deployment checklist.
-->
# Transformer Integration Strategy for Aku Platform

<!-- Copilot: expand here -->

## Aku Workspace Consumption

Aku Workspace is a primary consumer of Transformer capabilities on the platform. The Workspace uses Transformers for NLU, NLG, summarization, and light-weight data transformation. Key considerations for Workspace consumption:

- Latency vs Privacy trade-off: Short, interactive requests should prefer local or Super Hub inference when possible. Techniques like model quantization, distillation, and small specialized models reduce latency on Edge Hubs.
- Context handling: Conversation context and user memory should be stored in the Contextual Memory Service with fine-grained retention and consent controls; only metadata or anonymized artifacts are forwarded for global fine-tuning.
- Fallback & orchestration: The Query Planner decides execution location. If an Edge Hub lacks capacity it falls back to Super Hub or IG-Hub; degraded modes should return cached or shorter responses.

## Hardware & Resource Integration

Transformers integration must be tightly coupled with resource management across tiers:

- Edge Hubs: Expect constrained CPU/GPU availability. Use model optimization (quantization, pruning, distillation) and tiny Transformer variants (e.g., distilled or adapter-based models). Caching and batching reduce inference overhead.
- Super Hubs: Provide modest GPU/accelerator pools for batched inference and federated fine-tuning. Super Hubs act as aggregation points for telemetry and intermediate training workloads.
- IG-Hub / Cloud: Hosts full-size models, heavy training/fine-tuning jobs, model registry, and experimentation platforms.

### Deployment Checklist (per model)

1. Register model in Model Registry with metadata (resource footprint, privacy labels, intended tier deployment).
2. Validate model with unit inference tests and safety checks (toxicity, hallucination tests where applicable).
3. Produce optimized artifacts for edge deployment (quantized weights, ONNX or TensorRT where supported).
4. Add rollout config (canary percent, target Super Hubs, telemetry thresholds).
5. Deploy to staging Super Hub cluster, monitor, then gradually roll out to Edge Hubs.

### Privacy & Federated Learning

When using federated or on-device learning, ensure contributions are differentially private, and agree on secure aggregation protocols. Only send model updates (gradients or weight deltas), never raw PII. Use the Data Governance microservice and Vault for key management.

---

See `docs/services/aku-workspace.md` for Workspace architecture and operational guidance.
