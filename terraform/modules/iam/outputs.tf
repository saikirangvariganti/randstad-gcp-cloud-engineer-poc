output "gke_sa_email" {
  description = "Email of the GKE node service account"
  value       = google_service_account.gke_sa.email
}

output "cicd_sa_email" {
  description = "Email of the CI/CD service account"
  value       = google_service_account.cicd_sa.email
}

output "app_sa_email" {
  description = "Email of the application service account"
  value       = google_service_account.app_sa.email
}
