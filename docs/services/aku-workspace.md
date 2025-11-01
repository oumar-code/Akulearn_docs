<!--
COPILOT_PROMPT:
Create a comprehensive Aku Workspace service document: vision, user scenarios, core components, backend integration, data flows, MLOps & model lifecycle, security/privacy, deployment & rollout plan, metrics, and known challenges.
-->
# Aku Workspace

## Vision

Aku Workspace is the AI-native productivity layer of the Aku Platform. It provides natural-language-driven tools for document creation, data analysis, communication, and lightweight automation. The Workspace exposes an Aku AI Assistant that orchestrates distributed compute across Edge Hubs, Super Hubs, and the IG-Hub to deliver low-latency, privacy-preserving intelligence to users in constrained connectivity environments.

## Primary User Scenarios

- Natural-language data queries (Aku Data Insights): ask questions like "show attendance trends for School X" and receive charts and summaries.
- Document generation and summarization (Aku Docs): create lesson plans, summaries, and student feedback from prompts.
- Conversational workflows: tutoring dialogs, task automation, and guided forms.
- Collaborative editing and sharing with synchronized local caching for offline access.

## Core Components

- Aku AI Assistant: central orchestration and NLU/NLG engine (may call external LLMs or local inference).
- Contextual Memory Service: stores conversation context and short-term memory with strict retention policies.
- Query Planner / Orchestrator: decides where to run inference (edge/superhub/cloud) based on latency, cost, and privacy policies.
- Workspace Frontend: web/desktop/mobile UI components for Aku Data Insights, Aku Docs, and collaboration.
- Security & Privacy Layer: encryption, access control, consent, and anonymization hooks.

## Backend Integration

- Identity and Access: integrates with IG-Hub IdP for user authentication and role-based access control.
- Data Access: queries DaaS APIs (via Super Hubs / IG-Hub) to fetch anonymized datasets when allowed.
- Model Registry & Serving: integrates with model registry (MLflow or cloud provider) for model versioning, and K8s-based inference services for serving.
- Telemetry & Monitoring: hooks into platform telemetry (Prometheus/Grafana, OpenTelemetry) for latency, error rates, and model performance monitoring.

## MLOps & Model Lifecycle

- Model Registry: all models used by Aku Workspace MUST be registered with metadata: version, lineage, training data provenance, privacy labels, resource requirements.
- Experiment Tracking: each fine-tune or experiment must be tracked (MLflow or equivalent) and have reproducible training artifacts.
- CI/CD for Models: models pass automated unit tests, integration tests (small inference runs), and safety checks before promoted to staging/production.
- Canary & Rollout: support for gradual rollout at Super Hub or IG-Hub level with monitoring and automatic rollback on anomalies.

## Data Flow (Typical Query)

1. User issues a natural-language query in Workspace UI.
2. Request is authenticated and enriched with user/context metadata.
3. Query Planner checks privacy policy, local caches, and decides an execution plan.
4. If permitted & low-latency required, inference is executed at the nearest Edge Hub (local model) or Super Hub; otherwise routed to IG-Hub or cloud provider.
5. Results are post-processed, persisted if needed (with anonymization), and returned to the user.

## Security & Privacy

- Data Minimization: default behavior is to avoid sending raw PII off-device. Use the Data Governance microservice to sanitize any records.
- Consent & Access Controls: workspace actions that access sensitive datasets require explicit user consent and role checks.
- Encryption: TLS for transport; field-level encryption for sensitive persisted artifacts.
- Audit Logging: all model invocations, data accesses, and policy decisions are logged for audit (with PII obfuscated where appropriate).

## Deployment & Rollout Plan (MVP -> Scale)

- MVP: Host core NLU at IG-Hub with a lightweight local fallback at Edge Hubs for critical paths.
- Pilot: Deploy Workspace to a small set of schools/regions; collect telemetry and user feedback.
- Scale: Gradually replicate inference and caching logic to Super Hubs and Edge Hubs; optimize models for edge resource constraints.

## Observability & Metrics

- Latency (end-to-end), success/error rates, model accuracy metrics (as applicable), resource utilization (CPU/GPU/memory), and user engagement metrics.

## Challenges & Mitigations

- Intermittent connectivity: mitigate via aggressive caching, offline-first UI, and resumable uploads.
- Model size vs edge resources: mitigate via quantization, distillation, and offloading heavier workloads to Super Hubs.
- Data privacy: robust policy enforcement and strict data minimization.

---

For implementation examples (IaC, API schemas, example microservices), see the `infra/examples/` folder in the repo.
