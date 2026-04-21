# AIOps Strategy

## Objective
Establish an AIOps operating model for Akulearn that improves reliability, security, and learning outcomes by combining observability, automation, and AI-assisted incident operations.

## Scope
- Platform services: Aku-EdgeHub, Aku-SuperHub, Aku-IGHub, AkuAI, AkuTutor, Akudemy, AkuWorkspace, Aku-Telhone.
- Environments: pilot, staging, production.
- Workloads: APIs, content ingestion, model inference, sync jobs, and dashboards.

## Principles
1. **Reliability first**: prioritize student-facing uptime and low-latency learning experiences.
2. **Automate repeatable work**: detection, triage, rollback, and runbook execution.
3. **Human-in-the-loop**: AI proposes actions; operators approve high-impact changes.
4. **Data governance by default**: preserve privacy, lineage, and auditability.
5. **Continuous learning**: turn incidents into improved rules, prompts, and playbooks.

## Operating Model

### 1) Observe
Collect and centralize:
- Metrics: availability, latency, throughput, error rates, queue depth, model inference time.
- Logs: structured application logs with trace IDs.
- Traces: service-to-service request paths.
- Events: deployments, schema changes, model version changes, feature flags.

### 2) Detect
- Rule-based alerts for known thresholds (SLO/SLA violations).
- AI anomaly detection for traffic shifts, drift, and unusual failure patterns.
- Alert suppression and deduplication to reduce noise.

### 3) Diagnose
- Correlate alerts with recent deploys, model updates, and infra changes.
- Use AI-assisted root-cause hints from traces/log clusters.
- Prioritize incidents by user impact and blast radius.

### 4) Act
- Automated low-risk remediations:
  - Restart unhealthy pods/services.
  - Scale workers for queue backlogs.
  - Roll back last deployment on severe regression.
- Human approval required for data/schema destructive actions.

### 5) Learn
- Post-incident review with action items.
- Convert findings into updated runbooks, detectors, and guardrails.
- Feed incident patterns back into alert tuning and AI triage prompts.

## AIOps Architecture (Logical)
1. **Telemetry Layer**: OpenTelemetry + Prometheus-compatible metrics + centralized logs.
2. **Event Layer**: deploy/model/config events from CI/CD and service control planes.
3. **Intelligence Layer**:
   - Anomaly detectors
   - Log clustering and change-point detection
   - Incident summarizer and triage assistant
4. **Automation Layer**: runbook orchestrator (safe actions), ticketing, on-call routing.
5. **Governance Layer**: policy engine, approvals, audit trail, and compliance records.

## SLOs and Error Budgets
Define service-level objectives by service tier:
- **Tier 1 (student-critical APIs)**: 99.9% availability, p95 latency targets by endpoint.
- **Tier 2 (content and sync jobs)**: completion-time and freshness SLOs.
- **Tier 3 (analytics/reporting)**: dashboard freshness and query latency targets.

Use error budgets to govern deployment velocity and model promotion.

## Incident Lifecycle
1. Alert created and deduplicated.
2. AI triage generates probable cause + impacted services.
3. On-call receives severity-ranked incident card.
4. Automated remediation executes where policy allows.
5. Operator confirms recovery and closes incident.
6. Postmortem updates runbooks and detectors.

## Governance and Security Controls
- Role-based access for operational actions.
- Prompt and model response logging for auditability.
- PII masking/redaction in logs and AI context windows.
- Segregated environments for experimentation vs production.
- Change-management gates for model and rule updates.

## Rollout Plan
### Phase 1: Baseline Visibility
- Standardize service telemetry and SLO dashboards.
- Implement alert routing and on-call ownership.

### Phase 2: AI-Assisted Triage
- Add anomaly detection and incident summarization.
- Start with read-only recommendations.

### Phase 3: Safe Automation
- Enable low-risk auto-remediation runbooks.
- Add approval workflows for high-impact operations.

### Phase 4: Closed-Loop Optimization
- Feed incident outcomes into detector tuning.
- Introduce reliability scorecards by service/team.

## KPIs
- MTTD (Mean Time To Detect)
- MTTR (Mean Time To Restore)
- Alert noise ratio (actionable vs non-actionable)
- Incident recurrence rate
- Change failure rate
- Student-facing uptime and performance

## Definition of Done
AIOps implementation is considered operational when:
- Core services emit standardized telemetry.
- SLO dashboards and incident workflows are active.
- AI triage is used in production incidents.
- At least one approved safe auto-remediation path is live.
- Postmortem feedback loop updates rules/runbooks continuously.
