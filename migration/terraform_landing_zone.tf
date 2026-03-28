terraform {
  required_version = ">= 1.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }
}

# Landing Zone VPC for migrated workloads
resource "google_compute_network" "landing_zone_vpc" {
  name                    = "landing-zone-vpc"
  auto_create_subnetworks = false
  project                 = var.project_id
  description             = "Landing zone VPC for on-prem to GCP migrations"
}

# Landing Zone Subnet
resource "google_compute_subnetwork" "landing_zone_subnet" {
  name          = "landing-zone-subnet"
  ip_cidr_range = var.landing_zone_cidr
  region        = var.region
  network       = google_compute_network.landing_zone_vpc.id
  project       = var.project_id

  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "migration-staging"
    ip_cidr_range = var.migration_staging_cidr
  }
}

# Cloud VPN for on-premises connectivity
resource "google_compute_ha_vpn_gateway" "ha_vpn" {
  name    = "landing-zone-ha-vpn"
  network = google_compute_network.landing_zone_vpc.id
  region  = var.region
  project = var.project_id
}

resource "google_compute_external_vpn_gateway" "onprem_gateway" {
  name            = "onprem-vpn-gateway"
  redundancy_type = "TWO_IPS_REDUNDANCY"
  description     = "On-premises VPN gateway for migration"
  project         = var.project_id

  interface {
    id         = 0
    ip_address = var.onprem_vpn_ip_1
  }

  interface {
    id         = 1
    ip_address = var.onprem_vpn_ip_2
  }
}

resource "google_compute_router" "landing_zone_router" {
  name    = "landing-zone-router"
  region  = var.region
  network = google_compute_network.landing_zone_vpc.id
  project = var.project_id

  bgp {
    asn               = var.gcp_bgp_asn
    advertise_mode    = "CUSTOM"
    advertised_groups = ["ALL_SUBNETS"]
    advertised_ip_ranges {
      range = var.landing_zone_cidr
    }
  }
}

# VPN Tunnels for HA connectivity
resource "google_compute_vpn_tunnel" "tunnel_1" {
  name                  = "landing-zone-tunnel-1"
  region                = var.region
  project               = var.project_id
  vpn_gateway           = google_compute_ha_vpn_gateway.ha_vpn.id
  peer_external_gateway = google_compute_external_vpn_gateway.onprem_gateway.id
  shared_secret         = var.vpn_shared_secret
  router                = google_compute_router.landing_zone_router.id
  vpn_gateway_interface = 0
  peer_external_gateway_interface = 0
}

resource "google_compute_vpn_tunnel" "tunnel_2" {
  name                  = "landing-zone-tunnel-2"
  region                = var.region
  project               = var.project_id
  vpn_gateway           = google_compute_ha_vpn_gateway.ha_vpn.id
  peer_external_gateway = google_compute_external_vpn_gateway.onprem_gateway.id
  shared_secret         = var.vpn_shared_secret
  router                = google_compute_router.landing_zone_router.id
  vpn_gateway_interface = 1
  peer_external_gateway_interface = 1
}

# BGP Sessions
resource "google_compute_router_interface" "router_interface_1" {
  name       = "router-interface-1"
  router     = google_compute_router.landing_zone_router.name
  region     = var.region
  project    = var.project_id
  ip_range   = "${var.bgp_peer_ip_1}/30"
  vpn_tunnel = google_compute_vpn_tunnel.tunnel_1.name
}

resource "google_compute_router_peer" "bgp_peer_1" {
  name                      = "bgp-peer-1"
  router                    = google_compute_router.landing_zone_router.name
  region                    = var.region
  project                   = var.project_id
  peer_ip_address           = var.onprem_bgp_ip_1
  peer_asn                  = var.onprem_bgp_asn
  advertised_route_priority = 100
  interface                 = google_compute_router_interface.router_interface_1.name
}

# Migration staging bucket
resource "google_storage_bucket" "migration_staging" {
  name          = "${var.project_id}-migration-staging"
  location      = var.region
  project       = var.project_id
  storage_class = "REGIONAL"

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 90
    }
  }
}

# Firewall rules for migration traffic
resource "google_compute_firewall" "allow_migration" {
  name    = "allow-migration-traffic"
  network = google_compute_network.landing_zone_vpc.name
  project = var.project_id

  allow {
    protocol = "tcp"
    ports    = ["443", "9418", "22"]
  }

  source_ranges = [var.onprem_cidr]
  description   = "Allow migration traffic from on-premises"
}

# Variables
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west2"
}

variable "landing_zone_cidr" {
  description = "CIDR for landing zone subnet"
  type        = string
  default     = "10.200.0.0/24"
}

variable "migration_staging_cidr" {
  description = "CIDR for migration staging range"
  type        = string
  default     = "10.201.0.0/24"
}

variable "onprem_vpn_ip_1" {
  description = "First on-premises VPN gateway IP"
  type        = string
}

variable "onprem_vpn_ip_2" {
  description = "Second on-premises VPN gateway IP"
  type        = string
}

variable "gcp_bgp_asn" {
  description = "GCP BGP ASN"
  type        = number
  default     = 65001
}

variable "onprem_bgp_asn" {
  description = "On-premises BGP ASN"
  type        = number
  default     = 65002
}

variable "vpn_shared_secret" {
  description = "Shared secret for VPN tunnels"
  type        = string
  sensitive   = true
}

variable "onprem_cidr" {
  description = "On-premises network CIDR"
  type        = string
  default     = "192.168.0.0/16"
}

variable "bgp_peer_ip_1" {
  description = "BGP peer IP address 1"
  type        = string
  default     = "169.254.1.1"
}

variable "onprem_bgp_ip_1" {
  description = "On-premises BGP IP address 1"
  type        = string
  default     = "169.254.1.2"
}
