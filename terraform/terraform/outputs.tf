# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

output "gcs_bucket_name" {
  description = "Name of the raw landing GCS bucket (D0-raw-landing)"
  value       = module.storage.bucket_name
}

output "bigquery_dataset_id" {
  description = "BigQuery dataset ID (D1-staged-enforced)"
  value       = module.bigquery.dataset_id
}

output "bigquery_table_id" {
  description = "BigQuery table ID for student onboarding"
  value       = module.bigquery.table_id
}

output "bigquery_authorized_view_id" {
  description = "BigQuery authorized view ID for downstream consumers"
  value       = module.bigquery.authorized_view_id
}

output "ingest_service_account_email" {
  description = "Service account email for ingest pipeline"
  value       = module.iam.ingest_service_account_email
}

output "transform_service_account_email" {
  description = "Service account email for transform pipeline"
  value       = module.iam.transform_service_account_email
}

output "cicd_service_account_email" {
  description = "Service account email for CI/CD (GitHub Actions)"
  value       = module.iam.cicd_service_account_email
}

output "workload_identity_provider" {
  description = "Workload Identity Provider resource name (use in GitHub Actions secrets)"
  value       = module.iam.workload_identity_provider
  sensitive   = true
}

output "workload_identity_service_account_email" {
  description = "Service account email bound to GitHub Actions via Workload Identity Federation"
  value       = module.iam.cicd_service_account_email
  sensitive   = true
}

output "kms_key_id" {
  description = "KMS key ID for CMEK (Customer-Managed Encryption Key)"
  value       = module.storage.kms_key_id
}


