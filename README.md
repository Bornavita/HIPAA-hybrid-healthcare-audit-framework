# HIPAA Hybrid Healthcare Compliance & Audit Framework
**Organization:** Wellup Health System  
**Framework Baseline:** HIPAA Security Rule (45 CFR Part 160 & Part 164) & Privacy Rule (§ 164.502 / § 164.512)  
**Role:** Lead Security Compliance Assessor  

---

## Executive Summary

Wellup Health System operates a hybrid healthcare model linking on-premises Electronic Health Record (EHR) databases with AWS cloud infrastructure for medical record storage, telemetry, and analytics. 

This repository demonstrates an end-to-end **Security Compliance Assessor Workflow**:
1. **Infrastructure as Code (IaC):** Automated deployment of technical safeguards enforcing encryption, access control, and data immutability.
2. **Privacy Safeguard Engineering:** Implementation of the HIPAA *Minimum Necessary Rule* (§ 164.502(b)).
3. **Automated Evidence Collection:** Python audit engine verifying running cloud resources against HIPAA Technical Safeguards.
4. **Assessor Deliverables:** Security Risk Analysis (SRA), Control Traceability Matrix, and Corrective Action Plan (CAP).

---

## System Architecture

```text
[ Wellup Health On-Prem Datacenter ]
     │
     ├── PostgreSQL EHR Database (Encrypted at Rest)
     │    └── Minimum Necessary Masked Views (Clinician vs. Billing)
     │
     └── Simulated IPsec VPN Gateway
          │
          ▼
[ AWS Cloud Infrastructure (us-east-1) ]
     │
     ├── KMS Customer Managed Keys (CMK) ── Auto-Rotation Enabled
     │
     └── S3 ePHI Bucket ──────────────────── Object Lock (WORM) + KMS Enforced