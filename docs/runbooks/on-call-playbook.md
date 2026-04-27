# On-Call Playbook — Aku Platform

> **Last updated:** April 2026  
> **Owner:** Platform Engineering  
> **Related:** [`AIOPS_STRATEGY.md`](../AIOPS_STRATEGY.md) · [`monitoring/kpi_dashboard_spec.md`](../monitoring/kpi_dashboard_spec.md)

---

## Incident Severity Levels

| Severity | Definition | Response time | Examples |
|----------|-----------|--------------|---------|
| **P1** | Student-facing service completely down | < 15 min | AkuAI down, AkuTutor all requests failing, Akudemy unavailable |
| **P2** | Degraded performance affecting students | < 30 min | Latency p95 > 2× SLO, error rate > 5% |
| **P3** | Non-critical degradation | < 2 h | Background job delayed, non-critical endpoint slow |
| **P4** | Informational / potential future issue | Next business day | Metric trending toward SLO breach, log anomalies |

---

## Incident Lifecycle

```
Alert fires
    │
    ▼
1. Triage — AI-assisted probable cause + impacted services
    │
    ▼
2. Acknowledge — on-call claims incident
    │
    ▼
3. Assess blast radius — how many students affected?
    │
    ▼
4. Remediate
    ├── Low-risk: auto-remediation (restart pod, scale worker, flush cache)
    └── High-risk: requires human approval (DB migration, model rollback)
    │
    ▼
5. Confirm recovery — health endpoints green, SLO metrics recovering
    │
    ▼
6. Close incident + schedule postmortem
    │
    ▼
7. Postmortem → update runbooks / detectors
```

---

## On-Call Responsibilities

- Monitor Grafana dashboards (link in team wiki) during your rotation.
- Acknowledge PagerDuty/OpsGenie alerts within SLA.
- Execute safe remediations from this playbook without escalation.
- Escalate to engineering lead for destructive actions (DB changes, schema migrations, infra changes).
- File a postmortem for all P1 and P2 incidents within 48 hours.

---

## Service Tier Map

| Tier | Services | SLO |
|------|---------|-----|
| Tier 1 (student-critical) | AkuAI, AkuTutor, Aku-EdgeHub, Aku-Code-Editor | 99.9% availability, latency SLOs |
| Tier 2 (content & sync) | Akudemy, Aku-DaaS | Completion time + freshness SLOs |
| Tier 3 (platform) | Aku-SuperHub, Aku-IGHub, AkuWorkspace, Aku-Telhone | Dashboard freshness, query latency |

---

## Common Remediations

### Restart an unhealthy pod (K8s)

```bash
# Safe — Kubernetes will start a new pod before terminating the old one
kubectl rollout restart deployment/<service-name> -n aku-platform

# Verify recovery
kubectl rollout status deployment/<service-name> -n aku-platform
```

### Scale up workers for queue backlog

```bash
# Temporarily scale up DaaS workers
kubectl scale deployment/aku-daas --replicas=4 -n aku-platform

# Return to normal after backlog clears
kubectl scale deployment/aku-daas --replicas=2 -n aku-platform
```

### Rollback last deployment

```bash
kubectl rollout undo deployment/<service-name> -n aku-platform
kubectl rollout status deployment/<service-name> -n aku-platform
```

### Flush Redis cache for a service (last resort)

```bash
# CAUTION: flushes ALL keys in the service's Redis DB
# Requires human approval for Tier 1 services
kubectl exec -it redis-pod -n aku-platform -- redis-cli -n <db-index> FLUSHDB

# DB index reference:
# 2=AkuAI, 3=Akudemy, 4=EdgeHub, 5=IGHub, 6=SuperHub
# 7=Workspace, 8=DaaS, 9=CodeEditor, 10=Telhone
```

---

## Alert Reference

| Alert name | Meaning | Runbook |
|-----------|---------|---------|
| `AkuAIDown` | AkuAI health check failing | [`akuai-runbook.md`](./akuai-runbook.md) |
| `AkuTutorHighLatency` | AkuTutor p95 > 1 500 ms | Check EdgeHub RAG + AkuAI inference |
| `CodeEditorHighLatency` | Code Editor p95 > 800 ms | Check AkuAI code model; scale if needed |
| `CodeEditorLowAcceptanceRate` | Acceptance rate < 30% for 24h | Review fine-tune; check model version |
| `RedisMemoryPressure` | Redis memory > 80% of `maxmemory` | Investigate key growth; scale Redis |
| `AkudemyContentFreshness` | Content chunks > 48h behind cloud | Check sync agent; restart if stuck |
| `DaaSPipelineStuck` | Ingestion job running > 2× expected time | Check DaaS logs; restart job if safe |

---

## Postmortem Template

```
## Incident Postmortem — <Service> — <Date>

**Severity:** P1 / P2 / P3
**Duration:** <start> → <end> (<total minutes>)
**Impact:** <number of students/requests affected>

### Timeline

| Time (UTC) | Event |
|-----------|-------|
| HH:MM | Alert fired |
| HH:MM | On-call acknowledged |
| HH:MM | Root cause identified |
| HH:MM | Remediation applied |
| HH:MM | Service recovered |

### Root Cause

<Describe the root cause in plain language.>

### Contributing Factors

<What conditions made this possible or worse?>

### Resolution

<What was done to resolve the incident?>

### Action Items

| Item | Owner | Due date |
|------|-------|---------|
| Add alert for X | @engineer | <date> |
| Update runbook for Y | @engineer | <date> |

### Lessons Learned

<What did we learn? What should we do differently?>
```

---

## Escalation Contacts

| Role | When to escalate |
|------|-----------------|
| Engineering Lead | Destructive DB/schema actions; P1 unresolved > 30 min |
| AI/ML Lead | Model quality degradation; fine-tune failure |
| Platform Security | Suspected security incident; harmful code detections spike |
| Product Lead | P1 during active pilot deployment |
