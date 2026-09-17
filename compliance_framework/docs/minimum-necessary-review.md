# Minimum Necessary Rule — Assessor Review
**HIPAA Reference:** § 164.502(b)
**Reviewed by:** Bornavita
**Date:** 16/09/2026

## Control Description
Access to the on-premises PostgreSQL EHR database is restricted through
role-based masked views. Application and analytics roles query these views
rather than the base tables, limiting exposed fields to only what each
role requires.

## Example masked view (illustrative)

```sql
CREATE VIEW analytics_patient_view AS
SELECT
    patient_id,
    admission_date,
    diagnosis_code
FROM patients;
-- Excludes: full_name, ssn, address, phone_number, dob
```

## Assessor Conclusion
Role-based views were manually reviewed against the analytics and clinical
application roles. Confirmed that no directly identifying fields are
exposed to the analytics role.

## Limitation
This control is verified through manual review, not through the automated
`hipaa_audit.py` scanner, since it operates at the database layer rather
than the AWS resource layer.