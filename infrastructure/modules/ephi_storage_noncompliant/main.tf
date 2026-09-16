variable "bucket_name" { type = string }

resource "aws_s3_bucket" "test_bucket" {
  bucket        = var.bucket_name
  force_destroy = true

  tags = {
    Name    = var.bucket_name
    Purpose = "Intentional non-compliant test bucket for audit validation"
  }
}

# Deliberately NOT applying public access block, encryption, versioning,
# or object lock — this is meant to fail the audit on purpose.

output "bucket_name" {
  value = aws_s3_bucket.test_bucket.id
}