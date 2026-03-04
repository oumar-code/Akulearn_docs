# Containerisation Guide

This document identifies all Aku Platform services that require containerisation, specifies their Docker image conventions, and describes the Kubernetes deployment strategy.

## Overview

All Aku Platform services are containerised using **Docker** and orchestrated with **Kubernetes** (K8s). This ensures:

- Independent deployment and scaling of each microservice
- Consistent environments across development, staging, and production
- Automated rollout and rollback via Kubernetes Deployments
- Resource isolation and limit enforcement per service

## Services Requiring Containerisation

### Core Backend Microservices

| Service | Container Name | Image Tag Pattern | Priority |
|---------|---------------|-------------------|----------|
| API Gateway | `aku-api-gateway` | `aku/api-gateway:<version>` | **Critical** |
| Authentication Service | `aku-auth` | `aku/auth:<version>` | **Critical** |
| Content Management Service | `aku-cms` | `aku/cms:<version>` | **Critical** |
| User Profile Service | `aku-user-profile` | `aku/user-profile:<version>` | **Critical** |
| AI/ML Service | `aku-ai-ml` | `aku/ai-ml:<version>` | High |
| Projector Sync Service | `aku-projector-sync` | `aku/projector-sync:<version>` | High |
| Blockchain Credentialing Service | `aku-blockchain` | `aku/blockchain:<version>` | High |
| Admin Portal Service | `aku-admin` | `aku/admin:<version>` | Medium |
| Telemetry & Analytics Service | `aku-telemetry` | `aku/telemetry:<version>` | Medium |

### Aku Platform Services

| Service | Container Name | Image Tag Pattern | Brand |
|---------|---------------|-------------------|-------|
| Aku Learn API | `aku-learn-api` | `aku/learn-api:<version>` | Akudemy |
| Aku Learn Sync Agent | `aku-learn-sync` | `aku/learn-sync:<version>` | Akudemy |
| Aku Learn AI Tutor | `aku-ai-tutor` | `aku/ai-tutor:<version>` | Akudemy |
| Aku eSIM Provisioning API | `telhone-provisioning-api` | `aku/esim-provisioning:<version>` | Telhone |
| Aku eSIM Policy Engine | `telhone-policy-engine` | `aku/esim-policy:<version>` | Telhone |
| Aku eSIM OTA Agent | `telhone-ota-agent` | `aku/esim-ota:<version>` | Telhone |
| Aku DaaS API | `aku-daas-api` | `aku/daas-api:<version>` | Aku Platform |
| Aku DaaS Governance | `aku-daas-governance` | `aku/daas-governance:<version>` | Aku Platform |
| Aku Workspace API | `aku-workspace-api` | `aku/workspace-api:<version>` | Aku Platform |
| Aku Workspace AI Assistant | `aku-ai-assistant` | `aku/ai-assistant:<version>` | Aku Platform |

### Infrastructure Services

These third-party services are also deployed as containers within the platform cluster:

| Service | Container Name | Upstream Image |
|---------|---------------|----------------|
| Kafka Broker | `aku-kafka` | `confluentinc/cp-kafka:<version>` |
| Zookeeper | `aku-zookeeper` | `confluentinc/cp-zookeeper:<version>` |
| PostgreSQL | `aku-postgres` | `postgres:<version>-alpine` |
| MongoDB | `aku-mongodb` | `mongo:<version>` |
| Redis | `aku-redis` | `redis:<version>-alpine` |
| MLflow | `aku-mlflow` | `ghcr.io/mlflow/mlflow:<version>` |
| Prometheus | `aku-prometheus` | `prom/prometheus:<version>` |
| Grafana | `aku-grafana` | `grafana/grafana:<version>` |

## Docker Image Conventions

All Aku-owned service images must follow these conventions:

1. **Base image:** Use official, minimal base images (e.g., `python:3.11-slim`, `node:20-alpine`).
2. **Non-root user:** Run the application as a non-root user inside the container.
3. **Labels:** Include standard OCI labels (`org.opencontainers.image.version`, `org.opencontainers.image.source`, `org.opencontainers.image.revision`).
4. **Health checks:** Define a `HEALTHCHECK` instruction in every `Dockerfile`.
5. **Multi-stage builds:** Use multi-stage builds to keep production images small and free of build dependencies.
6. **Secrets:** Never bake secrets into images. Use Kubernetes Secrets or a secrets manager (HashiCorp Vault / AWS Secrets Manager) mounted at runtime.

### Example Dockerfile (Python / FastAPI service)

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Production stage
FROM python:3.11-slim
LABEL org.opencontainers.image.source="https://github.com/oumar-code/Akulearn_docs"
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Kubernetes Deployment Strategy

### Namespace Layout

```
aku-system          — Platform-wide infrastructure (Kafka, Postgres, Redis)
aku-backend         — Core backend microservices
aku-learn           — Aku Learn / Akudemy service containers
aku-esim            — Aku eSIM / Telhone service containers
aku-daas            — Aku DaaS service containers
aku-workspace       — Aku Workspace service containers
aku-monitoring      — Prometheus, Grafana, alerting
```

### Deployment Guidelines

- **Replicas:** Production deployments use a minimum of 2 replicas for all stateless services.
- **Resource Limits:** Every container must declare `resources.requests` and `resources.limits`.
- **Rolling Updates:** Use `RollingUpdate` strategy with a `maxUnavailable: 1` and `maxSurge: 1`.
- **Liveness & Readiness Probes:** Required for every service to enable Kubernetes self-healing.
- **Horizontal Pod Autoscaler (HPA):** Configure HPA for all high-traffic services (API Gateway, CMS, AI/ML Service).
- **Persistent Volumes:** Use `PersistentVolumeClaims` for stateful services (PostgreSQL, MongoDB, Redis).

### Edge Hub Containerisation

Aku Edge Hubs run a lightweight container runtime (K3s) to host local service containers:

| Container | Purpose |
|-----------|---------|
| `aku-learn-sync` | Offline content sync |
| `aku-ai-tutor` | Local AI inference |
| `telhone-ota-agent` | eSIM OTA profile agent |
| `aku-edge-telemetry` | Local telemetry collector |

## CI/CD Pipeline for Container Images

1. **Build:** GitHub Actions builds Docker images on every push to `main` or a release tag.
2. **Test:** Container images are tested with unit and integration tests before push.
3. **Scan:** Images are scanned for vulnerabilities using Trivy (or equivalent).
4. **Push:** Verified images are pushed to the container registry (GitHub Container Registry / AWS ECR).
5. **Deploy:** Kubernetes manifests are updated (GitOps via Argo CD or Flux) to deploy the new image.

## Related Documents

- [`docs/01-architecture/index.md`](../01-architecture/index.md) — Architecture overview and microservices diagram
- [`docs/02-backend/index.md`](../02-backend/index.md) — Backend development handbook
- [`docs/services/aku-learn.md`](../services/aku-learn.md) — Aku Learn / Akudemy service
- [`docs/services/aku-esim.md`](../services/aku-esim.md) — Aku eSIM / Telhone service
- [`docs/services/aku-daas.md`](../services/aku-daas.md) — Aku DaaS service
- [`docs/services/aku-workspace.md`](../services/aku-workspace.md) — Aku Workspace service
