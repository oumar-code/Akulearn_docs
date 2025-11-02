# infra/

Purpose
-------
This folder contains example infrastructure manifests, Helm charts, Terraform variables, and quick-start guides used by the documentation and CI for running example services locally or in CI (for example, the IG‑Hub example, DaaS mock, and Super Hub simulator).

Contents
--------
- `examples/` — small example services (FastAPI examples, simulators, DaaS mock)
- `k8s/` — example Kubernetes manifests used for local testing in CI
- `helm/` — Helm chart scaffolds for demo deployments

How this differs from `infrastructure/`
-------------------------------------
- `infra/` is intentionally lightweight and contains examples and dev/demo manifests used by docs, CI jobs, and local testing.
- `infrastructure/` may contain production-grade deployment code, Terraform state, and cloud provider-specific modules. If you maintain production-level IaC, keep it in `infrastructure/` to avoid accidental modification from doc/demo updates.

Recommendation
--------------
If you're working on demos, tests, or documentation that explain how to deploy example services, use `infra/`. If you are building production-level automation (Terraform, cloud modules, deployment pipelines), use `infrastructure/` and clearly document the intended environment.
