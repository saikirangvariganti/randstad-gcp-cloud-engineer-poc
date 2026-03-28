# Migration Wave Plan — On-Premises to GCP

## Overview

This document defines the phased migration approach using **Migrate for Compute Engine**,
organized into waves to minimize risk and enable incremental validation.

---

## Wave Summary

| Wave | Scope | Timeline | Risk | VMs |
|------|-------|----------|------|-----|
| Wave 0 | Pilot (non-production) | Week 1-2 | Low | 2-5 |
| Wave 1 | Web/Frontend tier | Week 3-4 | Medium | 5-10 |
| Wave 2 | Application tier | Week 5-7 | Medium | 10-15 |
| Wave 3 | Database tier | Week 8-10 | High | 3-5 |
| Wave 4 | Remaining services | Week 11-12 | Low | 5-8 |

---

## Wave 0: Pilot Migration

### Objectives
- Validate Migrate for Compute Engine tooling
- Test network connectivity between on-premises and GCP
- Establish migration procedures and runbooks
- Validate monitoring and observability

### Included Systems
- Development environment web servers (2 VMs)
- Development database (1 VM)
- Build/CI server (1 VM)

### Success Criteria
- [ ] All pilot VMs running in GCP
- [ ] Applications functioning correctly
- [ ] Monitoring data flowing to Prometheus/Grafana
- [ ] Rollback procedure tested and validated

### Migration Steps

```bash
# Step 1: Create migration job for pilot VMs
gcloud compute migrate migrate-instances create pilot-migration \
  --project=PROJECT_ID \
  --source=SOURCE_ENVIRONMENT \
  --target-project=PROJECT_ID \
  --target-zone=europe-west2-a

# Step 2: Start replication
gcloud compute migrate migrate-instances start-replication pilot-vm-1 \
  --project=PROJECT_ID

# Step 3: Monitor replication progress
gcloud compute migrate migrate-instances describe pilot-vm-1 \
  --project=PROJECT_ID

# Step 4: Perform cutover test
gcloud compute migrate migrate-instances cutover pilot-vm-1 \
  --project=PROJECT_ID

# Step 5: Validate application
curl -f https://PILOT_APP_URL/health
```

---

## Wave 1: Web/Frontend Tier

### Objectives
- Migrate all web/frontend servers to GKE
- Configure Cloud Armor WAF
- Set up HTTPS load balancing with managed certificates

### Included Systems
- Web application servers (5 VMs → GKE Deployment)
- Static asset servers (3 VMs → Cloud Storage)
- CDN configuration

### Architecture Change
- VMs → GKE containers (replatform)
- Local file storage → Cloud Storage
- On-premises load balancer → Google Cloud Load Balancing + Cloud Armor

### Migration Steps

```bash
# Step 1: Containerize web application
docker build -t europe-west2-docker.pkg.dev/PROJECT_ID/randstad-repo/web-app:v1 .
docker push europe-west2-docker.pkg.dev/PROJECT_ID/randstad-repo/web-app:v1

# Step 2: Deploy to GKE
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Step 3: Migrate static assets
gsutil -m rsync -r /var/www/static gs://PROJECT_ID-static-assets/

# Step 4: DNS cutover
gcloud dns record-sets update www.example.com \
  --type=A \
  --ttl=300 \
  --rrdatas=LOAD_BALANCER_IP \
  --zone=example-com

# Step 5: Validate
kubectl get pods -n default
kubectl get ingress
curl -f https://www.example.com/health
```

### Rollback Plan
```bash
# Revert DNS to on-premises IP
gcloud dns record-sets update www.example.com \
  --type=A \
  --ttl=60 \
  --rrdatas=ONPREM_IP \
  --zone=example-com
```

---

## Wave 2: Application Tier

### Objectives
- Migrate microservices to GKE
- Configure service mesh (if applicable)
- Establish inter-service communication via Kubernetes Services

### Included Systems
- Auth service (1 VM → GKE)
- API gateway (2 VMs → GKE)
- Order processing service (3 VMs → GKE)
- Notification service (2 VMs → GKE)

### Migration Steps

```bash
# Containerize each service
for service in auth api-gateway order-processing notification; do
  docker build -t europe-west2-docker.pkg.dev/PROJECT_ID/randstad-repo/${service}:v1 \
    services/${service}/
  docker push europe-west2-docker.pkg.dev/PROJECT_ID/randstad-repo/${service}:v1
done

# Deploy via ArgoCD GitOps
git add k8s/
git commit -m "Add wave 2 services deployment manifests"
git push origin main

# Monitor ArgoCD sync
argocd app sync randstad-gcp-app
argocd app wait randstad-gcp-app --health
```

---

## Wave 3: Database Tier (High Risk)

### Objectives
- Migrate PostgreSQL databases to Cloud SQL
- Ensure zero data loss using continuous replication
- Validate HA and backup configurations

### Included Systems
- Primary PostgreSQL (1 VM → Cloud SQL Regional)
- Read replicas (2 VMs → Cloud SQL Read Replicas)
- Redis cache (1 VM → Memorystore)

### Database Migration Steps

```bash
# Step 1: Export database from on-premises
pg_dump -h ONPREM_DB_HOST -U dbadmin -d appdb -Fc -f appdb_export.dump

# Step 2: Upload to Cloud Storage
gsutil cp appdb_export.dump gs://PROJECT_ID-migration-staging/db/

# Step 3: Import to Cloud SQL
gcloud sql import sql CLOUDSQL_INSTANCE \
  gs://PROJECT_ID-migration-staging/db/appdb_export.dump \
  --database=appdb \
  --user=dbadmin

# Step 4: Set up continuous replication (using pglogical or Cloud DMS)
gcloud database-migration migration-jobs create db-migration \
  --region=europe-west2 \
  --source=SOURCE_CONNECTION \
  --destination=DESTINATION_CONNECTION \
  --migration-job-id=appdb-migration

# Step 5: Start migration
gcloud database-migration migration-jobs start db-migration \
  --region=europe-west2

# Step 6: Monitor replication lag
gcloud database-migration migration-jobs describe db-migration \
  --region=europe-west2

# Step 7: Promote replica and cut over
gcloud database-migration migration-jobs promote db-migration \
  --region=europe-west2
```

### Data Validation Queries

```sql
-- Row count comparison
SELECT schemaname, tablename, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Checksum comparison (run on both source and target)
SELECT
  table_name,
  count(*) as row_count,
  md5(array_to_string(ARRAY(
    SELECT row_to_json(t)::text
    FROM (SELECT * FROM information_schema.columns WHERE table_name = t.table_name) t
  ), '')) as schema_hash
FROM information_schema.tables
WHERE table_schema = 'public'
GROUP BY table_name;
```

---

## Wave 4: Remaining Services

### Objectives
- Migrate remaining low-priority services
- Decommission on-premises VMs
- Final validation and sign-off

### Included Systems
- Internal tools and dashboards
- Batch processing jobs
- Logging and monitoring agents

### Decommission Checklist

- [ ] All applications validated in GCP
- [ ] DNS records updated
- [ ] SSL certificates active
- [ ] Backups running on schedule
- [ ] On-premises VMs powered off (not deleted for 30 days)
- [ ] Firewall rules for on-premises access reviewed
- [ ] Final stakeholder sign-off obtained
- [ ] Migration complete report generated

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data loss during DB migration | Low | High | Continuous replication + validation |
| Network latency increase | Medium | Medium | Cloud Interconnect, CDN |
| Application compatibility issues | Medium | High | Testing in Wave 0 |
| Licensing issues | Low | Medium | License audit before migration |
| Extended downtime during cutover | Low | High | Blue-green deployment strategy |

---

## Communication Plan

| Milestone | Stakeholders | Communication Method |
|-----------|-------------|---------------------|
| Wave start | IT + Business | Email + Slack |
| DNS cutover | IT + End users | Email + Status page |
| Wave complete | All stakeholders | Meeting + Report |
| Final completion | Executive team | Presentation |
