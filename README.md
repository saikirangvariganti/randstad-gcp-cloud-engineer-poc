# Randstad GCP Cloud Engineer POC

**Author:** Sai Kiran Goud Variganti
**GitHub:** [saikirangvariganti/randstad-gcp-cloud-engineer-poc](https://github.com/saikirangvariganti/randstad-gcp-cloud-engineer-poc)
**Role Target:** GCP Cloud Engineer — Randstad

---

## Overview

This POC demonstrates end-to-end GCP cloud engineering capabilities including:

- **Terraform IaC** — modular infrastructure for GKE, VPC, Cloud SQL, Cloud Storage, IAM, and Secret Manager
- **CI/CD Pipeline** — GitHub Actions with Checkov security scanning, Trivy image scanning, and Artifact Registry push; Cloud Build integration
- **GitOps with ArgoCD** — Helm chart deployments with automated sync and self-heal
- **Security** — VPC Service Controls perimeter, Cloud Armor WAF with OWASP rules, Network Policies
- **Observability** — Prometheus metrics collection, Grafana dashboard with GKE and application panels
- **On-Premises Migration** — Migrate for Compute Engine runbook, wave plan, and Terraform landing zone

---

## Architecture

```
Internet
    |
[Cloud Armor WAF]
    |
[Google Cloud Load Balancing]
    |
[GKE Cluster — europe-west2]
  |           |
[App Pods]  [ArgoCD]
  |
[Cloud SQL (PostgreSQL)]  [Cloud Storage]  [Secret Manager]
  |
[VPC Service Controls Perimeter]
  |
[On-Premises via Cloud VPN / Interconnect]
```

---

## Repository Structure

```
.
├── terraform/                  # Terraform IaC
│   ├── main.tf                 # Root module
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       ├── gke/               # GKE cluster + node pool
│       ├── vpc/               # VPC, subnets, NAT, firewall
│       ├── cloud_sql/         # Cloud SQL PostgreSQL
│       ├── cloud_storage/     # Cloud Storage bucket
│       ├── iam/               # Service accounts + IAM bindings
│       └── secret_manager/    # Secret Manager secrets
├── k8s/                        # Kubernetes manifests
│   ├── deployment.yaml         # App deployment (3 replicas, non-root)
│   ├── service.yaml            # ClusterIP service
│   ├── ingress.yaml            # GCE ingress with HTTPS
│   └── network_policy.yaml     # Network policies (deny-all + allow)
├── helm/                       # Helm chart
│   └── app-chart/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── argocd/                     # ArgoCD application manifest
│   └── application.yaml        # Auto-sync with self-heal
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions CI/CD
├── cloud-build/
│   └── cloudbuild.yaml         # Cloud Build pipeline
├── security/
│   ├── vpc_service_controls.tf # VPC-SC perimeter
│   └── cloud_armor.tf         # WAF + rate limiting + DDoS
├── monitoring/
│   ├── prometheus.yml          # Prometheus scrape config
│   └── grafana_dashboard.json  # Pre-built Grafana dashboard
├── migration/
│   ├── assessment_runbook.md   # Migration assessment steps
│   ├── wave_plan.md            # 4-wave migration plan
│   └── terraform_landing_zone.tf # Landing zone + HA VPN
├── app/
│   ├── main.py                 # Flask app with /health, /metrics
│   ├── requirements.txt
│   └── Dockerfile              # Multi-stage, non-root container
└── tests/
    └── test_poc.py             # 85+ pytest tests
```

---

## Key GCP Services Demonstrated

| Service | Usage |
|---------|-------|
| GKE | Private cluster, Workload Identity, Network Policy, node autoscaling |
| Cloud SQL | PostgreSQL 14, regional HA, private IP, automatic backups |
| Cloud Storage | Uniform bucket-level access, versioning, lifecycle rules |
| Secret Manager | Regional replication, IAM-bound access |
| Artifact Registry | Docker image storage for CI/CD |
| Cloud Build | Managed CI/CD with Checkov + Trivy |
| Cloud Armor | WAF (OWASP Top 10), rate limiting, adaptive DDoS protection |
| VPC Service Controls | Service perimeter for data exfiltration prevention |
| Cloud VPN / Interconnect | HA VPN for on-premises migration connectivity |

---

## Infrastructure Deployment

### Prerequisites

- Terraform >= 1.3
- `gcloud` CLI authenticated
- GCP project with billing enabled

### Deploy

```bash
cd terraform/

# Initialize
terraform init

# Plan
terraform plan -var="project_id=YOUR_PROJECT_ID" \
  -var="bucket_name=YOUR_BUCKET_NAME" \
  -var="db_password=YOUR_DB_PASSWORD" \
  -var="api_key=YOUR_API_KEY"

# Apply
terraform apply
```

---

## CI/CD Pipeline

### GitHub Actions (`ci.yml`)

1. **Security Scan** — Checkov on Terraform + Kubernetes manifests
2. **Build + Trivy Scan** — Docker image build + vulnerability scan
3. **Push to Artifact Registry** — On merge to main (Workload Identity Federation)
4. **ArgoCD Sync** — Triggered after push

### Cloud Build (`cloudbuild.yaml`)

Parallel Checkov scans → Docker build → Trivy → Artifact Registry push → ArgoCD sync

---

## GitOps with ArgoCD

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Apply application
kubectl apply -f argocd/application.yaml

# Watch sync
argocd app watch randstad-gcp-app
```

---

## Observability

### Prometheus

```bash
# Deploy Prometheus (example with Helm)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus \
  --values monitoring/prometheus.yml \
  -n monitoring
```

### Grafana

Import `monitoring/grafana_dashboard.json` via Grafana UI > Dashboards > Import.

---

## Security Features

### Cloud Armor WAF Rules

- SQL injection (OWASP CRS)
- XSS protection (OWASP CRS)
- LFI/RFI protection
- Rate limiting (1000 req/min per IP)
- Adaptive DDoS protection (Layer 7)

### VPC Service Controls

- Perimeter protecting: Cloud Storage, Cloud SQL, Secret Manager, GKE, Cloud KMS
- On-premises access via Access Level
- Ingress/Egress policies for controlled data movement

---

## On-Premises Migration

See `migration/` for:
- `assessment_runbook.md` — Discovery, dependency mapping, sizing, cutover steps
- `wave_plan.md` — 4-wave phased migration plan with rollback procedures
- `terraform_landing_zone.tf` — HA VPN, BGP, landing zone VPC, migration staging bucket

---

## Running Tests

```bash
cd tests/
pip install pytest pyyaml
pytest test_poc.py -v
```

---

## License

MIT License — For educational and demonstration purposes.
