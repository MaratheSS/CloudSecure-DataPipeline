# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

# CloudSecure DataPipeline Hiring Project — Complete Operations Guide

This document contains every detail needed to deploy, test, operate, and troubleshoot the CloudSecure DataPipeline pipeline in production.

## Table of Contents

1. [Deployment Checklist](#deployment-checklist)
2. [Local Development Setup](#local-development-setup)
3. [Terraform Deployment](#terraform-deployment)
4. [GitHub Actions Configuration](#github-actions-configuration)
5. [Django Application Testing](#django-application-testing)
6. [CI/CD Fail-Closed Gate Testing](#cicd-fail-closed-gate-testing)
7. [Monitoring & Debugging](#monitoring--debugging)
8. [Cost Management](#cost-management)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Security Checklist](#security-checklist)

---

## Deployment Checklist

Before deploying to production, verify each of the following:

- [ ] GCP project created with billing enabled
- [ ] Service account created with necessary IAM roles (handled by Terraform)
- [ ] Terraform variables filled in (`terraform.tfvars`)
- [ ] GitHub repository created and Actions enabled
- [ ] CMEK key created and accessible
- [ ] Row-Level Security (RLS) configured with correct principal email
- [ ] Workload Identity Federation (WIF) configured
- [ ] GitHub Actions secrets populated (from Terraform outputs)
- [ ] Django serializer tests passing (3+ tests)
- [ ] Secret scanning enabled and tested
- [ ] Backup strategy for GCS bucket versioning
- [ ] Monitoring/alerting setup (optional)

---

## Local Development Setup

### Prerequisites

1. **Operating System**: Linux, macOS, or Windows (with WSL2 recommended)
2. **Python 3.9+**
3. **Terraform 1.0+**
4. **Google Cloud SDK (`gcloud` CLI)**
5. **Git 2.25+**

### Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/CloudSecure-DataPipeline.git
cd CloudSecure-DataPipeline
```

### Step 2: Install Python Dependencies

```bash
cd django_app
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows (Command Prompt)
venv\Scripts\activate

# On Windows (PowerShell)
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### Step 3: Install Terraform

```bash
# On macOS (Homebrew)
brew install terraform

# On Linux (Ubuntu/Debian)
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# On Windows (Chocolatey)
choco install terraform
```

Verify installation:

```bash
terraform -version
python --version
gcloud --version
```

### Step 4: Authenticate with Google Cloud

```bash
gcloud auth application-default login
gcloud config set project <YOUR-GCP-PROJECT-ID>
```

This enables Terraform to authenticate with your GCP project.

---

## Terraform Deployment

### Step 1: Configure Variables

Copy the example variables file:

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` and fill in your GCP project details:

```hcl
project_id           = "my-gcp-project-id"
region               = "us-central1"
environment          = "dev"
gcs_bucket_prefix    = "my-org-habot"
github_repo_owner    = "my-username"
github_repo_name     = "CloudSecure-DataPipeline"
github_repo_ref      = "main"
data_owner_email     = "your-email@example.com"
```

### Step 2: Initialize Terraform

```bash
terraform init
```

This downloads the Google Cloud provider and initializes the working directory.

Expected output:
```
Terraform has been successfully initialized!
```

### Step 3: Plan the Deployment

```bash
terraform plan -out=tfplan
```

This shows all resources that will be created. Review the output to ensure:
- GCS bucket with CMEK encryption ✓
- BigQuery dataset with RLS ✓
- Custom IAM roles ✓
- Service accounts ✓
- Workload Identity Federation ✓

### Step 4: Apply the Deployment

```bash
terraform apply tfplan
```

Terraform will create all resources. This takes 2–5 minutes.

Expected resources created:
- 1 KMS Keyring
- 1 KMS Crypto Key (CMEK)
- 1 GCS Bucket (D0-raw-landing)
- 1 BigQuery Dataset (D1-staged-enforced)
- 1 BigQuery Table (student_onboarding)
- 1 BigQuery Row Access Policy (RLS)
- 1 BigQuery Authorized View
- 3 Custom IAM Roles (ingest, transform, cicd)
- 3 Service Accounts
- 1 Workload Identity Pool
- 1 Workload Identity Provider

### Step 5: Capture Outputs

After apply completes, Terraform outputs critical information:

```bash
terraform output
```

Copy these values to GitHub Actions secrets:

```
WORKLOAD_IDENTITY_PROVIDER = projects/123456789/locations/global/workloadIdentityPools/github-dev/providers/github-provider-dev
SERVICE_ACCOUNT_EMAIL = habot-cicd-dev@my-gcp-project-id.iam.gserviceaccount.com
```

---

## GitHub Actions Configuration

### Step 1: Add Repository Secrets

Go to GitHub: **Settings → Secrets and variables → Actions → New repository secret**

Add these secrets:

| Secret Name | Value |
|---|---|
| `WORKLOAD_IDENTITY_PROVIDER` | From `terraform output workload_identity_provider` |
| `SERVICE_ACCOUNT_EMAIL` | From `terraform output workload_identity_service_account_email` |

### Step 2: Verify GitHub Actions is Enabled

Go to **Settings → Actions** and verify:
- [ ] Actions permissions: "Allow all actions and reusable workflows"
- [ ] Workflow permissions: "Read and write permissions"

### Step 3: Trigger a Workflow Run

Push a commit to any branch:

```bash
echo "# Test commit" >> README.md
git add README.md
git commit -m "test: trigger GitHub Actions"
git push origin test-branch
```

Go to **Actions** tab and confirm the workflow runs through all jobs:
- ✓ lint
- ✓ secret-scan
- ✓ security-scan
- ✓ deploy

---

## Django Application Testing

### Step 1: Run the Serializer Tests

```bash
cd django_app
pytest tests/test_serializers.py -v
```

Expected output (13 tests):
```
tests/test_serializers.py::TestStudentOnboardingSerializer::test_valid_payload PASSED
tests/test_serializers.py::TestStudentOnboardingSerializer::test_missing_required_field_email PASSED
tests/test_serializers.py::TestStudentOnboardingSerializer::test_invalid_status_choice PASSED
... (10 more tests)

===== 13 passed in 0.45s =====
```

### Step 2: Test a Valid Payload

Create a test script `django_app/test_payload.py`:

```python
from serializers import StudentOnboardingSerializer

valid_payload = {
    "student_id": "STU-001",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Johnson",
    "status": "VERIFIED",
}

serializer = StudentOnboardingSerializer(data=valid_payload)
if serializer.is_valid():
    print("✓ Valid payload accepted")
    print(f"Validated data: {serializer.validated_data}")
else:
    print(f"✗ Unexpected validation error: {serializer.errors}")
```

Run:

```bash
python test_payload.py
```

Expected output:
```
✓ Valid payload accepted
Validated data: {'student_id': 'STU-001', 'email': 'alice@example.com', ...}
```

### Step 3: Test an Invalid Payload

```python
invalid_payload = {
    "student_id": "STU-002",
    # Missing email (required)
    "first_name": "Bob",
    "last_name": "Smith",
    "status": "ACTIVE",
}

serializer = StudentOnboardingSerializer(data=invalid_payload)
if not serializer.is_valid():
    print(f"✓ Invalid payload rejected: {serializer.errors}")
else:
    print("✗ Invalid payload unexpectedly accepted")
```

Expected output:
```
✓ Invalid payload rejected: {'email': ['This field is required.']}
```

---

## CI/CD Fail-Closed Gate Testing

### Step 1: Create a Test Branch with a Fake Secret

```bash
git checkout -b test/secret-detection
```

Create `django_app/test_secret.py`:

```python
# DO NOT COMMIT THIS TO MAIN
API_KEY = "sk-fake-1234567890abcdef"
```

### Step 2: Commit and Push

```bash
git add django_app/test_secret.py
git commit -m "test: verify secret scanning blocks deploy"
git push origin test/secret-detection
```

### Step 3: Monitor the Workflow

Go to GitHub **Actions** tab. The workflow should show:

- ✓ **lint**: PASSED
- ✗ **secret-scan**: **FAILED** (gitleaks detected `sk-fake-1234567890abcdef`)
- ⊘ **security-scan**: SKIPPED
- ⊘ **deploy**: CANCELLED (hard dependency on secret-scan)

Click **secret-scan** job and expand **Run gitleaks on HEAD commit** to see the detected secret.

### Step 4: Fix and Re-test

Remove the secret file:

```bash
rm django_app/test_secret.py
git add django_app/
git commit -m "test: remove fake secret"
git push origin test/secret-detection
```

The new workflow run should show:

- ✓ **lint**: PASSED
- ✓ **secret-scan**: PASSED (no secrets found)
- ✓ **security-scan**: PASSED
- ✓ **deploy**: PASSED (all gates passed)

---

## Monitoring & Debugging

### Check GCS Bucket

```bash
gsutil ls -L gs://<bucket-name>/
```

Verify:
- Versioning enabled
- Encryption: CMEK key present
- Lifecycle rules in place

### Check BigQuery Table

```bash
bq show --format=prettyjson <project>:<dataset>.<table>

# Check Row-Level Security
bq query --use_legacy_sql=false \
  'SELECT * FROM `<project>.<dataset>.<table>` LIMIT 1'
```

### Check Service Accounts

```bash
gcloud iam service-accounts list --format="table(email,displayName)"

# Check IAM bindings for a service account
gcloud projects get-iam-policy <project> \
  --flatten="bindings[].members" \
  --filter="bindings.members:<service-account-email>" \
  --format="table(bindings.role)"
```

### Check Workload Identity Federation

```bash
gcloud iam workload-identity-pools list --location=global

# Verify the GitHub provider
gcloud iam workload-identity-pools providers list \
  --workload-identity-pool=<pool-id> \
  --location=global
```

### View Terraform State

```bash
terraform show

# Output a specific value
terraform output gcs_bucket_name
terraform output workload_identity_provider
```

---

## Cost Management

### Cost Breakdown (Monthly)

| Service | Usage | Cost |
|---|---|---|
| **GCS Storage** | 10 GB | $0.23 |
| **GCS Operations** | 10,000 reads/month | $0.04 |
| **BigQuery** | 0.5 TB scanned | Free (< 1 TB/month) |
| **KMS Key** | 1 key | $6.00 |
| **Pub/Sub** | 1M messages | $0.04 |
| **GitHub Actions** | 500 runs × 2 min | Free (< 2,000 min/month) |
| **Service Accounts** | 3 accounts | Free |
| **IAM** | Custom roles | Free |
| **Workload Identity** | Unlimited authentications | Free |
| **Terraform State** | GCS backend | ~$0.10 |
| **TOTAL** | | ~**$6.41/month** |

### Cost Optimization Tips

1. **Reduce KMS Key Cost**: Consider using Cloud Key Management Service (CKMS) or Google-managed encryption for non-sensitive data.
2. **Archive Old Data**: Use GCS lifecycle rules to transition to Coldline after 180 days (cheaper).
3. **Partition BigQuery**: Date-partitioned tables reduce query costs by only scanning relevant days.
4. **Use Authorized Views**: Ensures only necessary columns are exposed to downstream consumers.

### Disable Cost-Generating Services (Dev)

If testing in dev, you can reduce costs by disabling unused services:

```bash
# Disable KMS (use Google-managed encryption instead)
terraform destroy -target=google_kms_crypto_key.habot_key
```

**Note**: This sacrifices security for cost savings. Not recommended for production.

---

## Troubleshooting Guide

### Issue: "terraform init" fails with "provider download error"

**Solution**:
```bash
terraform init -upgrade
```

### Issue: "permission denied" error when running Terraform

**Solution**: Ensure you're authenticated with Google Cloud:
```bash
gcloud auth application-default login
gcloud config set project <PROJECT_ID>
```

### Issue: GitHub Actions secret-scan PASSED but I know there's a secret

**Solution**: gitleaks might not detect the pattern. Add custom rules in `.gitleaks.toml`:

```toml
[[rules]]
id = "custom-api-key"
regex = '''MY_API_KEY\s*=\s*["']?[A-Za-z0-9]{20,}["']?'''
```

### Issue: BigQuery query times out

**Solution**: Use the authorized view instead of the raw table:

```sql
SELECT * FROM `project.dataset.student_onboarding_view`
```

The authorized view is clustered and partitioned for faster queries.

### Issue: "Row access policy not working"

**Solution**: Ensure the IAM principal has the correct role on the BigQuery dataset:

```bash
gcloud bigquery datasets add-iam-policy-binding d1_staged_enforced \
  --member=<principal> \
  --role=roles/bigquery.dataViewer
```

### Issue: Django serializer test fails with "ModuleNotFoundError"

**Solution**: Ensure Django is installed and the Python path is correct:

```bash
cd django_app
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/test_serializers.py -v
```

### Issue: Workload Identity Federation not working in GitHub Actions

**Solution**: Verify the GitHub provider is configured correctly:

```bash
gcloud iam workload-identity-pools providers describe \
  --workload-identity-pool=<pool-id> \
  --location=global
```

Check that `attribute.repository` includes your repo owner and name.

---

## Security Checklist

Before going to production, verify:

- [ ] CMEK key is enabled and KMS key rotation is set to 90 days
- [ ] Row-Level Security (RLS) is configured with the correct principal
- [ ] Service accounts have minimum permissions (no `roles/editor` or `roles/owner`)
- [ ] Workload Identity Federation is enabled (no service account key files)
- [ ] GitHub Actions secrets are configured (never expose them in logs)
- [ ] Secret scanning (gitleaks) is enabled and tests pass
- [ ] Code security scanning (bandit, tfsec) is enabled
- [ ] GCS bucket has uniform bucket-level access enabled
- [ ] Authorized view restricts sensitive columns from downstream consumers
- [ ] Object versioning is enabled in GCS for data recovery
- [ ] Terraform state is encrypted and stored securely (local dev only; use remote backend for production)
- [ ] Audit logging is enabled for BigQuery and GCS (optional)

---

## Production Deployment Steps

1. **Update Terraform variables** for production environment:
   ```bash
   environment = "prod"
   gcs_bucket_prefix = "prod-org-habot"
   cmek_rotation_period = "7776000s"
   ```

2. **Run Terraform plan** and review all changes:
   ```bash
   terraform plan -var-file=terraform.prod.tfvars
   ```

3. **Apply Terraform** to production:
   ```bash
   terraform apply -var-file=terraform.prod.tfvars
   ```

4. **Update GitHub Actions secrets** with production values.

5. **Run Django serializer tests** to verify data validation.

6. **Run fail-closed gate test** with a fake secret to confirm deployment is blocked.

7. **Monitor costs** for the first month and adjust as needed.

8. **Set up alerting** (optional) for:
   - KMS key usage
   - BigQuery query costs
   - GCS storage growth
   - GitHub Actions job failures

---

## Support & Escalation

If you encounter issues not covered in this guide:

1. Check the logs: `terraform output` and GitHub Actions workflow logs
2. Review the architecture diagram: `docs/architecture-diagram.md`
3. Check the schema mapping: `docs/schema-mapping.md`
4. Contact: sushant Marathe at marathesushant862@gmail.com or +91-9307940220

---

End of Operations Guide


