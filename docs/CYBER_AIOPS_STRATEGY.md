# Cyber AIops Strategy for Akulearn — Security & Log Observability

## Executive Summary
This document outlines an AIops approach for cybersecurity monitoring of the Akulearn platform and logs. The goal: detect faults and security incidents quickly and reliably using automated log ingestion, feature extraction, anomaly detection, enrichment, alerting, and runbooks for responders.

---

## Principles
- Automation-first: automated ingestion, detection, triage and remediation suggestions.
- Observability: instrument apps to emit structured logs, traces, and metrics.
- Defense-in-depth: combine rule-based detections, signature checks and ML anomaly detection.
- Explainability: provide reasons/context for each alert to accelerate response.
- Privacy & compliance: redact PII in logs, keep audit trails, and control retention.

---

## Log Sources
- Application logs (FastAPI, workers)
- Access logs (API gateway, reverse proxy)
- Authentication logs (auth_service)
- Infrastructure logs (k8s, systemd, cloud provider)
- Network device logs (firewalls, load balancers)
- Telemetry & metrics (Prometheus)
- Audit logs (DB, admin actions)

---

## Architecture Overview

1. Log Collection
   - Agents: Filebeat/Fluent Bit for log shipping
   - Structured logging (JSON) from services
2. Ingestion & Storage
   - Centralized: Elasticsearch / OpenSearch or log lake (S3 + Parquet) + metadata DB
   - Short-term hot store for real-time detection, long-term cold store for forensics
3. Feature Extraction & Enrichment
   - Parse timestamps, levels, service, user, IP, response codes
   - Enrich with geo-IP, user metadata, asset tags
   - Create derived metrics (rate, error ratio) per host/service
4. Detection Layer
   - Rule Engine (Alerting rules for known bad patterns)
   - ML Anomaly Detector (IsolationForest / Autoencoder / streaming models)
   - Signature matching (YARA-like patterns for suspicious payloads)
5. Triage & Scoring
   - Score alerts by severity using signal fusion (rules + ML + asset criticality)
   - Add context: recent changes, related traces, last deploy, correlated alerts
6. Response & Playbooks
   - Auto-notifications (PagerDuty, Slack, email)
   - Auto-isolation steps for high-confidence incidents (e.g., block IP)
   - Human-operated runbooks for investigation and remediation
7. Monitoring & Feedback
   - Track false positives/negatives and retrain ML models
   - MLflow for model versioning and experiments

---

## Detection Strategy
- Hybrid approach:
  - Fast rules for known alarms (authentication brute-force, SQL errors, high HTTP 5xx rate)
  - ML anomaly detection for novel patterns (spikes in error context, unusual user activity)
- Multi-time-window analysis: per-minute alerting + hourly trend analysis
- Streaming detection for real-time alerts using Kafka / Pulsar; batch re-scoring for enrichment

---

## Feature Engineering (Logs -> Features)
- Temporal: time-of-day, inter-arrival time, event frequency per entity
- Categorical: service, endpoint, log level, user role
- Numeric: response time, payload size, status code bucket counts
- Text: TF-IDF / embeddings of log message or stack traces
- Sessionization: group events into sessions by user or IP

---

## ML Techniques (Prototype to Production)
- Prototype: IsolationForest on TF-IDF vectors of messages + simple numeric features
- Improved: Autoencoders on embeddings (sentence-transformers) + numeric features
- Advanced: Graph-based detection (user ↔ host ↔ process graphs) with GNN anomaly scoring
- Evaluate with historical incidents, synthetic anomalies, and labeled data when available

---

## Alerting & Scoring
- Each detection produces an alert containing:
  - Score (0-1), contributing features, examples from the time window, correlated alerts
- Severity mapping by score + asset criticality
- Deduplication and grouping to reduce noise
- Escalation rules (e.g., high severity → immediate pager)

---

## Runbooks & Playbooks
- Standard playbooks for: authentication failures, DB errors, data exfiltration suspicion, service outage
- Include: first checks, commands, evidence to collect, communication steps, rollback actions
- Attach automated remediation (lock account, restrict network) for confirmed incidents

---

## Observability & Instrumentation
- Structured logs (JSON) with consistent schema: timestamp, service, env, level, trace_id, user_id, request_id
- Correlate logs with traces and metrics using `trace_id` and `request_id`
- Sanitize logs for PII: apply client-side redaction or pipeline sanitizer

---

## Metrics and KPIs
- Mean time to detect (MTTD) — target: < 2 mins for critical incidents
- Mean time to respond (MTTR) — target: < 30 mins
- False positive rate — keep under 10% after tuning
- Alerts per day per engineer — keep manageable (< 50)
- Detection coverage of known incident types — target > 95%

---

## Roadmap (First 8 weeks)
1. Week 1: Instrumentation & log collection (Fluent Bit + structured logs)
2. Week 2: Central ingestion store + live dashboards (ELK / OpenSearch or log lake)
3. Week 3: Rule-based detections + alerting (Prometheus, ElastAlert, or builtin alerts)
4. Week 4: Prototype ML anomaly detector (IsolationForest on sample logs)
5. Week 5: Integrate detector with alert pipeline and triage dashboard
6. Week 6: Add enrichment (geoIP, asset tags) and reduce noise
7. Week 7: Train/validate model with labeled events, begin retraining pipeline
8. Week 8: Productionize (autoscaling, monitoring, runbooks, on-call integration)

---

## Tools & Stack Recommendations
- Collection: Fluent Bit, Filebeat
- Streaming: Kafka / Pulsar (optional)
- Storage: OpenSearch/Elasticsearch or S3 (Parquet) + metadata store
- Processing: Spark / Flink for batch/stream enrichment, lightweight Python microservices for near-real-time
- ML: scikit-learn, PyTorch, sentence-transformers, MLflow
- Visualization: Kibana / Grafana
- Alerting: Prometheus Alertmanager, ElastAlert, PagerDuty, Slack

---

## Quick Prototype Plan (IsolationForest)
- Input: structured log lines (timestamp, level, service, message)
- Text vectorization: TF-IDF over messages (or sentence embeddings)
- Combine with numeric/time features
- Train IsolationForest on baseline normal logs
- Score new events; alert top-k anomalies per time window

---

## Privacy & Compliance
- Mask PII before storing logs
- Maintain role-based access for logs and models
- Retention policies for logs and model training data

---

## Next Steps
- Implement collection & staging environment for logs
- Create `mlops/cyber_aiops_detector.py` prototype and demo notebook
- Run smoke tests with sample logs and refine features
- Create alert playbooks and integrate with Slack/PagerDuty

