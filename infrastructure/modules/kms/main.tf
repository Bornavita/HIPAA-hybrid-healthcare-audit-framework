resource "aws_kms_key" "hipaa_cmk" {
  description             = "Wellup Health KMS CMK for encrypting ePHI and HIPAA audit logs"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name               = "wellup-health-hipaa-ephi-kms-key"
    Organization       = "Wellup Health"
    DataClassification = "ePHI-Confidential"
    HIPAASafeguard     = "164.312.a.2.iv"
  }
}

resource "aws_kms_alias" "hipaa_cmk_alias" {
  name          = "alias/wellup-health-hipaa-ephi-key"
  target_key_id = aws_kms_key.hipaa_cmk.key_id
}

output "key_arn" {
  value = aws_kms_key.hipaa_cmk.arn
}