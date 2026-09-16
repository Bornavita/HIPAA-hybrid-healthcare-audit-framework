# Corrective Action Plan (CAP)

| Finding ID | Description | Risk | Remediation | Owner | Target Date | Status |
|---|---|---|---|---|---|---|
| CAP-001 | Test bucket `wellup-health-ephi-test-noncompliant-*` lacks public access block, encryption, and versioning | Critical | Apply `aws_s3_bucket_public_access_block`, KMS encryption, and versioning via Terraform module update | Bornavita | 2026-09-16 | Closed |