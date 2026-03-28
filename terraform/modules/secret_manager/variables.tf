variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "primary_region" {
  description = "Primary region for secret replication"
  type        = string
  default     = "europe-west2"
}

variable "secondary_region" {
  description = "Secondary region for secret replication"
  type        = string
  default     = "europe-west1"
}

variable "db_password_secret_id" {
  description = "Secret ID for the database password"
  type        = string
  default     = "db-password"
}

variable "db_password_value" {
  description = "Value of the database password"
  type        = string
  sensitive   = true
}

variable "api_key_secret_id" {
  description = "Secret ID for the API key"
  type        = string
  default     = "api-key"
}

variable "api_key_value" {
  description = "Value of the API key"
  type        = string
  sensitive   = true
}

variable "app_sa_email" {
  description = "Email of the application service account"
  type        = string
}
