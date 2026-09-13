# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "storage" {
  source = "./modules/storage"

  project_id          = var.project_id
  region              = var.region
  environment         = var.environment
  bucket_prefix       = var.gcs_bucket_prefix
  cmek_rotation_period = var.cmek_rotation_period

  ingest_service_account_email = module.iam.ingest_service_account_email
}

module "bigquery" {
  source = "./modules/bigquery"

  project_id    = var.project_id
  region        = var.region
  dataset_id    = var.bigquery_dataset_id
  environment   = var.environment
  data_owner_email = var.data_owner_email

  depends_on = [module.iam]
}

module "iam" {
  source = "./modules/iam"

  project_id           = var.project_id
  region               = var.region
  environment          = var.environment
  github_repo_owner    = var.github_repo_owner
  github_repo_name     = var.github_repo_name
  github_repo_ref      = var.github_repo_ref
}


