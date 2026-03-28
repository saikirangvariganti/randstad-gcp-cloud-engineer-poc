# On-Premises to GCP Migration Assessment Runbook

## Overview

This runbook documents the assessment process for migrating on-premises workloads to Google Cloud
using **Migrate for Compute Engine** (formerly Velostrata). It covers discovery, assessment,
dependency mapping, and readiness evaluation for migration waves.

---

## Phase 1: Discovery and Inventory

### 1.1 Install Migrate for Compute Engine Manager

```bash
# Download Migrate for Compute Engine Manager OVA
# Deploy on vSphere or install on-premises

# Configure connection to GCP
gcloud auth application-default login
gcloud config set project PROJECT_ID
```

### 1.2 Discover On-Premises VMs

```bash
# List all discovered workloads
gcloud compute migrate sources list --project=PROJECT_ID

# Get details on a specific source
gcloud compute migrate sources describe SOURCE_NAME --project=PROJECT_ID
```

### 1.3 Inventory Collection Checklist

- [ ] Total number of VMs to migrate
- [ ] Operating system versions (Windows/Linux distributions)
- [ ] CPU and memory utilization per VM
- [ ] Storage capacity and IOPS requirements
- [ ] Network topology and firewall rules
- [ ] Application dependencies and service maps
- [ ] Database versions and sizes
- [ ] Third-party software licenses
- [ ] High-availability and DR requirements

---

## Phase 2: Application Dependency Mapping

### 2.1 Network Traffic Analysis

```bash
# Enable VPC Flow Logs for analysis
gcloud compute networks subnets update SUBNET_NAME \
  --region=REGION \
  --enable-flow-logs \
  --logging-aggregation-interval=INTERVAL_5_SEC \
  --logging-flow-sampling=1.0

# Query flow logs in BigQuery
bq query --use_legacy_sql=false '
SELECT
  connection.src_ip,
  connection.dest_ip,
  connection.dest_port,
  SUM(bytes_sent) as total_bytes,
  COUNT(*) as connection_count
FROM `PROJECT_ID.DATASET.compute_vpc_flows`
WHERE DATE(start_time) = CURRENT_DATE()
GROUP BY 1, 2, 3
ORDER BY total_bytes DESC
LIMIT 100
'
```

### 2.2 Application Tiers Identification

| Tier | Components | Migration Strategy |
|------|------------|-------------------|
| Web | Nginx/Apache front-ends | Lift and shift to GKE |
| App | Microservices | Replatform to containers |
| Database | PostgreSQL, MySQL | Migrate to Cloud SQL |
| Cache | Redis | Migrate to Memorystore |
| Message Queue | RabbitMQ | Migrate to Pub/Sub |

### 2.3 Dependency Matrix

```
[Load Balancer] → [Web Tier VMs] → [App Tier VMs] → [Database VMs]
                                 ↓                 ↓
                            [Cache VMs]      [File Storage]
```

---

## Phase 3: Assessment and Sizing

### 3.1 GCP Machine Type Mapping

```bash
# Run Migration Center discovery agent
# Install on each source VM
curl -O https://dl.google.com/cloudmigration/migrationcenter/mc-agent-latest.deb
sudo dpkg -i mc-agent-latest.deb
sudo systemctl start google-migration-center-agent

# View recommendations
gcloud migration-center assets list --project=PROJECT_ID
```

### 3.2 On-Premises to GCP Sizing Guidelines

| On-Prem vCPU | On-Prem RAM | Recommended GCP Type |
|-------------|-------------|---------------------|
| 2 vCPU / 4GB | Standard workload | e2-standard-2 |
| 4 vCPU / 16GB | Web/App servers | e2-standard-4 |
| 8 vCPU / 32GB | Database servers | n2-standard-8 |
| 16 vCPU / 64GB | Heavy compute | n2-standard-16 |

### 3.3 TCO Analysis

```bash
# Export pricing estimate
gcloud beta billing accounts get-spot-price \
  --project=PROJECT_ID \
  --region=europe-west2
```

---

## Phase 4: Pre-Migration Preparation

### 4.1 Network Connectivity

```bash
# Set up Cloud Interconnect or VPN for migration traffic
gcloud compute vpn-tunnels create migration-tunnel \
  --peer-address=ONPREM_GATEWAY_IP \
  --shared-secret=VPN_SECRET \
  --ike-version=2 \
  --local-traffic-selector=0.0.0.0/0 \
  --remote-traffic-selector=0.0.0.0/0 \
  --region=europe-west2 \
  --vpn-gateway=projects/PROJECT_ID/regions/europe-west2/vpnGateways/GATEWAY_NAME \
  --vpn-gateway-interface=0
```

### 4.2 IAM and Permissions Setup

```bash
# Create migration service account
gcloud iam service-accounts create migration-sa \
  --display-name="Migration Service Account"

# Grant required permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:migration-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/compute.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:migration-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

### 4.3 Storage Bucket for Migration

```bash
# Create staging bucket
gsutil mb -l europe-west2 gs://PROJECT_ID-migration-staging
gsutil versioning set on gs://PROJECT_ID-migration-staging
```

---

## Phase 5: Migration Execution Checklist

- [ ] Connectivity verified (VPN/Interconnect active)
- [ ] DNS records documented
- [ ] Backup of all source VMs completed
- [ ] Runbook reviewed and approved by stakeholders
- [ ] Rollback plan documented
- [ ] Change management ticket created
- [ ] Monitoring dashboards prepared
- [ ] Support teams on standby
- [ ] Migration window communicated

---

## Phase 6: Post-Migration Validation

### 6.1 Validation Checklist

- [ ] All VMs running in GCP
- [ ] Network connectivity between tiers
- [ ] Application health checks passing
- [ ] Database connections functional
- [ ] Load balancers forwarding traffic
- [ ] DNS updated to GCP endpoints
- [ ] SSL certificates active
- [ ] Monitoring and alerting active
- [ ] Backup jobs running

### 6.2 Performance Baseline Comparison

```bash
# Compare CPU/memory usage
gcloud monitoring metrics list --filter="metric.type=compute.googleapis.com/instance/cpu"

# Query metrics
gcloud monitoring read "metric.type=\"compute.googleapis.com/instance/cpu/utilization\" AND resource.labels.instance_id=\"INSTANCE_ID\""
```

---

## Rollback Procedure

```bash
# If migration fails, revert DNS to on-premises IPs
# Stop replicated VMs in GCP

# Restore from backup if needed
gcloud compute disks create DISK_NAME \
  --source-snapshot=SNAPSHOT_NAME \
  --zone=ZONE

# Remove failed GCP resources
gcloud compute instances delete INSTANCE_NAME --zone=ZONE
```

---

## Contact Matrix

| Role | Name | Responsibility |
|------|------|----------------|
| Migration Lead | TBD | Overall coordination |
| Network Engineer | TBD | VPN/Interconnect |
| GCP Architect | Sai Kiran Goud Variganti | Cloud architecture |
| DBA | TBD | Database migration |
| App Owner | TBD | Application validation |
