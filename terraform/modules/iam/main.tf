terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }
}

resource "google_service_account" "gke_sa" {
  account_id   = var.gke_sa_name
  display_name = "GKE Workload Identity Service Account"
  project      = var.project_id
}

resource "google_service_account" "cicd_sa" {
  account_id   = var.cicd_sa_name
  display_name = "CI/CD Pipeline Service Account"
  project      = var.project_id
}

resource "google_service_account" "app_sa" {
  account_id   = var.app_sa_name
  display_name = "Application Service Account"
  project      = var.project_id
}

resource "google_project_iam_member" "gke_sa_roles" {
  for_each = toset(var.gke_sa_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.gke_sa.email}"
}

resource "google_project_iam_member" "cicd_sa_roles" {
  for_each = toset(var.cicd_sa_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.cicd_sa.email}"
}

resource "google_project_iam_member" "app_sa_roles" {
  for_each = toset(var.app_sa_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.app_sa.email}"
}

resource "google_service_account_iam_member" "workload_identity_binding" {
  service_account_id = google_service_account.app_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.k8s_namespace}/${var.k8s_service_account}]"
}
