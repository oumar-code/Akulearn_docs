# Developer Onboarding Guide — Aku Platform

> **Last updated:** April 2026  
> **Audience:** New engineers joining the Aku Platform team

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Docker Desktop / Docker Engine | 24+ | https://docs.docker.com/get-docker/ |
| Docker Compose | v2.24+ | bundled with Docker Desktop |
| git | 2.40+ | https://git-scm.com/ |
| Python | 3.11+ | https://python.org |
| kubectl | 1.28+ | https://kubernetes.io/docs/tasks/tools/ |
| curl / httpie | any | for testing endpoints |

For macOS/Windows: **cap Docker Desktop RAM to 5 GB** (Settings → Resources → Memory). See [`dev-ram-allocation-decision.md`](../deployment/local/dev-ram-allocation-decision.md).

---

## 1. Clone the Repository

```bash
git clone https://github.com/oumar-code/Akulearn_docs.git
cd Akulearn_docs
```

---

## 2. Start the Dev Stack

### Option A — Infra + Core (recommended for daily dev)

```bash
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core up -d
```

### Option B — Add Code Editor

```bash
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core --profile editor up -d
```

### Option C — Full Stack (integration testing)

```bash
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core --profile full up -d
```

### Option D — With Observability

```bash
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core --profile monitoring up -d

# Open Grafana: http://localhost:3001 (admin / aku_dev_grafana)
# Open Prometheus: http://localhost:9090
```

---

## 3. Verify Services Are Healthy

```bash
# Check all containers
docker compose -f docs/deployment/local/docker-compose.dev.yml ps

# Health-check each service
for port in 8004 8005 8006 8007; do
  echo -n "Port $port: "; curl -sf http://localhost:$port/health || echo "UNHEALTHY"
done

# Neo4j browser: http://localhost:7474
# Postgres: psql -h localhost -U aku -d aku_platform -W
#   password: aku_dev
```

---

## 4. Service Port Map (Dev)

| Service | Host Port | Purpose |
|---------|-----------|---------|
| Postgres | 5432 | Relational DB |
| Redis | 6379 | Cache / sessions |
| Neo4j HTTP | 7474 | Graph browser UI |
| Neo4j Bolt | 7687 | Graph Bolt connection |
| AkuAI | 8004 | Inference engine |
| Akudemy | 8005 | Curriculum LMS |
| Aku-EdgeHub | 8006 | Edge orchestrator |
| AkuTutor | 8007 | RAG tutor |
| Aku-IGHub | 8008 | Idempotency gateway |
| Aku-SuperHub | 8009 | Central hub + JWT |
| AkuWorkspace | 8010 | AI productivity |
| Aku-Telhone | 8011 | eSIM management |
| Aku-DaaS | 8012 | Data-as-a-Service |
| Aku-Code-Editor | 8013 | AI code assistant |
| Prometheus | 9090 | Metrics |
| Grafana | 3001 | Dashboards |

---

## 5. Running Integration Tests

```bash
# Full stack must be running
docker compose -f docs/deployment/local/docker-compose.dev.yml \
  --profile infra --profile core --profile full --profile editor up -d

# Run contract tests
cd aku-platform-contracts
pytest tests/ -v

# Or use the CI workflow locally (act required: https://github.com/nektos/act)
act -j integration-test
```

---

## 6. Adding a New Service

1. **Create service repository** using the scaffold: `docs/service-migrations/bootstrap.sh`.
2. **Add to `docker-compose.dev.yml`**: add under the appropriate profile (`core`, `full`, or a new profile).
3. **Add K8s manifest**: copy `docs/deployment/k8s/akuai.yaml` as a template; update all names.
4. **Add secret template**: add a new section in `docs/deployment/k8s/secrets.yaml`.
5. **Register Redis DB**: claim the next available DB index in `docs/deployment/local/REDIS_KEY_TTL_POLICY.md`.
6. **Add Postgres schema**: define tables in `docs/deployment/local/postgres-schemas.md`.
7. **Add Prometheus scrape target**: add to `monitoring/prometheus.yml`.
8. **Register in Aku-SuperHub**: add to the service registry seed data.
9. **Update `mkdocs.yml`**: add the new service to the navigation.
10. **Write a runbook**: add `docs/runbooks/<service>-runbook.md`.

---

## 7. Key Documentation

| Topic | Document |
|-------|---------|
| 5-Phase sprint plan | [`docs/06-process-methodology/sprint-orchestration.md`](../06-process-methodology/sprint-orchestration.md) |
| Architecture overview | [`docs/01-architecture/index.md`](../01-architecture/index.md) |
| Redis TTL policy | [`docs/deployment/local/REDIS_KEY_TTL_POLICY.md`](../deployment/local/REDIS_KEY_TTL_POLICY.md) |
| Postgres schemas | [`docs/deployment/local/postgres-schemas.md`](../deployment/local/postgres-schemas.md) |
| Neo4j LO schema | [`docs/infra/neo4j-lo-schema.md`](../infra/neo4j-lo-schema.md) |
| Code Editor service | [`docs/services/aku-code-editor.md`](../services/aku-code-editor.md) |
| Code Editor ADR | [`docs/adrs/adr-005-aku-code-editor.md`](../adrs/adr-005-aku-code-editor.md) |
| RAG chatbot strategy | [`docs/strategy/rag_chatbot_strategy.md`](../strategy/rag_chatbot_strategy.md) |
| AIOps strategy | [`docs/AIOPS_STRATEGY.md`](../AIOPS_STRATEGY.md) |
| MLOps handbook | [`docs/handbooks/MLOps_AI_Engineering_Handbook.md`](../handbooks/MLOps_AI_Engineering_Handbook.md) |
| On-call playbook | [`docs/runbooks/on-call-playbook.md`](./on-call-playbook.md) |

---

## 8. Getting Help

- **Slack:** `#platform-engineering` for dev questions, `#platform-incidents` for P1/P2.
- **GitHub Discussions:** for architecture questions and RFC proposals.
- **ADRs:** check `docs/adrs/` for rationale behind key design decisions before asking why something was built a certain way.
