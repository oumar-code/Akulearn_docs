variable "aws_region" {
  description = "AWS region for IG-Hub VPC"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the IG-Hub VPC"
  type        = string
  default     = "10.0.0.0/16"
}
