terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }
}

# VPC Service Controls Access Policy
resource "google_access_context_manager_access_policy" "policy" {
  parent = "organizations/${var.org_id}"
  title  = "Randstad GCP VPC Service Controls Policy"
}

# Access Level for on-premises network
resource "google_access_context_manager_access_level" "onprem_access" {
  parent = "accessPolicies/${google_access_context_manager_access_policy.policy.name}"
  name   = "accessPolicies/${google_access_context_manager_access_policy.policy.name}/accessLevels/onprem_access"
  title  = "On-premises Network Access"

  basic {
    conditions {
      ip_sub_networks = var.onprem_ip_ranges
    }
  }
}

# Access Level for trusted identities
resource "google_access_context_manager_access_level" "trusted_identity" {
  parent = "accessPolicies/${google_access_context_manager_access_policy.policy.name}"
  name   = "accessPolicies/${google_access_context_manager_access_policy.policy.name}/accessLevels/trusted_identity"
  title  = "Trusted Identity Access"

  basic {
    conditions {
      members = var.trusted_members
    }
  }
}

# VPC Service Perimeter
resource "google_access_context_manager_service_perimeter" "service_perimeter" {
  parent = "accessPolicies/${google_access_context_manager_access_policy.policy.name}"
  name   = "accessPolicies/${google_access_context_manager_access_policy.policy.name}/servicePerimeters/randstad_perimeter"
  title  = "Randstad GCP Service Perimeter"

  spec {
    restricted_services = [
      "storage.googleapis.com",
      "cloudsql.googleapis.com",
      "secretmanager.googleapis.com",
      "container.googleapis.com",
      "cloudkms.googleapis.com",
    ]

    resources = [
      "projects/${var.project_number}",
    ]

    access_levels = [
      google_access_context_manager_access_level.onprem_access.name,
      google_access_context_manager_access_level.trusted_identity.name,
    ]

    ingress_policies {
      ingress_from {
        sources {
          access_level = google_access_context_manager_access_level.onprem_access.name
        }
        identity_type = "ANY_SERVICE_ACCOUNT"
      }
      ingress_to {
        resources = ["*"]
        operations {
          service_name = "storage.googleapis.com"
          method_selectors {
            method = "*"
          }
        }
      }
    }

    egress_policies {
      egress_from {
        identity_type = "ANY_SERVICE_ACCOUNT"
      }
      egress_to {
        resources = ["*"]
        operations {
          service_name = "storage.googleapis.com"
          method_selectors {
            method = "*"
          }
        }
      }
    }
  }

  use_explicit_dry_run_spec = true
  status {
    restricted_services = [
      "storage.googleapis.com",
    ]
    resources = [
      "projects/${var.project_number}",
    ]
  }
}

variable "org_id" {
  description = "GCP Organization ID"
  type        = string
}

variable "project_number" {
  description = "GCP Project Number"
  type        = string
}

variable "onprem_ip_ranges" {
  description = "On-premises IP ranges for access"
  type        = list(string)
  default     = ["10.100.0.0/16"]
}

variable "trusted_members" {
  description = "Trusted identity members"
  type        = list(string)
  default     = []
}
