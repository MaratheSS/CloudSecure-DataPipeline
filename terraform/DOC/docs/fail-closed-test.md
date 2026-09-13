# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

# Testing the Fail-Closed CI/CD Gate

This document provides step-by-step instructions to verify that the secret-scan job blocks deployment when credentials are detected.

## Objective

Prove that the fail-closed gate prevents a junior developer's accidental credential leak from reaching production.

## Prerequisites

1. Local Git repository cloned from GitHub
2. GitHub repository with Actions enabled
3. Gitleaks installed locally (optional, for pre-testing)

## Step 1: Create a Test Branch

```bash
cd CloudSecure-DataPipeline
git checkout -b test/secret-leak-detection
```

## Step 2: Add a Fake Hardcoded API Key

Create a new file `django_app/test_config.py` with an intentionally leaked API key:

```python
# sushant Marathe / marathesushant862@gmail.com / +91-9307940220
# This is a test file to verify secret scanning works

API_KEY = "sk-fake-1234567890abcdef"
DATABASE_PASSWORD = "prod_password_123"
AWS_SECRET_KEY = "AKIA2FAKE1234567890AB"
```

Do NOT commit this yet. First, test it locally.

## Step 3: Test Locally with Gitleaks (Optional)

Install gitleaks (if not already installed):

```bash
# On macOS (Homebrew)
brew install gitleaks

# On Linux
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks-linux-x64
chmod +x gitleaks-linux-x64
sudo mv gitleaks-linux-x64 /usr/local/bin/gitleaks

# On Windows (PowerShell)
curl -L https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks-windows-amd64.exe -o gitleaks.exe
```

Run gitleaks to detect the secret:

```bash
gitleaks detect --verbose --report-format json
```

Expected output:
```
finding:
  description: Asymmetric Private Key
  file: django_app/test_config.py
  secret: sk-fake-1234567890abcdef
  match: API_KEY = "sk-fake-1234567890abcdef"
```

The exit code should be **non-zero** (failure), indicating a secret was found.

## Step 4: Commit and Push to GitHub

```bash
git add django_app/test_config.py
git commit -m "test: add fake API key to verify secret scanning"
git push origin test/secret-leak-detection
```

## Step 5: Monitor GitHub Actions

1. Go to your GitHub repository on github.com
2. Click **Actions** tab
3. Find the workflow run for commit `test: add fake API key to verify secret scanning`
4. Click into the run to view the jobs

### Expected Behavior

The workflow should show:

- ✓ **lint** job: PASSED (no code style issues)
- ✗ **secret-scan** job: **FAILED** (gitleaks detected credentials)
- ⊘ **security-scan** job: SKIPPED (because secret-scan failed)
- ⊘ **deploy** job: **NOT TRIGGERED** (hard dependency on secret-scan)

### Finding the Failure Log Line

1. Click on the **secret-scan** job in the workflow run
2. Expand the **Run gitleaks on HEAD commit** step
3. Look for a line like:
   ```
   finding:
     description: AWS Manager ID
     secret: sk-fake-1234567890abcdef
     file: django_app/test_config.py
   ```
4. The gitleaks output ends with a JSON report and exit code **1** (failure)

This proves the gate is fail-closed: **the secret-scan job blocked the deploy job from running.**

## Step 6: Clean Up the Test Commit

Once you've confirmed the test passed, delete the test file and commit:

```bash
rm django_app/test_config.py
git add django_app/
git commit -m "test: cleanup after verifying secret scanning works"
git push origin test/secret-leak-detection
```

The new workflow run should show:

- ✓ **lint** job: PASSED
- ✓ **secret-scan** job: PASSED (no secrets found)
- ✓ **security-scan** job: PASSED
- ✓ **deploy** job: PASSED (all upstream jobs succeeded)

## Step 7: Delete the Test Branch (Optional)

```bash
git checkout main
git branch -d test/secret-leak-detection
git push origin --delete test/secret-leak-detection
```

## Success Criteria

The fail-closed gate is working correctly if:

1. ✓ Commit with fake API key → secret-scan **FAILS** → deploy is **BLOCKED**
2. ✓ Commit with fake API key removed → secret-scan **PASSES** → deploy is **ALLOWED**
3. ✓ The GitHub Actions log shows the exact line where the secret was detected
4. ✓ The `deploy` job never runs when any upstream gate fails

## Real-World Scenario: Simulating the Incident

Imagine a junior developer accidentally commits this code:

```python
# django_app/integrations.py
def fetch_student_data():
    client = BigQueryClient(
        project_id="my-gcp-project",
        api_key="sk-real-production-key-1234567890"  # OOPS! Leaked!
    )
    return client.query("SELECT * FROM students")
```

**Without the fail-closed gate**:
- The commit is pushed to main
- The deployment proceeds without scanning
- The credentials are now visible in the repository
- Attackers can use the API key to access production data

**With the fail-closed gate**:
- Gitleaks detects the pattern `sk-real-production-key-` 
- The secret-scan job **FAILS**
- The deploy job **NEVER RUNS**
- The junior developer gets an error notification
- They fix the code (remove the key, use environment variables instead)
- The corrected commit passes all gates and deploys
- **The incident is prevented.**

## Advanced: Custom Gitleaks Rules

If you want to detect additional secret patterns (e.g., custom API key formats), you can create a `.gitleaks.toml` configuration file in the repository root:

```toml
title = "Custom Gitleaks Config"

[[rules]]
id = "custom-api-key"
description = "Custom API key pattern"
regex = '''CUSTOM_KEY\s*=\s*["']?[A-Za-z0-9]{20,}["']?'''
secretGroup = 1
```

Then run:

```bash
gitleaks detect --config .gitleaks.toml --verbose
```

This allows you to extend secret detection for your organization's internal secret formats.


