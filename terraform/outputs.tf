output "gke_cluster_name" {
  description = "GKE cluster name"
  value       = module.gke.cluster_name
}

output "vpc_network_name" {
  description = "VPC network name"
  value       = module.vpc.network_name
}

output "cloud_sql_connection_name" {
  description = "Cloud SQL connection name"
  value       = module.cloud_sql.connection_name
}

output "storage_bucket_url" {
  description = "Cloud Storage bucket URL"
  value       = module.cloud_storage.bucket_url
}

output "app_sa_email" {
  description = "Application service account email"
  value       = module.iam.app_sa_email
}
