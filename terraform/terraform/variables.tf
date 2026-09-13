# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "github_repo_owner" {
  description = "GitHub repository owner (username or organization)"
  type        = string
}

variable "github_repo_name" {
  description = "GitHub repository name"
  type        = string
}

variable "github_repo_ref" {
  description = "GitHub repository branch for Workload Identity Federation (main or master)"
  type        = string
  default     = "main"
}

variable "gcs_bucket_prefix" {
  description = "Prefix for GCS bucket names (must be globally unique)"
  type        = string
}

variable "bigquery_dataset_id" {
  description = "BigQuery dataset ID"
  type        = string
  default     = "d1_staged_enforced"
}

variable "data_owner_email" {
  description = "Email of IAM principal who should have Row-Level Security access (leave empty to skip RLS binding)"
  type        = string
  default     = ""
}

variable "cmek_rotation_period" {
  description = "Rotation period for KMS key (e.g., 7776000s = 90 days)"
  type        = string
  default     = "7776000s"
}


