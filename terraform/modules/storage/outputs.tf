# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

output "bucket_name" {
  value = google_storage_bucket.d0_raw_landing.name
}

output "kms_key_id" {
  value = google_kms_crypto_key.habot_key.id
}


