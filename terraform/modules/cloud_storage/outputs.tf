output "bucket_name" {
  description = "The name of the storage bucket"
  value       = google_storage_bucket.app_bucket.name
}

output "bucket_url" {
  description = "The URL of the storage bucket"
  value       = google_storage_bucket.app_bucket.url
}

output "bucket_self_link" {
  description = "The self link of the storage bucket"
  value       = google_storage_bucket.app_bucket.self_link
}
