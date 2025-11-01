Infra examples

This folder contains small, opinionated examples for bootstrapping the Aku Platform infrastructure and services. They are minimal and intended as starting points — adapt variables, regions, and resource sizing to your environment.

Contents:

- `k8s/deployment.yaml` — simple Kubernetes Deployment + Service example (nginx placeholder for IG-Hub).
- `helm/aku-ig-hub/` — a minimal Helm chart scaffold for deploying the IG-Hub service.
- `terraform_ig_hub_vpc.tf` — example Terraform snippet for creating a VPC.
- `variables.tf` — recommended Terraform variables (create and adapt before apply).
- `data_sanitizer.py` — a simple PII anonymization script (use for prototyping only).
- `ig_hub_api.yaml` — OpenAPI sample for IG-Hub endpoints.
- `AkuDataInsights.tsx` — frontend example component that queries the Aku AI Assistant.

E2E demo

- `infra/examples/ig_hub_control_panel/` includes an IG-Hub control panel example. See its `README.md` for usage.
- `infra/examples/super_hub_simulator/` includes a Super Hub simulator that registers and publishes anonymized metadata. It can be run locally or by the CI e2e workflow.

How to adapt

1. Copy the Terraform example into a new folder and provide a `terraform.tfvars` with your cloud credentials and region.
2. Replace placeholder container images with your actual service images and push to your container registry.
3. Use the Helm chart as a starting point and add ingress, secrets, and ConfigMaps per environment.
4. Review `data_sanitizer.py` and integrate with your data governance pipeline; do not use it for production PII removal without policy review.

CI

There is a small workflow under `.github/workflows/ci-data-sanitizer.yml` that runs pytest on the `data_sanitizer.py` example to ensure the example functions as expected.
