variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "Default GCP region"
  type        = string
  default     = "europe-west2"
}

variable "network_name" {
  description = "VPC network name"
  type        = string
  default     = "randstad-gcp-vpc"
}

variable "subnet_name" {
  description = "Subnet name"
  type        = string
  default     = "randstad-gcp-subnet"
}

variable "subnet_cidr" {
  description = "Subnet CIDR range"
  type        = string
  default     = "10.0.0.0/24"
}

variable "pods_cidr" {
  description = "Pods CIDR range"
  type        = string
  default     = "10.1.0.0/16"
}

variable "services_cidr" {
  description = "Services CIDR range"
  type        = string
  default     = "10.2.0.0/20"
}

variable "cluster_name" {
  description = "GKE cluster name"
  type        = string
  default     = "randstad-gcp-cluster"
}

variable "node_count" {
  description = "Initial node count"
  type        = number
  default     = 2
}

variable "min_node_count" {
  description = "Minimum node count"
  type        = number
  default     = 1
}

variable "max_node_count" {
  description = "Maximum node count"
  type        = number
  default     = 5
}

variable "machine_type" {
  description = "Node machine type"
  type        = string
  default     = "e2-standard-4"
}

variable "db_instance_name" {
  description = "Cloud SQL instance name"
  type        = string
  default     = "randstad-gcp-db"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "bucket_name" {
  description = "Cloud Storage bucket name"
  type        = string
}

variable "bucket_location" {
  description = "Bucket location"
  type        = string
  default     = "EU"
}

variable "api_key" {
  description = "API key secret value"
  type        = string
  sensitive   = true
}
