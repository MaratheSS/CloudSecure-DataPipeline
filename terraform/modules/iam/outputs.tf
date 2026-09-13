# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

output "ingest_service_account_email" {
  value = google_service_account.ingest.email
}

output "transform_service_account_email" {
  value = google_service_account.transform.email
}

output "cicd_service_account_email" {
  value = google_service_account.cicd.email
}

output "workload_identity_provider" {
  value     = "projects/${data.google_client_config.current.project_number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github_pool.workload_identity_pool_id}/providers/${google_iam_workload_identity_pool_provider.github_provider.workload_identity_pool_provider_id}"
  sensitive = true
}


