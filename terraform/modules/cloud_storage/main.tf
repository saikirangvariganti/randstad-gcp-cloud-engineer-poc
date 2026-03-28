terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }
}

resource "google_storage_bucket" "app_bucket" {
  name          = var.bucket_name
  location      = var.location
  project       = var.project_id
  storage_class = var.storage_class

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
    condition {
      age = 30
    }
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age                   = 365
      with_state            = "ARCHIVED"
      num_newer_versions    = 3
    }
  }

  retention_policy {
    retention_period = 86400
  }

  encryption {
    default_kms_key_name = var.kms_key_name
  }

  logging {
    log_bucket = var.log_bucket
  }

  labels = var.labels
}

resource "google_storage_bucket_iam_binding" "app_bucket_binding" {
  bucket = google_storage_bucket.app_bucket.name
  role   = "roles/storage.objectViewer"

  members = var.bucket_viewers
}
