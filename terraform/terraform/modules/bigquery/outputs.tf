# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

output "dataset_id" {
  value = google_bigquery_dataset.d1_staged_enforced.dataset_id
}

output "table_id" {
  value = google_bigquery_table.student_onboarding.table_id
}

output "authorized_view_id" {
  value = google_bigquery_table.student_onboarding_view.table_id
}


