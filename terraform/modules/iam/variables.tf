variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "gke_sa_name" {
  description = "Service account name for GKE nodes"
  type        = string
  default     = "gke-node-sa"
}

variable "cicd_sa_name" {
  description = "Service account name for CI/CD"
  type        = string
  default     = "cicd-sa"
}

variable "app_sa_name" {
  description = "Service account name for the application"
  type        = string
  default     = "app-sa"
}

variable "gke_sa_roles" {
  description = "IAM roles for the GKE node service account"
  type        = list(string)
  default = [
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/artifactregistry.reader",
  ]
}

variable "cicd_sa_roles" {
  description = "IAM roles for the CI/CD service account"
  type        = list(string)
  default = [
    "roles/artifactregistry.writer",
    "roles/container.developer",
    "roles/cloudbuild.builds.builder",
    "roles/secretmanager.secretAccessor",
  ]
}

variable "app_sa_roles" {
  description = "IAM roles for the application service account"
  type        = list(string)
  default = [
    "roles/cloudsql.client",
    "roles/secretmanager.secretAccessor",
    "roles/storage.objectViewer",
  ]
}

variable "k8s_namespace" {
  description = "Kubernetes namespace for workload identity"
  type        = string
  default     = "default"
}

variable "k8s_service_account" {
  description = "Kubernetes service account for workload identity"
  type        = string
  default     = "app-sa"
}
