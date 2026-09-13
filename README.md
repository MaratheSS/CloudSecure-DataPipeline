# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

# CloudSecure DataPipeline — Enterprise-Grade Secure Cloud Data Pipeline

## Overview

This submission demonstrates a secure, production-ready data ingestion pipeline that prevents the incident described: unencrypted API credentials in code and database schema mismatches breaking downstream analytics.

The solution consists of three integrated components:

1. **Secure Infrastructure as Code (IaC)** — GCP resources provisioned via Terraform with Customer-Managed Encryption Keys (CMEK), fine-grained Identity and Access Management (IAM), and Row-Level Security (RLS).
2. **Automated CI/CD Fail-Closed Gate** — GitHub Actions workflow that scans for leaked secrets, enforces code quality, and blocks deployment if any gate fails.
3. **Schema Validation Layer** — Django REST Framework (DRF) serializer that validates all ingested data against the BigQuery schema before it reaches the data warehouse.

### Why This Fixes the Incident

- **Leaked credentials**: Terraform manages all secrets via environment variables and Google Cloud Secret Manager; GitHub Actions uses Workload Identity Federation (WIF) to authenticate without downloading service account keys. Gitleaks scans detect hardcoded credentials before merge.
- **Schema mismatch**: The DRF serializer is the single source of truth for data shape and enforces 1:1 mapping to the BigQuery table schema; validation errors are caught before data reaches the warehouse.

## Architecture

See `docs/architecture-diagram.md` for the full data flow and CI/CD gate placement.

## Stack

- **Cloud**: Google Cloud Platform (GCP)
- **Infrastructure Code**: Terraform
- **CI/CD**: GitHub Actions
- **Application**: Django REST Framework (Python)
- **Messaging**: Google Cloud Pub/Sub
- **Data Warehouse**: Google BigQuery
- **Secret Scanning**: gitleaks (open source)
- **Code Quality**: black, flake8, bandit
- **Infrastructure Security**: tfsec

## Setup & Deployment

### Prerequisites

1. GCP project with billing enabled
2. Terraform installed locally (`terraform` CLI)
3. Google Cloud CLI (`gcloud`) configured with Application Default Credentials (ADC)
4. GitHub repository with Actions enabled
5. Python 3.9+

### Local Terraform Deployment

```bash
cd terraform

# Copy and customize the example variables file
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars and fill in your GCP project ID, region, and GitHub repository details

# Initialize Terraform
terraform init

# Review the planned changes
terraform plan

# Apply the infrastructure (creates CMEK-encrypted buckets, BigQuery datasets with RLS, service accounts with WIF)
terraform apply
```

### GitHub Actions Setup (Workload Identity Federation)

After `terraform apply`, Terraform outputs the Workload Identity Federation configuration. Add these as GitHub repository secrets:

```
WORKLOAD_IDENTITY_PROVIDER = <output from terraform apply>
SERVICE_ACCOUNT_EMAIL = <output from terraform apply>
```

No service account key file is ever downloaded or stored in the repository.

### Django Application Tests

```bash
cd django_app

# Install dependencies (Django, DRF, pytest)
pip install -r requirements.txt

# Run serializer tests
pytest tests/test_serializers.py -v
```

All tests validate that the serializer enforces the BigQuery schema and rejects invalid payloads.

### Triggering the CI/CD Workflow

1. Push a commit to any branch:
   ```bash
   git push origin <branch-name>
   ```
2. GitHub Actions automatically runs `ci-fail-closed.yml`.
3. The workflow executes `lint` → `secret-scan` → `security-scan` in parallel, then `deploy` only if all three pass.

### Proving Fail-Closed Behavior

See `docs/fail-closed-test.md` for step-by-step instructions to reproduce the secret-scan failure locally and in GitHub Actions.

## File Structure

```
CloudSecure-DataPipeline/
├── README.md                          (this file)
├── terraform/
│   ├── main.tf                        (root config, module wiring)
│   ├── variables.tf                   (typed input variables)
│   ├── outputs.tf                     (bucket, dataset, service account outputs)
│   ├── terraform.tfvars.example       (example variable values)
│   └── modules/
│       ├── storage/main.tf            (GCS bucket with CMEK, versioning, lifecycle)
│       ├── bigquery/main.tf           (BigQuery dataset, table with RLS, authorized view)
│       └── iam/main.tf                (custom IAM roles, service accounts, WIF)
├── .github/
│   └── workflows/
│       └── ci-fail-closed.yml         (lint, secret-scan, security-scan, deploy)
├── django_app/
│   ├── models.py                      (Student model matching BigQuery schema)
│   ├── serializers.py                 (StudentOnboardingSerializer with validation)
│   ├── requirements.txt               (Python dependencies)
│   └── tests/
│       └── test_serializers.py        (3+ unit tests for validation)
└── docs/
    ├── architecture-diagram.md        (Mermaid diagram, data flow, CI/CD gate)
    ├── schema-mapping.md              (table: JSON field → Serializer → BigQuery)
    └── fail-closed-test.md            (instructions to reproduce secret-scan failure)
```

## Key Security Features

1. **CMEK Encryption**: All data at rest in GCS is encrypted with a customer-managed key.
2. **Workload Identity Federation**: GitHub Actions authenticates to GCP without service account key files.
3. **Row-Level Security (RLS)**: BigQuery rows are restricted by IAM principal; queries only return authorized data.
4. **Custom IAM Roles**: Each service account has the minimum permission set; no `roles/editor` or `roles/owner`.
5. **Automated Secret Scanning**: gitleaks scans every commit diff and fails the build if credentials are detected.
6. **Authorized View**: Downstream consumers query the authorized view, not the raw table.
7. **Schema Validation**: Django serializer rejects any payload that does not match the BigQuery schema.

## Testing the Solution

### Unit Tests (Schema Validation)
```bash
cd django_app
pytest tests/test_serializers.py -v
```

Expected output:
- ✓ Test valid student onboarding payload
- ✓ Test missing required field (email) → raises ValidationError
- ✓ Test invalid choice (status) → raises ValidationError

### Integration Test (Fail-Closed Gate)
Follow the instructions in `docs/fail-closed-test.md` to create a test branch with a fake API key and confirm that GitHub Actions blocks deployment.

## Cost Considerations

This solution uses **free and low-cost GCP services**:

- **GCS bucket**: Storage + operations (~$0.02–$0.05/month for small workloads)
- **BigQuery**: Query costs only (first 1 TB/month free); no storage costs for small datasets
- **Pub/Sub**: ~$0.04 per million messages
- **KMS**: ~$6/month per key (CMEK) — unavoidable for production security
- **GitHub Actions**: Free tier includes 2,000 minutes/month (sufficient for this project)
- **Service Accounts & IAM**: Free

**Total monthly cost for a small project: ~$10–15 USD** (primarily KMS key).

All tools are open source: Terraform, gitleaks, bandit, tfsec, Django, DRF, pytest.

## Contact & Support

For questions or issues, contact sushant Marathe at marathesushant862@gmail.com or +91-9307940220.


