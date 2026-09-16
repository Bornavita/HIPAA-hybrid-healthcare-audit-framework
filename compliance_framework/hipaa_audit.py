import boto3
import csv
import os

def audit_hipaa_s3_controls():
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()['Buckets']
    
    audit_results = []
    
    print("====================================================")
    print(" WELLUP HEALTH - HIPAA TECHNICAL SAFEGUARDS AUDIT ")
    print("====================================================\n")
    
    for bucket in buckets:
        name = bucket['Name']
        if "wellup-health" not in name:
            continue
            
        print(f"[*] Auditing ePHI Bucket: {name}")
        
        # 1. Test § 164.312(a)(1) - Public Access Block
        try:
            pab = s3_client.get_public_access_block(Bucket=name)['PublicAccessBlockConfiguration']
            public_blocked = all([
                pab.get('BlockPublicAcls', False),
                pab.get('IgnorePublicAcls', False),
                pab.get('BlockPublicPolicy', False),
                pab.get('RestrictPublicBuckets', False)
            ])
        except Exception:
            public_blocked = False
            
        # 2. Test § 164.312(a)(2)(iv) - KMS Encryption
        try:
            enc = s3_client.get_bucket_encryption(Bucket=name)
            rules = enc['ServerSideEncryptionConfiguration']['Rules']
            encrypted = any(r['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'aws:kms' for r in rules)
        except Exception:
            encrypted = False

        # 3. Test § 164.312(c)(2) - Object Lock (WORM / Integrity)
        try:
            lock = s3_client.get_object_lock_configuration(Bucket=name)
            worm_enabled = lock['ObjectLockConfiguration']['ObjectLockEnabled'] == 'Enabled'
        except Exception:
            worm_enabled = False

        audit_results.append({
            "Resource": name,
            "HIPAA_Safeguard": "§ 164.312(a)(1) Access Control (Public Block)",
            "Status": "COMPLIANT" if public_blocked else "NON-COMPLIANT",
            "Risk_Rating": "CRITICAL" if not public_blocked else "LOW"
        })
        audit_results.append({
            "Resource": name,
            "HIPAA_Safeguard": "§ 164.312(a)(2)(iv) Encryption at Rest (KMS)",
            "Status": "COMPLIANT" if encrypted else "NON-COMPLIANT",
            "Risk_Rating": "HIGH" if not encrypted else "LOW"
        })
        audit_results.append({
            "Resource": name,
            "HIPAA_Safeguard": "§ 164.312(c)(2) Integrity Controls (WORM)",
            "Status": "COMPLIANT" if worm_enabled else "NON-COMPLIANT",
            "Risk_Rating": "MEDIUM" if not worm_enabled else "LOW"
        })

    # Ensure evidence directory exists
    os.makedirs("evidence", exist_ok=True)
    csv_file = "evidence/hipaa_audit_report.csv"
    
    if audit_results:
        keys = audit_results[0].keys()
        with open(csv_file, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(audit_results)
        print(f"\n[+] Audit Complete. Evidence report saved to: {csv_file}")
    else:
        print("[-] No Wellup Health resources found to audit.")

if __name__ == "__main__":
    audit_hipaa_s3_controls()