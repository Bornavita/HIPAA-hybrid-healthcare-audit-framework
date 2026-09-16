variable "bucket_name" { type = string }
variable "kms_key_arn" { type = string }

resource "aws_s3_bucket" "ephi_bucket" {
  bucket        = var.bucket_name
  force_destroy = false

  # Object Lock for WORM § 164.312(c)(2) Integrity
  object_lock_enabled = true

  tags = {
    Name               = var.bucket_name
    Organization       = "Wellup Health"
    DataClassification = "ePHI-Confidential"
    BAA_Covered        = "True"
    HIPAASafeguard     = "164.312.a.1"
  }
}

# Block all public access - Critical HIPAA Finding if missing
resource "aws_s3_bucket_public_access_block" "ephi_block_public" {
  bucket = aws_s3_bucket.ephi_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# KMS Encryption at Rest § 164.312(a)(2)(iv)
resource "aws_s3_bucket_server_side_encryption_configuration" "ephi_encryption" {
  bucket = aws_s3_bucket.ephi_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = var.kms_key_arn
      sse_algorithm     = "aws:kms"
    }
  }
}

# Versioning for Recovery § 164.308(a)(7)(ii)(A) Contingency Plan
resource "aws_s3_bucket_versioning" "ephi_versioning" {
  bucket = aws_s3_bucket.ephi_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.ephi_bucket.id
}