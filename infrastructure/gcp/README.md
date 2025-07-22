# Akulearn GCP Infrastructure (Terraform)

This directory contains Terraform code to provision robust, scalable, and secure infrastructure for Akulearn on Google Cloud Platform (GCP).

## Structure
- `main.tf`: Provider, project, and core service setup
- `network.tf`: VPC, subnets, and firewall rules
- `gke.tf`: Google Kubernetes Engine (GKE) cluster for backend
- `sql.tf`: Cloud SQL for PostgreSQL (HA, private IP)
- `storage.tf`: Cloud Storage bucket for frontend static hosting (with CDN)
- `ai.tf`: Vertex AI endpoint/model registry placeholder
- `monitoring.tf`: Monitoring dashboard and logging sinks
- `iam.tf`: Custom IAM roles and service accounts
- `variables.tf`: All configurable variables
- `outputs.tf`: Key resource outputs

## Usage

1. **Install Terraform** (>= 1.3.0) and authenticate with GCP (`gcloud auth application-default login`).
2. Edit `variables.tf` to set your `project_id`, `region`, and allowed SSH IPs.
3. Initialize Terraform:
   ```sh
   terraform init
   ```
4. Review the plan:
   ```sh
   terraform plan
   ```
5. Apply the configuration:
   ```sh
   terraform apply
   ```

## Security Notes
- No secrets are hardcoded; DB passwords are auto-generated.
- IAM roles follow least-privilege principles.
- All resources are named for clarity and future scaling.

## Expansion
- Vertex AI resources are placeholders for future model deployment.
- Easily extendable for multi-region, multi-environment setups.

---

For questions, contact the Akulearn DevOps team.
