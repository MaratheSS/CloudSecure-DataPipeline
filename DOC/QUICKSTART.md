# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

# CloudSecure DataPipeline — Quick Start Guide

Get the pipeline running in 15 minutes (or less).

## One-Time Setup (5 minutes)

### 1. Clone & Install

```bash
git clone https://github.com/<your-username>/CloudSecure-DataPipeline.git
cd CloudSecure-DataPipeline
cd django_app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 2. Install Terraform & gcloud

```bash
# macOS
brew install terraform google-cloud-sdk

# Linux (Ubuntu/Debian)
curl https://sdk.cloud.google.com | bash
terraform -v
gcloud --version

# Windows (Chocolatey)
choco install terraform google-cloud-sdk
```

### 3. Authenticate

```bash
gcloud auth application-default login
gcloud config set project my-gcp-project-id
```

## Deploy Infrastructure (5 minutes)

### 1. Configure Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your values:
# - project_id
# - gcs_bucket_prefix
# - github_repo_owner & github_repo_name
```

### 2. Deploy

```bash
terraform init
terraform plan
terraform apply
```

**Save the outputs** (you'll need them for GitHub Actions):

```bash
terraform output
```

## Setup GitHub Actions (3 minutes)

Go to your GitHub repo:

**Settings → Secrets and variables → Actions → New repository secret**

Add these two secrets (from `terraform output`):

1. `WORKLOAD_IDENTITY_PROVIDER` = `projects/...`
2. `SERVICE_ACCOUNT_EMAIL` = `habot-cicd-...@...iam.gserviceaccount.com`

Save and you're done!

## Test Everything (2 minutes)

### Run Django Tests

```bash
cd django_app
pytest tests/test_serializers.py -v
```

Expected output: **13 passed** ✓

### Trigger GitHub Actions

```bash
git push origin main
# or create a test branch:
# git checkout -b test/workflow
# touch test.txt && git add test.txt && git commit -m "test" && git push origin test/workflow
```

Go to **Actions** tab on GitHub and verify all jobs pass:
- ✓ lint
- ✓ secret-scan
- ✓ security-scan
- ✓ deploy

### Test Fail-Closed Gate

```bash
git checkout -b test/secret-leak
echo 'API_KEY = "sk-fake-1234567890"' > django_app/test_key.py
git add django_app/test_key.py
git commit -m "test: verify secret scan blocks deploy"
git push origin test/secret-leak
```

Go to **Actions** and watch:
- ✓ lint: PASSED
- ✗ secret-scan: **FAILED** (✓ This is what we want!)
- ⊘ deploy: CANCELLED (✓ Deploy was blocked!)

Clean up:

```bash
git checkout test/secret-leak
rm django_app/test_key.py
git add django_app/ && git commit -m "cleanup" && git push
```

## What You Now Have

| Component | Status |
|---|---|
| GCS Bucket (CMEK encrypted) | ✓ Deployed |
| BigQuery Dataset + Table | ✓ Deployed |
| Row-Level Security (RLS) | ✓ Configured |
| Authorized View | ✓ Ready |
| Custom IAM Roles | ✓ Deployed |
| Workload Identity Federation | ✓ Configured |
| GitHub Actions CI/CD | ✓ Running |
| Secret Scanning | ✓ Active |
| Django Serializer Validation | ✓ Tested |
| Fail-Closed Gate | ✓ Verified |

## Next Steps

1. **Ingest Real Data**: Send JSON payloads to the serializer for validation
2. **Monitor BigQuery**: Query the authorized view (not the raw table)
3. **Scale**: Adjust terraform variables for production (environment = "prod")
4. **Monitor Costs**: Check GCP billing for CMEK and BigQuery usage

## Troubleshooting

**"gcloud auth failed"**
```bash
gcloud auth application-default login
```

**"terraform init" fails**
```bash
terraform init -upgrade
```

**"pytest: command not found"**
```bash
cd django_app
pip install pytest pytest-django
pytest tests/test_serializers.py -v
```

**"GitHub Actions secrets not working"**
- Verify both secrets are set (Settings → Secrets)
- Re-run the workflow (Actions → select workflow → Re-run jobs)

## Full Documentation

- **Architecture & Data Flow**: `docs/architecture-diagram.md`
- **Schema Mapping**: `docs/schema-mapping.md`
- **Fail-Closed Testing**: `docs/fail-closed-test.md`
- **Complete Operations Guide**: `OPERATIONS.md`

## Need Help?

Contact: sushant Marathe at marathesushant862@gmail.com or +91-9307940220


