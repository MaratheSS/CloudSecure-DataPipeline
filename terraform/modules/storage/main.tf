# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

# KMS Keyring for CMEK (Customer-Managed Encryption Key)
resource "google_kms_key_ring" "habot_keyring" {
  name     = "habot-keyring-${var.environment}"
  location = var.region
}

# KMS Crypto Key for bucket encryption
resource "google_kms_crypto_key" "habot_key" {
  name            = "habot-bucket-key-${var.environment}"
  key_ring        = google_kms_key_ring.habot_keyring.id
  rotation_period = var.cmek_rotation_period
  purpose         = "ENCRYPT_DECRYPT"

  lifecycle {
    prevent_destroy = true
  }
}

# GCS Bucket for raw landing data (D0-raw-landing)
resource "google_storage_bucket" "d0_raw_landing" {
  name          = "${var.bucket_prefix}-d0-raw-landing-${var.environment}"
  location      = var.region
  project       = var.project_id
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.habot_key.id
  }
}

# IAM binding: only ingest service account can access the bucket
resource "google_storage_bucket_iam_member" "d0_raw_landing_ingest" {
  bucket = google_storage_bucket.d0_raw_landing.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${var.ingest_service_account_email}"
}

# Grant KMS access to ingest service account for encryption/decryption
resource "google_kms_crypto_key_iam_member" "ingest_kms_access" {
  crypto_key_id = google_kms_crypto_key.habot_key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${var.ingest_service_account_email}"
}


