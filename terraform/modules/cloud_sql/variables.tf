variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "instance_name" {
  description = "Name of the Cloud SQL instance"
  type        = string
  default     = "randstad-gcp-db"
}

variable "database_version" {
  description = "Database version"
  type        = string
  default     = "POSTGRES_14"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west2"
}

variable "tier" {
  description = "Machine tier for Cloud SQL"
  type        = string
  default     = "db-custom-2-7680"
}

variable "availability_type" {
  description = "Availability type: REGIONAL or ZONAL"
  type        = string
  default     = "REGIONAL"
}

variable "disk_size" {
  description = "Disk size in GB"
  type        = number
  default     = 50
}

variable "private_network" {
  description = "VPC network for private IP"
  type        = string
}

variable "database_name" {
  description = "Name of the database"
  type        = string
  default     = "appdb"
}

variable "db_user" {
  description = "Database user name"
  type        = string
  default     = "appuser"
}

variable "db_password" {
  description = "Database user password"
  type        = string
  sensitive   = true
}

variable "deletion_protection" {
  description = "Enable deletion protection"
  type        = bool
  default     = true
}
