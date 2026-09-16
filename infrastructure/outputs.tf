output "ephi_s3_bucket" {
  description = "Name of the ePHI S3 Bucket"
  value       = module.ephi_storage.bucket_name
}

output "kms_key_arn" {
  description = "ARN of the KMS Key"
  value       = module.hipaa_kms.key_arn
}