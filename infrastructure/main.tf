terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Generate unique suffix for S3 bucket naming
resource "random_id" "suffix" {
  byte_length = 4
}

module "hipaa_kms" {
  source = "./modules/kms"
}

module "ephi_storage" {
  source      = "./modules/ephi_storage"
  bucket_name = "${var.hospital_name}-ephi-records-${random_id.suffix.hex}"
  kms_key_arn = module.hipaa_kms.key_arn
}

module "ephi_storage_test_noncompliant" {
  source      = "./modules/ephi_storage_noncompliant"
  bucket_name = "${var.hospital_name}-ephi-test-noncompliant-${random_id.suffix.hex}"
}