# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

# Custom IAM Role for ingest pipeline (minimal permissions)
resource "google_project_iam_custom_role" "ingest_role" {
  role_id     = "ingestPipeline${replace(var.environment, "-", "")}"
  title       = "Ingest Pipeline ${var.environment}"
  description = "Custom role for ingesting data to GCS and BigQuery (minimum permissions)"

  permissions = [
    "storage.buckets.get",
    "storage.objects.create",
    "storage.objects.delete",
    "storage.objects.get",
    "storage.objects.list",
    "bigquery.tables.get",
    "bigquery.tables.list",
    "bigquery.datasets.get",
    "bigquery.datasets.list",
    "bigquery.tables.updateData",
  ]
}

# Custom IAM Role for transform pipeline
resource "google_project_iam_custom_role" "transform_role" {
  role_id     = "transformPipeline${replace(var.environment, "-", "")}"
  title       = "Transform Pipeline ${var.environment}"
  description = "Custom role for transforming data in BigQuery (minimum permissions)"

  permissions = [
    "bigquery.tables.get",
    "bigquery.tables.list",
    "bigquery.datasets.get",
    "bigquery.datasets.list",
    "bigquery.tables.update",
    "bigquery.tables.updateData",
  ]
}

# Custom IAM Role for CI/CD (GitHub Actions) — deploy only, no data access
resource "google_project_iam_custom_role" "cicd_role" {
  role_id     = "cicdPipeline${replace(var.environment, "-", "")}"
  title       = "CI/CD Pipeline ${var.environment}"
  description = "Custom role for GitHub Actions (terraform deploy, no data access)"

  permissions = [
    "compute.instances.get",
    "compute.instances.list",
  ]
}

# Service Account: Ingest
resource "google_service_account" "ingest" {
  account_id   = "habot-ingest-${var.environment}"
  display_name = "Habot Ingest Service Account (${var.environment})"
  description  = "Service account for data ingestion pipeline"
}

# Service Account: Transform
resource "google_service_account" "transform" {
  account_id   = "habot-transform-${var.environment}"
  display_name = "Habot Transform Service Account (${var.environment})"
  description  = "Service account for data transformation pipeline"
}

# Service Account: CI/CD (GitHub Actions)
resource "google_service_account" "cicd" {
  account_id   = "habot-cicd-${var.environment}"
  display_name = "Habot CI/CD Service Account (${var.environment})"
  description  = "Service account for GitHub Actions (Workload Identity Federation)"
}

# Bind custom roles to service accounts
resource "google_project_iam_member" "ingest_role_binding" {
  project = var.project_id
  role    = google_project_iam_custom_role.ingest_role.id
  member  = "serviceAccount:${google_service_account.ingest.email}"
}

resource "google_project_iam_member" "transform_role_binding" {
  project = var.project_id
  role    = google_project_iam_custom_role.transform_role.id
  member  = "serviceAccount:${google_service_account.transform.email}"
}

resource "google_project_iam_member" "cicd_role_binding" {
  project = var.project_id
  role    = google_project_iam_custom_role.cicd_role.id
  member  = "serviceAccount:${google_service_account.cicd.email}"
}

# Workload Identity Federation: Configure trust relationship with GitHub
resource "google_iam_workload_identity_pool" "github_pool" {
  provider            = google
  project             = var.project_id
  location            = "global"
  workload_identity_pool_id = "github-${var.environment}"
  display_name        = "GitHub ${var.environment}"
  disabled            = false
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  provider = google
  project  = var.project_id
  location = "global"

  workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider-${var.environment}"

  display_name = "GitHub Provider ${var.environment}"
  disabled     = false

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.aud"        = "assertion.aud"
    "attribute.repository" = "assertion.repository"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Bind GitHub Actions to the CI/CD service account via Workload Identity Federation
resource "google_service_account_iam_member" "github_workload_identity" {
  service_account_id = google_service_account.cicd.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/projects/${var.project_id}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github_pool.workload_identity_pool_id}/attribute.repository/${var.github_repo_owner}/${var.github_repo_name}"
}

# Output the Workload Identity Provider for GitHub Actions configuration
resource "local_file" "github_actions_config" {
  filename = "${path.module}/../../.github/workload-identity-config.txt"
  content  = <<-EOT
    WORKLOAD_IDENTITY_PROVIDER=projects/${data.google_client_config.current.project_number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github_pool.workload_identity_pool_id}/providers/${google_iam_workload_identity_pool_provider.github_provider.workload_identity_pool_provider_id}
    SERVICE_ACCOUNT_EMAIL=${google_service_account.cicd.email}
  EOT
}

data "google_client_config" "current" {
  provider = google
}


