# Aku Platform — Kubernetes Manifests

Raw Kubernetes manifests for deploying all 9 Aku Platform backend services to a staging or production cluster. Images are pulled from GHCR (`ghcr.io/oumar-code/<service>:<tag>`).

---

## Structure

```
docs/deployment/k8s/
├── README.md           ← this file
├── namespace.yaml      ← shared Namespace (aku-platform)
├── akuai.yaml          ← AkuAI: Deployment + Service + ConfigMap
├── akudemy.yaml        ← Akudemy
├── aku-edgehub.yaml    ← Aku-EdgeHub
├── aku-ighub.yaml      ← Aku-IGHub
├── aku-superhub.yaml   ← Aku-SuperHub
├── akututor.yaml       ← AkuTutor
├── akuworkspace.yaml   ← AkuWorkspace
├── aku-telhone.yaml    ← Aku-Telhone
└── aku-daas.yaml       ← Aku-DaaS
```

Each service manifest contains three resources separated by `---`:

| Resource | Purpose |
|----------|---------|
| `ConfigMap` | Non-sensitive environment variables (`APP_ENV`, `LOG_LEVEL`, service URL references) |
| `Deployment` | 2-replica deployment; env loaded from ConfigMap + a `<service>-secret` Secret |
| `Service` | ClusterIP — internal traffic only; external access goes through an Ingress or API gateway (Aku-IGHub) |

---

## Prerequisites

| Tool | Version |
|------|---------|
| kubectl | 1.28+ |
| Access to a Kubernetes cluster | (any CNCF-conformant cluster) |
| GHCR pull secret | see "Image Pull Secret" below |

---

## Quick Deploy (Staging)

```bash
# 1. Create namespace
kubectl apply -f docs/deployment/k8s/namespace.yaml

# 2. Create GHCR pull secret (one-time per namespace)
kubectl create secret docker-registry ghcr-pull-secret \
  --namespace aku-platform \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<github-pat-with-read:packages>

# 3. Create service secrets (adjust values before running)
#    Each service expects a Secret named <service>-secret with keys:
#      DATABASE_URL, REDIS_URL, and any service-specific API keys.
#    Example for AkuAI:
kubectl create secret generic akuai-secret \
  --namespace aku-platform \
  --from-literal=DATABASE_URL="postgresql+asyncpg://akuai:CHANGE_ME@postgres:5432/akuai" \
  --from-literal=REDIS_URL="redis://redis:6379/2" \
  --from-literal=AKUAI_API_SECRET="CHANGE_ME_IN_PRODUCTION"

# 4. Apply all service manifests
kubectl apply -f docs/deployment/k8s/

# 5. Verify pods are running
kubectl get pods -n aku-platform

# 6. Check a service health endpoint (via port-forward)
kubectl port-forward -n aku-platform svc/akuai 8004:80
curl http://localhost:8004/health
```

---

## Image Tags

All manifests default to `v0.1.1`. To deploy a different tag, patch the Deployment:

```bash
# Patch a single service image tag
kubectl set image deployment/akuai \
  akuai=ghcr.io/oumar-code/akuai:v0.1.2 \
  -n aku-platform

# Or update the image tag in-place (sed) before applying:
sed 's|:v0.1.1|:v0.1.2|g' docs/deployment/k8s/akuai.yaml | kubectl apply -f -
```

---

## Image Pull Secret

All `Deployment` specs reference `imagePullSecrets: [{name: ghcr-pull-secret}]`. Create this secret once per namespace:

```bash
kubectl create secret docker-registry ghcr-pull-secret \
  --namespace aku-platform \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<github-pat-with-read:packages>
```

---

## Service Port Map

| Service | Container Port | K8s Service Port |
|---------|---------------|-----------------|
| AkuAI | 8004 | 80 |
| Akudemy | 8000 | 80 |
| Aku-EdgeHub | 8000 | 80 |
| Aku-IGHub | 8000 | 80 |
| Aku-SuperHub | 8000 | 80 |
| AkuTutor | 8002 | 80 |
| AkuWorkspace | 8004 | 80 |
| Aku-Telhone | 8001 | 80 |
| Aku-DaaS | 8001 | 80 |

All Services expose port **80** externally (within the cluster) and forward to the container port. This lets services call each other on `http://<service-name>.<namespace>.svc.cluster.local/api/v1/...`.

---

## Secrets Reference

Each service Deployment mounts a `<service>-secret` Secret. The required keys are:

| Service | Required Secret Keys |
|---------|---------------------|
| **AkuAI** | `DATABASE_URL`, `REDIS_URL`, `AKUAI_API_SECRET` |
| **Akudemy** | `DATABASE_URL`, `REDIS_URL` |
| **Aku-EdgeHub** | `DATABASE_URL`, `REDIS_URL` |
| **Aku-IGHub** | `DATABASE_URL`, `REDIS_URL`, `IGHUB_JWT_SECRET` |
| **Aku-SuperHub** | `DATABASE_URL`, `REDIS_URL` |
| **AkuTutor** | `DATABASE_URL`, `REDIS_URL` |
| **AkuWorkspace** | `DATABASE_URL`, `REDIS_URL` |
| **Aku-Telhone** | `DATABASE_URL`, `REDIS_URL` |
| **Aku-DaaS** | `DATABASE_URL`, `REDIS_URL` |

> **Never commit real secret values to this repository.** Use `kubectl create secret` or a secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager) to inject secrets at deploy time.

---

## Updating Manifests

After each new release tag:

1. Update the `image:` tag in every `Deployment` spec.
2. Add any new environment variables to the relevant `ConfigMap`.
3. Run `kubectl apply -f docs/deployment/k8s/` to apply changes.

For production, consider using **Kustomize overlays** or **Helm** to manage environment-specific values on top of these base manifests.
