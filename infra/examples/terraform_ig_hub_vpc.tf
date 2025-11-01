// Example Terraform snippet: AWS VPC for Aku IG-Hub
// NOTE: This is a minimal example. Customize provider, region, and AZs to your environment.
provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "aku_ig_hub_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "aku-ig-hub-vpc"
  }
}

// Example: three public subnets
resource "aws_subnet" "public" {
  count                   = 3
  vpc_id                  = aws_vpc.aku_ig_hub_vpc.id
  cidr_block              = cidrsubnet(aws_vpc.aku_ig_hub_vpc.cidr_block, 8, count.index)
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  tags = {
    Name = "aku-ig-hub-public-${count.index}"
  }
}

// Example: three private subnets
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.aku_ig_hub_vpc.id
  cidr_block        = cidrsubnet(aws_vpc.aku_ig_hub_vpc.cidr_block, 8, 10 + count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags = {
    Name = "aku-ig-hub-private-${count.index}"
  }
}

data "aws_availability_zones" "available" {}

// The rest of the VPC (IGW, NAT, route tables) should be added per cloud best practices.
