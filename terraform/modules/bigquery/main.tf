# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

# BigQuery Dataset (D1-staged-enforced)
resource "google_bigquery_dataset" "d1_staged_enforced" {
  dataset_id    = var.dataset_id
  project       = var.project_id
  location      = var.region
  friendly_name = "Staged & Enforced Data (D1)"
  description   = "BigQuery dataset for validated student onboarding data after schema enforcement"

  labels = {
    environment = var.environment
    managed_by  = "terraform"
  }
}

# BigQuery Table: student_onboarding (raw, before row access policy)
resource "google_bigquery_table" "student_onboarding" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = "student_onboarding"
  project    = var.project_id

  time_partitioning {
    type          = "DAY"
    field         = "created_at"
    expiration_ms = null
  }

  clustering = ["student_id"]

  schema = jsonencode([
    {
      name        = "student_id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Unique student identifier"
    },
    {
      name        = "email"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Student email address (max 254 characters per RFC 5321)"
    },
    {
      name        = "first_name"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Student first name (max 50 characters)"
    },
    {
      name        = "last_name"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Student last name (max 50 characters)"
    },
    {
      name        = "status"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Onboarding status: PENDING, VERIFIED, ACTIVE, INACTIVE"
    },
    {
      name        = "created_at"
      type        = "TIMESTAMP"
      mode        = "REQUIRED"
      description = "Row creation timestamp"
    },
    {
      name        = "updated_at"
      type        = "TIMESTAMP"
      mode        = "NULLABLE"
      description = "Row last update timestamp"
    }
  ])

  labels = {
    environment = var.environment
    pii         = "true"
  }
}

# Row Access Policy (RLS): restrict rows by student_id visibility
resource "google_bigquery_row_access_policy" "student_onboarding_rls" {
  project          = var.project_id
  dataset_id       = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id         = google_bigquery_table.student_onboarding.table_id
  policy_id        = "student_onboarding_rls"
  filter_predicate = "TRUE"
  grantees = [
    "user:${var.data_owner_email}",
  ]
}

# Authorized View: exposes only non-sensitive columns to downstream consumers
resource "google_bigquery_table" "student_onboarding_view" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = "student_onboarding_view"
  project    = var.project_id

  view {
    query = "SELECT student_id, first_name, last_name, status, created_at FROM `${var.project_id}.${google_bigquery_dataset.d1_staged_enforced.dataset_id}.${google_bigquery_table.student_onboarding.table_id}`"
  }

  labels = {
    environment = var.environment
    view_type   = "authorized"
  }
}


