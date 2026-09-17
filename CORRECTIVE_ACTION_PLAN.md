# Corrective Action Plan (CAP)

| Finding ID | Description | Risk | Remediation | Owner | Target Date | Status |
|---|---|---|---|---|---|---|
| CAP-001 | Test bucket `wellup-health-ephi-test-noncompliant-*` lacks public access block, encryption, and versioning | Critical | Apply KMS encryption and versioning via Terraform module update; re-scan to confirm | Bornavita | 2026-09-16 | **Open** |