variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "bucket_name" {
  description = "Name of the Cloud Storage bucket"
  type        = string
}

variable "location" {
  description = "Bucket location"
  type        = string
  default     = "EU"
}

variable "storage_class" {
  description = "Storage class for the bucket"
  type        = string
  default     = "STANDARD"
}

variable "kms_key_name" {
  description = "KMS key for bucket encryption"
  type        = string
  default     = null
}

variable "log_bucket" {
  description = "Bucket for access logs"
  type        = string
  default     = ""
}

variable "labels" {
  description = "Labels for the bucket"
  type        = map(string)
  default     = {}
}

variable "bucket_viewers" {
  description = "List of members with viewer access"
  type        = list(string)
  default     = []
}
