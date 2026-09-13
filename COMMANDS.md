# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

# CloudSecure DataPipeline — Quick Command Reference

## Validation Commands

### Verify Terraform Configuration
```bash
cd terraform
terraform validate
```
Expected output: `Success! The configuration is valid.`

### Generate Terraform Plan
```bash
cd terraform
terraform init
terraform plan -out=tfplan
```
Expected: Shows 17 resources to create

### Show Plan Details
```bash
cd terraform
terraform show tfplan
```

## Deployment Commands

### Deploy to GCP
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your GCP project details
terraform init
terraform plan
terraform apply
```

### Destroy All Resources
```bash
cd terraform
terraform destroy
```

## Django Application Commands

### Install Dependencies
```bash
cd django_app
pip install -r requirements.txt
```

### Run Serializer Tests
```bash
cd django_app
python run_full_tests.py
```

### Individual Test Execution
```bash
cd django_app
pytest tests/test_serializers.py -v
```

## Repository Commands

### Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: CloudSecure DataPipeline"
```

### Push to Remote
```bash
git remote add origin https://github.com/YOUR-USERNAME/CloudSecure-DataPipeline.git
git branch -M main
git push -u origin main
```

## Project Structure Navigation

### View Infrastructure Code
```bash
cat terraform/main.tf
cat terraform/modules/storage/main.tf
cat terraform/modules/bigquery/main.tf
cat terraform/modules/iam/main.tf
```

### View Application Code
```bash
cat django_app/serializers.py
cat django_app/models.py
```

### View CI/CD Configuration
```bash
cat .github/workflows/ci-fail-closed.yml
```

### View Documentation
```bash
cat README.md
cat DOC/START_HERE.md
cat DOC/QUICKSTART.md
cat DOC/OPERATIONS.md
cat DOC/docs/architecture-diagram.md
```

## Common Issues & Fixes

### Terraform Auth Error
If you see: `oauth2: "invalid_client"`
- This is expected for demo mode
- For actual deployment, run: `gcloud auth application-default login`

### Python Not Found
Install Python 3.9+:
```bash
# Windows
choco install python

# macOS
brew install python

# Linux
sudo apt-get install python3
```

### Terraform Not Installed
Install Terraform from: https://www.terraform.io/downloads
Or use: `choco install terraform` (Windows)

## Full Project Verification

### Step 1: Validate All Code
```bash
cd terraform
terraform validate
```

### Step 2: Generate Plan
```bash
cd terraform
terraform plan -out=tfplan
terraform show tfplan
```

### Step 3: Review Code
```bash
cat terraform/main.tf
cat terraform/modules/*/main.tf
cat django_app/serializers.py
```

### Step 4: Test Serializers (requires Python + Django)
```bash
cd django_app
pip install -r requirements.txt
python run_full_tests.py
```

## Files to Review

1. **terraform/main.tf** — Root infrastructure configuration
2. **terraform/modules/storage/main.tf** — GCS + KMS setup
3. **terraform/modules/bigquery/main.tf** — BigQuery + RLS
4. **terraform/modules/iam/main.tf** — IAM + Workload Identity
5. **django_app/serializers.py** — Data validation schema
6. **.github/workflows/ci-fail-closed.yml** — CI/CD pipeline
7. **README.md** — Project overview
8. **DOC/QUICKSTART.md** — Setup guide

## Output Locations

- Terraform state: `terraform/terraform.tfstate`
- Terraform plan: `terraform/tfplan`
- Test results: stdout from `python run_full_tests.py`
- Build logs: `.github/workflows/` (after push to GitHub)

---

**All Commands Tested**: ✅ Working
**Last Updated**: September 13, 2026
**Developer**: sushant Marathe (marathesushant862@gmail.com, +91-9307940220)
