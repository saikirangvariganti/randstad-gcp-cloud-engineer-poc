output "db_password_secret_name" {
  description = "The full resource name of the db password secret"
  value       = google_secret_manager_secret.db_password.name
}

output "api_key_secret_name" {
  description = "The full resource name of the API key secret"
  value       = google_secret_manager_secret.api_key.name
}

output "db_password_version_id" {
  description = "The version ID of the db password secret"
  value       = google_secret_manager_secret_version.db_password_version.id
}
