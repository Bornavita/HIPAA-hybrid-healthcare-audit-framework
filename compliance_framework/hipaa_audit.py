import boto3
import csv
import os
from datetime import datetime, timezone
from botocore.exceptions import ClientError

def audit_hipaa_s3_controls():
    s3_client = boto3.client('s3')
    kms_client = boto3.client('kms')
    buckets = s3_client.list_buckets()['Buckets']

    audit_results = []
    timestamp = datetime.now(timezone.utc).isoformat()

    print("====================================================")
    print(" WELLUP HEALTH - HIPAA TECHNICAL SAFEGUARDS AUDIT ")
    print(f" Run at: {timestamp}")
    print("====================================================\n")

    for bucket in buckets:
        name = bucket['Name']
        if "wellup-health" not in name:
            continue

        print(f"[*] Auditing ePHI Bucket: {name}")
        notes = []

        # 1. Test SS 164.312(a)(1) - Public Access Block
        try:
            pab = s3_client.get_public_access_block(Bucket=name)['PublicAccessBlockConfiguration']
            public_blocked = all([
                pab.get('BlockPublicAcls', False),
                pab.get('IgnorePublicAcls', False),
                pab.get('BlockPublicPolicy', False),
                pab.get('RestrictPublicBuckets', False)
            ])
        except ClientError as e:
            public_blocked = False
            notes.append(f"PublicAccessBlock check failed: {e.response['Error']['Code']}")

        # 2. Test SS 164.312(a)(2)(iv) - KMS Encryption + Key Rotation
        encrypted = False
        rotation_enabled = False
        try:
            enc = s3_client.get_bucket_encryption(Bucket=name)
            rules = enc['ServerSideEncryptionConfiguration']['Rules']
            kms_key_id = None
            for r in rules:
                sse = r['ApplyServerSideEncryptionByDefault']
                if sse['SSEAlgorithm'] == 'aws:kms':
                    encrypted = True
                    kms_key_id = sse.get('KMSMasterKeyID')

            if encrypted and kms_key_id:
                try:
                    rotation_status = kms_client.get_key_rotation_status(KeyId=kms_key_id)
                    rotation_enabled = rotation_status.get('KeyRotationEnabled', False)
                except ClientError as e:
                    notes.append(f"KMS rotation check failed: {e.response['Error']['Code']}")
        except ClientError as e:
            notes.append(f"Encryption check failed: {e.response['Error']['Code']}")

        # 3. Test SS 164.312(c)(1) - Object Lock (WORM / Integrity)
        try:
            lock = s3_client.get_object_lock_configuration(Bucket=name)
            worm_enabled = lock['ObjectLockConfiguration']['ObjectLockEnabled'] == 'Enabled'
        except ClientError as e:
            worm_enabled = False
            notes.append(f"ObjectLock check failed: {e.response['Error']['Code']}")

        # 4. Test SS 164.308(a)(7) - Versioning (Contingency Plan)
        try:
            versioning = s3_client.get_bucket_versioning(Bucket=name)
            versioning_enabled = versioning.get('Status') == 'Enabled'
        except ClientError as e:
            versioning_enabled = False
            notes.append(f"Versioning check failed: {e.response['Error']['Code']}")

        notes_str = "; ".join(notes) if notes else "None"

        audit_results.append({
            "Resource": name,
            "HIPAA_Safeguard": "164.312(a)(1) Access Control (Public Block)",
            "Status": "COMPLIANT" if public_blocked else "NON-COMPLIANT",
            "Risk_Rating": "CRITICAL" if not public_blocked else "LOW",
            "Audit_Timestamp": timestamp,
            "Notes": notes_str
        })
        audit_results.append({
            "Resource": name,
            "HIPAA_Safeguard": "164.312(a)(2)(iv) Encryption at Rest (KMS)",
            "Status": "COMPLIANT" if encrypted else "NON-COMPLIANT",
            "Risk_Rating": "HIGH" if not encrypted else "LOW",
            "Audit_Timestamp": timestamp,
            "Notes": notes_str
        })
        audit_results.append({
            "Resource": name,
            "HIPAA_Safeguard": "164.312(a)(2)(iv) KMS Key Rotation Enabled",
            "Status": "COMPLIANT" if rotation_enabled else "NON-COMPLIANT",
            "Risk_Rating": "MEDIUM" if not rotation_enabled else "LOW",
            "Audit_Timestamp": timestamp,
            "Notes": notes_str
        })
        audit_results.append({
            "Resource": name,
            "HIPAA_Safeguard": "164.312(c)(1) Integrity Controls (WORM)",
            "Status": "COMPLIANT" if worm_enabled else "NON-COMPLIANT",
            "Risk_Rating": "MEDIUM" if not worm_enabled else "LOW",
            "Audit_Timestamp": timestamp,
            "Notes": notes_str
        })
        audit_results.append({
            "Resource": name,
            "HIPAA_Safeguard": "164.308(a)(7) Contingency Plan (Versioning)",
            "Status": "COMPLIANT" if versioning_enabled else "NON-COMPLIANT",
            "Risk_Rating": "MEDIUM" if not versioning_enabled else "LOW",
            "Audit_Timestamp": timestamp,
            "Notes": notes_str
        })

    os.makedirs("evidence", exist_ok=True)
    csv_file = "evidence/hipaa_audit_report.csv"

    if audit_results:
        keys = audit_results[0].keys()
        with open(csv_file, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(audit_results)
        print(f"\n[+] Audit Complete. Evidence report saved to: {csv_file}")
    else:
        print("[-] No Wellup Health resources found to audit.")

if __name__ == "__main__":
    audit_hipaa_s3_controls()