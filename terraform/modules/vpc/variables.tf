variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "network_name" {
  description = "Name of the VPC network"
  type        = string
  default     = "randstad-gcp-vpc"
}

variable "subnet_name" {
  description = "Name of the subnet"
  type        = string
  default     = "randstad-gcp-subnet"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west2"
}

variable "subnet_cidr" {
  description = "CIDR range for the subnet"
  type        = string
  default     = "10.0.0.0/24"
}

variable "pods_cidr" {
  description = "CIDR range for pods"
  type        = string
  default     = "10.1.0.0/16"
}

variable "services_cidr" {
  description = "CIDR range for services"
  type        = string
  default     = "10.2.0.0/20"
}
