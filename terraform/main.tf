terraform {
  required_version = ">= 1.3"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }

  backend "gcs" {
    bucket = "randstad-gcp-terraform-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "vpc" {
  source       = "./modules/vpc"
  project_id   = var.project_id
  network_name = var.network_name
  subnet_name  = var.subnet_name
  region       = var.region
  subnet_cidr  = var.subnet_cidr
  pods_cidr    = var.pods_cidr
  services_cidr = var.services_cidr
}

module "gke" {
  source         = "./modules/gke"
  project_id     = var.project_id
  cluster_name   = var.cluster_name
  region         = var.region
  network        = module.vpc.network_name
  subnetwork     = module.vpc.subnet_name
  node_count     = var.node_count
  min_node_count = var.min_node_count
  max_node_count = var.max_node_count
  machine_type   = var.machine_type

  depends_on = [module.vpc]
}

module "cloud_sql" {
  source          = "./modules/cloud_sql"
  project_id      = var.project_id
  instance_name   = var.db_instance_name
  region          = var.region
  private_network = module.vpc.network_id
  db_password     = var.db_password

  depends_on = [module.vpc]
}

module "cloud_storage" {
  source      = "./modules/cloud_storage"
  project_id  = var.project_id
  bucket_name = var.bucket_name
  location    = var.bucket_location
}

module "iam" {
  source     = "./modules/iam"
  project_id = var.project_id
}

module "secret_manager" {
  source               = "./modules/secret_manager"
  project_id           = var.project_id
  db_password_value    = var.db_password
  api_key_value        = var.api_key
  app_sa_email         = module.iam.app_sa_email

  depends_on = [module.iam]
}
