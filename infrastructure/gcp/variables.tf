variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "Primary region for resources"
  type        = string
  default     = "europe-west1"
}

variable "ssh_source_ranges" {
  description = "Allowed source IPs for SSH access"
  type        = list(string)
  default     = ["YOUR_IP_ADDRESS/32"]
}
