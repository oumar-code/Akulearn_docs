# infrastructure/

Purpose
-------
This folder is intended for production-grade infrastructure-as-code (IaC), provider-specific modules, and deployment manifests for the Aku Platform. It should contain Terraform modules, cloud provider configurations, and other artifacts that are intended to be used for real deployments.

Contents (expected)
-------------------
- `terraform/` — production-grade Terraform modules and variables
- `deploy/` — deployment scripts, CI deployment pipelines
- `k8s/` — manifests intended for production clusters

Why it's separate from `infra/`
--------------------------------
`infra/` holds examples, demo code, and lightweight manifests used for docs and CI. `infrastructure/` is for production automation. Keeping them separate reduces the risk that demo changes (which often evolve rapidly) affect production configuration.

If you maintain both in the same repository, please clearly document expected workflows and use branch protections and separate CI jobs for `infrastructure/` to avoid accidental deployments.
