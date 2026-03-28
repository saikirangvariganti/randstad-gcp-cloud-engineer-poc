terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }
}

# Cloud Armor Security Policy — WAF
resource "google_compute_security_policy" "waf_policy" {
  name        = "randstad-waf-policy"
  description = "Cloud Armor WAF policy for Randstad GCP POC"
  project     = var.project_id

  # Rule 1: Block known malicious IPs
  rule {
    action   = "deny(403)"
    priority = "1000"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = var.blocked_ip_ranges
      }
    }
    description = "Block known malicious IP ranges"
  }

  # Rule 2: OWASP Top 10 — SQL Injection protection
  rule {
    action   = "deny(403)"
    priority = "2000"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('sqli-stable', ['owasp-crs-v030001-id942110-sqli', 'owasp-crs-v030001-id942120-sqli'])"
      }
    }
    description = "OWASP SQL Injection protection"
  }

  # Rule 3: OWASP Top 10 — XSS protection
  rule {
    action   = "deny(403)"
    priority = "2001"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('xss-stable')"
      }
    }
    description = "OWASP XSS protection"
  }

  # Rule 4: OWASP Top 10 — LFI protection
  rule {
    action   = "deny(403)"
    priority = "2002"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('lfi-stable')"
      }
    }
    description = "OWASP LFI protection"
  }

  # Rule 5: OWASP Top 10 — RFI protection
  rule {
    action   = "deny(403)"
    priority = "2003"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('rfi-stable')"
      }
    }
    description = "OWASP RFI protection"
  }

  # Rule 6: Rate limiting — general
  rule {
    action   = "throttle"
    priority = "3000"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    description = "Rate limiting for all traffic"
    rate_limit_options {
      conform_action = "allow"
      exceed_action  = "deny(429)"
      enforce_on_key = "IP"
      rate_limit_threshold {
        count        = 1000
        interval_sec = 60
      }
    }
  }

  # Rule 7: Allow GFE health checks
  rule {
    action   = "allow"
    priority = "4000"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["35.191.0.0/16", "130.211.0.0/22"]
      }
    }
    description = "Allow Google Frontend health checks"
  }

  # Default rule: allow all
  rule {
    action   = "allow"
    priority = "2147483647"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    description = "Default allow rule"
  }

  adaptive_protection_config {
    layer_7_ddos_defense_config {
      enable          = true
      rule_visibility = "STANDARD"
    }
  }
}

# Attach WAF policy to backend service
resource "google_compute_backend_service" "app_backend" {
  name                  = "randstad-app-backend"
  project               = var.project_id
  protocol              = "HTTP"
  timeout_sec           = 30
  security_policy       = google_compute_security_policy.waf_policy.id
  load_balancing_scheme = "EXTERNAL_MANAGED"

  backend {
    group           = var.instance_group
    balancing_mode  = "UTILIZATION"
    max_utilization = 0.8
  }

  health_checks = [google_compute_health_check.default.id]

  cdn_policy {
    cache_mode        = "CACHE_ALL_STATIC"
    default_ttl       = 3600
    max_ttl           = 86400
    negative_caching  = true
  }

  log_config {
    enable      = true
    sample_rate = 1.0
  }
}

resource "google_compute_health_check" "default" {
  name               = "randstad-app-health-check"
  project            = var.project_id
  check_interval_sec = 10
  timeout_sec        = 5

  http_health_check {
    port         = 8080
    request_path = "/health"
  }
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "blocked_ip_ranges" {
  description = "IP ranges to block"
  type        = list(string)
  default     = []
}

variable "instance_group" {
  description = "Instance group URL for backend service"
  type        = string
  default     = ""
}
