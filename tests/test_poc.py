"""
Comprehensive pytest test suite for Randstad GCP Cloud Engineer POC.

Covers:
- File/directory structure validation
- Terraform IaC content checks (root + all modules)
- GitHub Actions CI/CD pipeline YAML validation
- Cloud Build YAML validation
- Kubernetes manifest checks (Deployment, Service, Ingress, NetworkPolicy)
- Helm chart validation
- ArgoCD application manifest checks
- Security Terraform file checks (Cloud Armor, VPC-SC)
- Monitoring config (Prometheus, Grafana)
- Migration artefacts (runbook, wave plan, landing zone Terraform)
- Application code checks (Flask app, Dockerfile, requirements)
- README completeness checks
"""

from pathlib import Path
import json
import yaml

REPO_ROOT = Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _yaml(rel: str):
    with open(REPO_ROOT / rel, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _yaml_all(rel: str):
    with open(REPO_ROOT / rel, encoding="utf-8") as fh:
        return list(yaml.safe_load_all(fh))


# ===========================================================================
# 1. FILE STRUCTURE VALIDATION
# ===========================================================================

def test_repo_root_exists():
    assert REPO_ROOT.is_dir()

def test_readme_exists():
    assert (REPO_ROOT / "README.md").is_file()

def test_terraform_dir_exists():
    assert (REPO_ROOT / "terraform").is_dir()

def test_terraform_main_tf_exists():
    assert (REPO_ROOT / "terraform" / "main.tf").is_file()

def test_terraform_variables_tf_exists():
    assert (REPO_ROOT / "terraform" / "variables.tf").is_file()

def test_terraform_outputs_tf_exists():
    assert (REPO_ROOT / "terraform" / "outputs.tf").is_file()

def test_terraform_modules_dir_exists():
    assert (REPO_ROOT / "terraform" / "modules").is_dir()

def test_module_gke_main_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "gke" / "main.tf").is_file()

def test_module_gke_variables_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "gke" / "variables.tf").is_file()

def test_module_gke_outputs_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "gke" / "outputs.tf").is_file()

def test_module_vpc_main_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "vpc" / "main.tf").is_file()

def test_module_vpc_variables_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "vpc" / "variables.tf").is_file()

def test_module_vpc_outputs_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "vpc" / "outputs.tf").is_file()

def test_module_cloud_sql_main_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "cloud_sql" / "main.tf").is_file()

def test_module_cloud_storage_main_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "cloud_storage" / "main.tf").is_file()

def test_module_iam_main_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "iam" / "main.tf").is_file()

def test_module_secret_manager_main_exists():
    assert (REPO_ROOT / "terraform" / "modules" / "secret_manager" / "main.tf").is_file()

def test_k8s_dir_exists():
    assert (REPO_ROOT / "k8s").is_dir()

def test_k8s_deployment_yaml_exists():
    assert (REPO_ROOT / "k8s" / "deployment.yaml").is_file()

def test_k8s_service_yaml_exists():
    assert (REPO_ROOT / "k8s" / "service.yaml").is_file()

def test_k8s_ingress_yaml_exists():
    assert (REPO_ROOT / "k8s" / "ingress.yaml").is_file()

def test_k8s_network_policy_yaml_exists():
    assert (REPO_ROOT / "k8s" / "network_policy.yaml").is_file()

def test_helm_dir_exists():
    assert (REPO_ROOT / "helm").is_dir()

def test_helm_chart_yaml_exists():
    assert (REPO_ROOT / "helm" / "app-chart" / "Chart.yaml").is_file()

def test_helm_values_yaml_exists():
    assert (REPO_ROOT / "helm" / "app-chart" / "values.yaml").is_file()

def test_helm_deployment_template_exists():
    assert (REPO_ROOT / "helm" / "app-chart" / "templates" / "deployment.yaml").is_file()

def test_argocd_application_yaml_exists():
    assert (REPO_ROOT / "argocd" / "application.yaml").is_file()

def test_github_actions_ci_yml_exists():
    assert (REPO_ROOT / ".github" / "workflows" / "ci.yml").is_file()

def test_cloud_build_yaml_exists():
    assert (REPO_ROOT / "cloud-build" / "cloudbuild.yaml").is_file()

def test_security_cloud_armor_tf_exists():
    assert (REPO_ROOT / "security" / "cloud_armor.tf").is_file()

def test_security_vpc_service_controls_tf_exists():
    assert (REPO_ROOT / "security" / "vpc_service_controls.tf").is_file()

def test_monitoring_prometheus_yml_exists():
    assert (REPO_ROOT / "monitoring" / "prometheus.yml").is_file()

def test_monitoring_grafana_dashboard_exists():
    assert (REPO_ROOT / "monitoring" / "grafana_dashboard.json").is_file()

def test_migration_dir_exists():
    assert (REPO_ROOT / "migration").is_dir()

def test_migration_assessment_runbook_exists():
    assert (REPO_ROOT / "migration" / "assessment_runbook.md").is_file()

def test_migration_wave_plan_exists():
    assert (REPO_ROOT / "migration" / "wave_plan.md").is_file()

def test_migration_terraform_landing_zone_exists():
    assert (REPO_ROOT / "migration" / "terraform_landing_zone.tf").is_file()

def test_app_main_py_exists():
    assert (REPO_ROOT / "app" / "main.py").is_file()

def test_app_dockerfile_exists():
    assert (REPO_ROOT / "app" / "Dockerfile").is_file()

def test_app_requirements_txt_exists():
    assert (REPO_ROOT / "app" / "requirements.txt").is_file()


# ===========================================================================
# 2. TERRAFORM ROOT MODULE CHECKS
# ===========================================================================

def test_terraform_main_required_version():
    txt = _read("terraform/main.tf")
    assert ">= 1.3" in txt

def test_terraform_main_google_provider():
    txt = _read("terraform/main.tf")
    assert 'source  = "hashicorp/google"' in txt

def test_terraform_main_gcs_backend():
    txt = _read("terraform/main.tf")
    assert 'backend "gcs"' in txt

def test_terraform_main_module_vpc():
    txt = _read("terraform/main.tf")
    assert 'module "vpc"' in txt

def test_terraform_main_module_gke():
    txt = _read("terraform/main.tf")
    assert 'module "gke"' in txt

def test_terraform_main_module_cloud_sql():
    txt = _read("terraform/main.tf")
    assert 'module "cloud_sql"' in txt

def test_terraform_main_module_cloud_storage():
    txt = _read("terraform/main.tf")
    assert 'module "cloud_storage"' in txt

def test_terraform_main_module_iam():
    txt = _read("terraform/main.tf")
    assert 'module "iam"' in txt

def test_terraform_main_module_secret_manager():
    txt = _read("terraform/main.tf")
    assert 'module "secret_manager"' in txt

def test_terraform_main_depends_on_vpc():
    txt = _read("terraform/main.tf")
    assert "depends_on" in txt

def test_terraform_variables_project_id():
    txt = _read("terraform/variables.tf")
    assert 'variable "project_id"' in txt

def test_terraform_variables_region_default():
    txt = _read("terraform/variables.tf")
    assert "europe-west2" in txt

def test_terraform_variables_db_password_sensitive():
    txt = _read("terraform/variables.tf")
    assert "sensitive" in txt

def test_terraform_variables_api_key_sensitive():
    txt = _read("terraform/variables.tf")
    # api_key must also be marked sensitive
    assert txt.count("sensitive") >= 2

def test_terraform_outputs_gke_cluster_name():
    txt = _read("terraform/outputs.tf")
    assert 'output "gke_cluster_name"' in txt

def test_terraform_outputs_vpc_network_name():
    txt = _read("terraform/outputs.tf")
    assert 'output "vpc_network_name"' in txt

def test_terraform_outputs_cloud_sql_connection():
    txt = _read("terraform/outputs.tf")
    assert 'output "cloud_sql_connection_name"' in txt

def test_terraform_outputs_storage_bucket_url():
    txt = _read("terraform/outputs.tf")
    assert 'output "storage_bucket_url"' in txt


# ===========================================================================
# 3. TERRAFORM MODULE — GKE
# ===========================================================================

def test_gke_module_container_cluster_resource():
    txt = _read("terraform/modules/gke/main.tf")
    assert 'resource "google_container_cluster"' in txt

def test_gke_module_node_pool_resource():
    txt = _read("terraform/modules/gke/main.tf")
    assert 'resource "google_container_node_pool"' in txt

def test_gke_module_private_nodes_enabled():
    txt = _read("terraform/modules/gke/main.tf")
    assert "enable_private_nodes    = true" in txt

def test_gke_module_workload_identity():
    txt = _read("terraform/modules/gke/main.tf")
    assert "workload_identity_config" in txt

def test_gke_module_network_policy_calico():
    txt = _read("terraform/modules/gke/main.tf")
    assert "CALICO" in txt

def test_gke_module_autoscaling():
    txt = _read("terraform/modules/gke/main.tf")
    assert "autoscaling" in txt

def test_gke_module_auto_repair():
    txt = _read("terraform/modules/gke/main.tf")
    assert "auto_repair  = true" in txt

def test_gke_module_shielded_instance():
    txt = _read("terraform/modules/gke/main.tf")
    assert "shielded_instance_config" in txt

def test_gke_module_logging_config():
    txt = _read("terraform/modules/gke/main.tf")
    assert "logging_config" in txt

def test_gke_module_remove_default_node_pool():
    txt = _read("terraform/modules/gke/main.tf")
    assert "remove_default_node_pool = true" in txt


# ===========================================================================
# 4. TERRAFORM MODULE — VPC
# ===========================================================================

def test_vpc_module_compute_network_resource():
    txt = _read("terraform/modules/vpc/main.tf")
    assert 'resource "google_compute_network"' in txt

def test_vpc_module_compute_subnetwork_resource():
    txt = _read("terraform/modules/vpc/main.tf")
    assert 'resource "google_compute_subnetwork"' in txt

def test_vpc_module_nat_resource():
    txt = _read("terraform/modules/vpc/main.tf")
    assert 'resource "google_compute_router_nat"' in txt

def test_vpc_module_firewall_allow_internal():
    txt = _read("terraform/modules/vpc/main.tf")
    assert "allow_internal" in txt

def test_vpc_module_firewall_deny_all_ingress():
    txt = _read("terraform/modules/vpc/main.tf")
    assert "deny_all_ingress" in txt

def test_vpc_module_private_ip_google_access():
    txt = _read("terraform/modules/vpc/main.tf")
    assert "private_ip_google_access = true" in txt

def test_vpc_module_secondary_ip_ranges_pods():
    txt = _read("terraform/modules/vpc/main.tf")
    assert '"pods"' in txt

def test_vpc_module_secondary_ip_ranges_services():
    txt = _read("terraform/modules/vpc/main.tf")
    assert '"services"' in txt

def test_vpc_module_auto_create_subnetworks_false():
    txt = _read("terraform/modules/vpc/main.tf")
    assert "auto_create_subnetworks = false" in txt

def test_vpc_module_flow_logs():
    txt = _read("terraform/modules/vpc/main.tf")
    assert "log_config" in txt


# ===========================================================================
# 5. TERRAFORM MODULE — CLOUD SQL
# ===========================================================================

def test_cloud_sql_module_instance_resource():
    txt = _read("terraform/modules/cloud_sql/main.tf")
    assert 'resource "google_sql_database_instance"' in txt

def test_cloud_sql_module_database_resource():
    txt = _read("terraform/modules/cloud_sql/main.tf")
    assert 'resource "google_sql_database"' in txt

def test_cloud_sql_module_user_resource():
    txt = _read("terraform/modules/cloud_sql/main.tf")
    assert 'resource "google_sql_user"' in txt

def test_cloud_sql_backup_enabled():
    txt = _read("terraform/modules/cloud_sql/main.tf")
    assert "enabled                        = true" in txt

def test_cloud_sql_require_ssl():
    txt = _read("terraform/modules/cloud_sql/main.tf")
    assert "require_ssl     = true" in txt

def test_cloud_sql_private_ip_only():
    txt = _read("terraform/modules/cloud_sql/main.tf")
    assert "ipv4_enabled    = false" in txt

def test_cloud_sql_point_in_time_recovery():
    txt = _read("terraform/modules/cloud_sql/main.tf")
    assert "point_in_time_recovery_enabled = true" in txt

def test_cloud_sql_disk_autoresize():
    txt = _read("terraform/modules/cloud_sql/main.tf")
    assert "disk_autoresize   = true" in txt


# ===========================================================================
# 6. TERRAFORM MODULE — CLOUD STORAGE
# ===========================================================================

def test_cloud_storage_bucket_resource():
    txt = _read("terraform/modules/cloud_storage/main.tf")
    assert 'resource "google_storage_bucket"' in txt

def test_cloud_storage_uniform_bucket_access():
    txt = _read("terraform/modules/cloud_storage/main.tf")
    assert "uniform_bucket_level_access = true" in txt

def test_cloud_storage_public_access_prevention():
    txt = _read("terraform/modules/cloud_storage/main.tf")
    assert 'public_access_prevention    = "enforced"' in txt

def test_cloud_storage_versioning_enabled():
    txt = _read("terraform/modules/cloud_storage/main.tf")
    assert "enabled = true" in txt

def test_cloud_storage_lifecycle_rule_nearline():
    txt = _read("terraform/modules/cloud_storage/main.tf")
    assert "NEARLINE" in txt

def test_cloud_storage_lifecycle_rule_delete():
    txt = _read("terraform/modules/cloud_storage/main.tf")
    assert '"Delete"' in txt

def test_cloud_storage_iam_binding():
    txt = _read("terraform/modules/cloud_storage/main.tf")
    assert 'resource "google_storage_bucket_iam_binding"' in txt


# ===========================================================================
# 7. TERRAFORM MODULE — IAM
# ===========================================================================

def test_iam_gke_service_account():
    txt = _read("terraform/modules/iam/main.tf")
    assert 'resource "google_service_account" "gke_sa"' in txt

def test_iam_cicd_service_account():
    txt = _read("terraform/modules/iam/main.tf")
    assert 'resource "google_service_account" "cicd_sa"' in txt

def test_iam_app_service_account():
    txt = _read("terraform/modules/iam/main.tf")
    assert 'resource "google_service_account" "app_sa"' in txt

def test_iam_workload_identity_binding():
    txt = _read("terraform/modules/iam/main.tf")
    assert "workload_identity_binding" in txt

def test_iam_workload_identity_user_role():
    txt = _read("terraform/modules/iam/main.tf")
    assert "roles/iam.workloadIdentityUser" in txt

def test_iam_project_iam_members():
    txt = _read("terraform/modules/iam/main.tf")
    assert 'resource "google_project_iam_member"' in txt


# ===========================================================================
# 8. TERRAFORM MODULE — SECRET MANAGER
# ===========================================================================

def test_secret_manager_db_password_secret():
    txt = _read("terraform/modules/secret_manager/main.tf")
    assert 'resource "google_secret_manager_secret" "db_password"' in txt

def test_secret_manager_api_key_secret():
    txt = _read("terraform/modules/secret_manager/main.tf")
    assert 'resource "google_secret_manager_secret" "api_key"' in txt

def test_secret_manager_db_password_version():
    txt = _read("terraform/modules/secret_manager/main.tf")
    assert 'resource "google_secret_manager_secret_version" "db_password_version"' in txt

def test_secret_manager_iam_accessor():
    txt = _read("terraform/modules/secret_manager/main.tf")
    assert "roles/secretmanager.secretAccessor" in txt

def test_secret_manager_replication_user_managed():
    txt = _read("terraform/modules/secret_manager/main.tf")
    assert "user_managed" in txt


# ===========================================================================
# 9. GITHUB ACTIONS CI/CD PIPELINE
# ===========================================================================

def test_ci_yml_parses_as_yaml():
    data = _yaml(".github/workflows/ci.yml")
    assert data is not None

def test_ci_yml_has_on_trigger():
    data = _yaml(".github/workflows/ci.yml")
    trigger = data.get("on", data.get(True, {}))
    assert trigger is not None

def test_ci_yml_triggers_on_push_main():
    data = _yaml(".github/workflows/ci.yml")
    trigger = data.get("on", data.get(True, {}))
    branches = trigger.get("push", {}).get("branches", [])
    assert "main" in branches

def test_ci_yml_triggers_on_pull_request():
    data = _yaml(".github/workflows/ci.yml")
    trigger = data.get("on", data.get(True, {}))
    assert "pull_request" in trigger

def test_ci_yml_has_security_scan_job():
    data = _yaml(".github/workflows/ci.yml")
    assert "security-scan" in data["jobs"]

def test_ci_yml_has_build_and_scan_job():
    data = _yaml(".github/workflows/ci.yml")
    assert "build-and-scan" in data["jobs"]

def test_ci_yml_has_push_to_artifact_registry_job():
    data = _yaml(".github/workflows/ci.yml")
    assert "push-to-artifact-registry" in data["jobs"]

def test_ci_yml_uses_checkov():
    txt = _read(".github/workflows/ci.yml")
    assert "checkov" in txt.lower()

def test_ci_yml_uses_trivy():
    txt = _read(".github/workflows/ci.yml")
    assert "trivy" in txt.lower()

def test_ci_yml_artifact_registry_region():
    txt = _read(".github/workflows/ci.yml")
    assert "europe-west2" in txt

def test_ci_yml_workload_identity_federation():
    txt = _read(".github/workflows/ci.yml")
    assert "workload_identity_provider" in txt

def test_ci_yml_push_job_runs_on_main_only():
    txt = _read(".github/workflows/ci.yml")
    assert "refs/heads/main" in txt

def test_ci_yml_docker_buildx_action():
    txt = _read(".github/workflows/ci.yml")
    assert "docker/setup-buildx-action" in txt

def test_ci_yml_build_push_action():
    txt = _read(".github/workflows/ci.yml")
    assert "docker/build-push-action" in txt

def test_ci_yml_env_project_id_secret():
    txt = _read(".github/workflows/ci.yml")
    assert "GCP_PROJECT_ID" in txt


# ===========================================================================
# 10. CLOUD BUILD PIPELINE
# ===========================================================================

def test_cloudbuild_yaml_parses():
    data = _yaml("cloud-build/cloudbuild.yaml")
    assert data is not None

def test_cloudbuild_has_steps():
    data = _yaml("cloud-build/cloudbuild.yaml")
    assert "steps" in data
    assert len(data["steps"]) >= 6

def test_cloudbuild_checkov_terraform_step():
    data = _yaml("cloud-build/cloudbuild.yaml")
    ids = [s.get("id", "") for s in data["steps"]]
    assert "checkov-terraform" in ids

def test_cloudbuild_checkov_k8s_step():
    data = _yaml("cloud-build/cloudbuild.yaml")
    ids = [s.get("id", "") for s in data["steps"]]
    assert "checkov-k8s" in ids

def test_cloudbuild_build_step():
    data = _yaml("cloud-build/cloudbuild.yaml")
    ids = [s.get("id", "") for s in data["steps"]]
    assert "build" in ids

def test_cloudbuild_trivy_scan_step():
    data = _yaml("cloud-build/cloudbuild.yaml")
    ids = [s.get("id", "") for s in data["steps"]]
    assert "trivy-scan" in ids

def test_cloudbuild_push_sha_step():
    data = _yaml("cloud-build/cloudbuild.yaml")
    ids = [s.get("id", "") for s in data["steps"]]
    assert "push-sha" in ids

def test_cloudbuild_argocd_sync_step():
    data = _yaml("cloud-build/cloudbuild.yaml")
    ids = [s.get("id", "") for s in data["steps"]]
    assert "argocd-sync" in ids

def test_cloudbuild_substitutions_region():
    data = _yaml("cloud-build/cloudbuild.yaml")
    assert data["substitutions"]["_REGION"] == "europe-west2"

def test_cloudbuild_substitutions_repo():
    data = _yaml("cloud-build/cloudbuild.yaml")
    assert "randstad-repo" in data["substitutions"]["_REPO"]

def test_cloudbuild_timeout_set():
    data = _yaml("cloud-build/cloudbuild.yaml")
    assert "timeout" in data

def test_cloudbuild_machine_type_highcpu():
    data = _yaml("cloud-build/cloudbuild.yaml")
    assert "E2_HIGHCPU_8" in data["options"]["machineType"]

def test_cloudbuild_secret_manager_argocd_token():
    txt = _read("cloud-build/cloudbuild.yaml")
    assert "argocd-token" in txt

def test_cloudbuild_images_list():
    data = _yaml("cloud-build/cloudbuild.yaml")
    assert "images" in data
    assert len(data["images"]) >= 2

def test_cloudbuild_parallel_checkov_steps():
    data = _yaml("cloud-build/cloudbuild.yaml")
    # Both checkov steps should have waitFor: ["-"] meaning parallel
    checkov_steps = [s for s in data["steps"] if "checkov" in s.get("id", "")]
    for step in checkov_steps:
        assert step.get("waitFor") == ["-"]


# ===========================================================================
# 11. KUBERNETES MANIFESTS
# ===========================================================================

def test_k8s_deployment_api_version():
    data = _yaml("k8s/deployment.yaml")
    assert data["apiVersion"] == "apps/v1"

def test_k8s_deployment_kind():
    data = _yaml("k8s/deployment.yaml")
    assert data["kind"] == "Deployment"

def test_k8s_deployment_replicas_3():
    data = _yaml("k8s/deployment.yaml")
    assert data["spec"]["replicas"] == 3

def test_k8s_deployment_non_root_user():
    data = _yaml("k8s/deployment.yaml")
    sc = data["spec"]["template"]["spec"]["securityContext"]
    assert sc["runAsNonRoot"] is True
    assert sc["runAsUser"] == 1000

def test_k8s_deployment_run_as_user_1000():
    data = _yaml("k8s/deployment.yaml")
    sc = data["spec"]["template"]["spec"]["securityContext"]
    assert sc["runAsUser"] == 1000

def test_k8s_deployment_liveness_probe_health():
    data = _yaml("k8s/deployment.yaml")
    container = data["spec"]["template"]["spec"]["containers"][0]
    assert container["livenessProbe"]["httpGet"]["path"] == "/health"

def test_k8s_deployment_readiness_probe_ready():
    data = _yaml("k8s/deployment.yaml")
    container = data["spec"]["template"]["spec"]["containers"][0]
    assert container["readinessProbe"]["httpGet"]["path"] == "/ready"

def test_k8s_deployment_no_privilege_escalation():
    data = _yaml("k8s/deployment.yaml")
    container = data["spec"]["template"]["spec"]["containers"][0]
    assert container["securityContext"]["allowPrivilegeEscalation"] is False

def test_k8s_deployment_readonly_root_filesystem():
    data = _yaml("k8s/deployment.yaml")
    container = data["spec"]["template"]["spec"]["containers"][0]
    assert container["securityContext"]["readOnlyRootFilesystem"] is True

def test_k8s_deployment_drop_all_capabilities():
    data = _yaml("k8s/deployment.yaml")
    container = data["spec"]["template"]["spec"]["containers"][0]
    assert "ALL" in container["securityContext"]["capabilities"]["drop"]

def test_k8s_deployment_resource_limits():
    data = _yaml("k8s/deployment.yaml")
    container = data["spec"]["template"]["spec"]["containers"][0]
    assert "limits" in container["resources"]
    assert "requests" in container["resources"]

def test_k8s_deployment_prometheus_annotations():
    data = _yaml("k8s/deployment.yaml")
    annotations = data["spec"]["template"]["metadata"]["annotations"]
    assert annotations.get("prometheus.io/scrape") == "true"

def test_k8s_deployment_rolling_update_strategy():
    data = _yaml("k8s/deployment.yaml")
    assert data["spec"]["strategy"]["type"] == "RollingUpdate"

def test_k8s_deployment_pod_anti_affinity():
    data = _yaml("k8s/deployment.yaml")
    spec = data["spec"]["template"]["spec"]
    assert "affinity" in spec
    assert "podAntiAffinity" in spec["affinity"]

def test_k8s_service_cluster_ip_type():
    data = _yaml("k8s/service.yaml")
    assert data["spec"]["type"] == "ClusterIP"

def test_k8s_service_port_80():
    data = _yaml("k8s/service.yaml")
    ports = data["spec"]["ports"]
    assert any(p["port"] == 80 for p in ports)

def test_k8s_service_target_port_8080():
    data = _yaml("k8s/service.yaml")
    ports = data["spec"]["ports"]
    assert any(p["targetPort"] == 8080 for p in ports)

def test_k8s_ingress_gce_class():
    data = _yaml("k8s/ingress.yaml")
    annotations = data["metadata"]["annotations"]
    assert annotations.get("kubernetes.io/ingress.class") == "gce"

def test_k8s_ingress_https_only():
    data = _yaml("k8s/ingress.yaml")
    annotations = data["metadata"]["annotations"]
    assert annotations.get("kubernetes.io/ingress.allow-http") == "false"

def test_k8s_ingress_managed_cert_annotation():
    data = _yaml("k8s/ingress.yaml")
    annotations = data["metadata"]["annotations"]
    assert "networking.gke.io/managed-certificates" in annotations

def test_k8s_network_policy_deny_all_present():
    docs = _yaml_all("k8s/network_policy.yaml")
    names = [d["metadata"]["name"] for d in docs if d]
    assert "default-deny-all" in names

def test_k8s_network_policy_app_policy_present():
    docs = _yaml_all("k8s/network_policy.yaml")
    names = [d["metadata"]["name"] for d in docs if d]
    assert any("randstad-gcp-app" in n for n in names)

def test_k8s_network_policy_ingress_egress_types():
    docs = _yaml_all("k8s/network_policy.yaml")
    app_policy = next((d for d in docs if d and "randstad-gcp-app-netpol" in d["metadata"]["name"]), None)
    assert app_policy is not None
    assert "Ingress" in app_policy["spec"]["policyTypes"]
    assert "Egress" in app_policy["spec"]["policyTypes"]


# ===========================================================================
# 12. HELM CHART
# ===========================================================================

def test_helm_chart_api_version():
    data = _yaml("helm/app-chart/Chart.yaml")
    assert data["apiVersion"] == "v2"

def test_helm_chart_name():
    data = _yaml("helm/app-chart/Chart.yaml")
    assert data["name"] == "app-chart"

def test_helm_chart_app_version():
    data = _yaml("helm/app-chart/Chart.yaml")
    assert "appVersion" in data

def test_helm_chart_maintainer_saikiran():
    data = _yaml("helm/app-chart/Chart.yaml")
    maintainers = data.get("maintainers", [])
    assert any("Sai Kiran" in m.get("name", "") for m in maintainers)

def test_helm_values_replica_count():
    data = _yaml("helm/app-chart/values.yaml")
    assert data["replicaCount"] == 3

def test_helm_values_image_pull_policy_always():
    data = _yaml("helm/app-chart/values.yaml")
    assert data["image"]["pullPolicy"] == "Always"

def test_helm_values_service_type_clusterip():
    data = _yaml("helm/app-chart/values.yaml")
    assert data["service"]["type"] == "ClusterIP"

def test_helm_values_autoscaling_enabled():
    data = _yaml("helm/app-chart/values.yaml")
    assert data["autoscaling"]["enabled"] is True

def test_helm_values_autoscaling_max_replicas():
    data = _yaml("helm/app-chart/values.yaml")
    assert data["autoscaling"]["maxReplicas"] >= 5

def test_helm_values_run_as_non_root():
    data = _yaml("helm/app-chart/values.yaml")
    assert data["podSecurityContext"]["runAsNonRoot"] is True

def test_helm_values_read_only_root_filesystem():
    data = _yaml("helm/app-chart/values.yaml")
    assert data["securityContext"]["readOnlyRootFilesystem"] is True

def test_helm_values_prometheus_annotations():
    data = _yaml("helm/app-chart/values.yaml")
    annotations = data.get("podAnnotations", {})
    assert annotations.get("prometheus.io/scrape") == "true"

def test_helm_values_ingress_enabled():
    data = _yaml("helm/app-chart/values.yaml")
    assert data["ingress"]["enabled"] is True

def test_helm_deployment_template_contains_helm_syntax():
    txt = _read("helm/app-chart/templates/deployment.yaml")
    assert "{{" in txt


# ===========================================================================
# 13. ARGOCD APPLICATION
# ===========================================================================

def test_argocd_api_version():
    data = _yaml("argocd/application.yaml")
    assert "argoproj.io" in data["apiVersion"]

def test_argocd_kind_application():
    data = _yaml("argocd/application.yaml")
    assert data["kind"] == "Application"

def test_argocd_app_name():
    data = _yaml("argocd/application.yaml")
    assert data["metadata"]["name"] == "randstad-gcp-app"

def test_argocd_repo_url():
    data = _yaml("argocd/application.yaml")
    assert "saikirangvariganti" in data["spec"]["source"]["repoURL"]

def test_argocd_helm_path():
    data = _yaml("argocd/application.yaml")
    assert data["spec"]["source"]["path"] == "helm/app-chart"

def test_argocd_auto_sync_enabled():
    data = _yaml("argocd/application.yaml")
    assert data["spec"]["syncPolicy"]["automated"]["prune"] is True

def test_argocd_self_heal_enabled():
    data = _yaml("argocd/application.yaml")
    assert data["spec"]["syncPolicy"]["automated"]["selfHeal"] is True

def test_argocd_retry_configured():
    data = _yaml("argocd/application.yaml")
    assert data["spec"]["syncPolicy"]["retry"]["limit"] >= 3

def test_argocd_destination_namespace_default():
    data = _yaml("argocd/application.yaml")
    assert data["spec"]["destination"]["namespace"] == "default"

def test_argocd_revision_history_limit():
    data = _yaml("argocd/application.yaml")
    assert data["spec"]["revisionHistoryLimit"] >= 5


# ===========================================================================
# 14. SECURITY — CLOUD ARMOR
# ===========================================================================

def test_cloud_armor_waf_policy_resource():
    txt = _read("security/cloud_armor.tf")
    assert 'resource "google_compute_security_policy"' in txt

def test_cloud_armor_sqli_protection():
    txt = _read("security/cloud_armor.tf")
    assert "sqli-stable" in txt

def test_cloud_armor_xss_protection():
    txt = _read("security/cloud_armor.tf")
    assert "xss-stable" in txt

def test_cloud_armor_lfi_protection():
    txt = _read("security/cloud_armor.tf")
    assert "lfi-stable" in txt

def test_cloud_armor_rfi_protection():
    txt = _read("security/cloud_armor.tf")
    assert "rfi-stable" in txt

def test_cloud_armor_rate_limiting():
    txt = _read("security/cloud_armor.tf")
    assert "rate_limit_options" in txt

def test_cloud_armor_ddos_protection():
    txt = _read("security/cloud_armor.tf")
    assert "layer_7_ddos_defense_config" in txt

def test_cloud_armor_backend_service():
    txt = _read("security/cloud_armor.tf")
    assert 'resource "google_compute_backend_service"' in txt

def test_cloud_armor_health_check():
    txt = _read("security/cloud_armor.tf")
    assert 'resource "google_compute_health_check"' in txt

def test_cloud_armor_health_check_path():
    txt = _read("security/cloud_armor.tf")
    assert '"/health"' in txt

def test_cloud_armor_rate_limit_1000():
    txt = _read("security/cloud_armor.tf")
    assert "count        = 1000" in txt


# ===========================================================================
# 15. SECURITY — VPC SERVICE CONTROLS
# ===========================================================================

def test_vpc_sc_access_policy_resource():
    txt = _read("security/vpc_service_controls.tf")
    assert 'resource "google_access_context_manager_access_policy"' in txt

def test_vpc_sc_service_perimeter_resource():
    txt = _read("security/vpc_service_controls.tf")
    assert 'resource "google_access_context_manager_service_perimeter"' in txt

def test_vpc_sc_access_level_onprem():
    txt = _read("security/vpc_service_controls.tf")
    assert "onprem_access" in txt

def test_vpc_sc_restricted_services_storage():
    txt = _read("security/vpc_service_controls.tf")
    assert "storage.googleapis.com" in txt

def test_vpc_sc_restricted_services_cloudsql():
    txt = _read("security/vpc_service_controls.tf")
    assert "cloudsql.googleapis.com" in txt

def test_vpc_sc_restricted_services_secretmanager():
    txt = _read("security/vpc_service_controls.tf")
    assert "secretmanager.googleapis.com" in txt

def test_vpc_sc_restricted_services_gke():
    txt = _read("security/vpc_service_controls.tf")
    assert "container.googleapis.com" in txt

def test_vpc_sc_ingress_egress_policies():
    txt = _read("security/vpc_service_controls.tf")
    assert "ingress_policies" in txt
    assert "egress_policies" in txt

def test_vpc_sc_dry_run_spec():
    txt = _read("security/vpc_service_controls.tf")
    assert "use_explicit_dry_run_spec = true" in txt


# ===========================================================================
# 16. MONITORING
# ===========================================================================

def test_prometheus_yml_parses():
    data = _yaml("monitoring/prometheus.yml")
    assert data is not None

def test_prometheus_scrape_interval():
    data = _yaml("monitoring/prometheus.yml")
    assert data["global"]["scrape_interval"] == "15s"

def test_prometheus_external_labels_cluster():
    data = _yaml("monitoring/prometheus.yml")
    labels = data["global"]["external_labels"]
    assert "randstad-gcp-cluster" in labels.get("cluster", "")

def test_prometheus_scrape_configs_not_empty():
    data = _yaml("monitoring/prometheus.yml")
    assert len(data["scrape_configs"]) >= 4

def test_prometheus_kubernetes_pods_job():
    data = _yaml("monitoring/prometheus.yml")
    job_names = [j["job_name"] for j in data["scrape_configs"]]
    assert "kubernetes-pods" in job_names

def test_prometheus_randstad_app_job():
    data = _yaml("monitoring/prometheus.yml")
    job_names = [j["job_name"] for j in data["scrape_configs"]]
    assert "randstad-gcp-app" in job_names

def test_prometheus_alerting_config():
    data = _yaml("monitoring/prometheus.yml")
    assert "alerting" in data

def test_prometheus_alertmanager_target():
    data = _yaml("monitoring/prometheus.yml")
    targets = data["alerting"]["alertmanagers"][0]["static_configs"][0]["targets"]
    assert any("9093" in t for t in targets)

def test_grafana_dashboard_json_is_valid():
    txt = _read("monitoring/grafana_dashboard.json")
    data = json.loads(txt)
    assert data is not None

def test_grafana_dashboard_has_panels():
    txt = _read("monitoring/grafana_dashboard.json")
    data = json.loads(txt)
    assert "panels" in data or "rows" in data or len(data) > 0


# ===========================================================================
# 17. MIGRATION ARTEFACTS
# ===========================================================================

def test_assessment_runbook_has_phases():
    txt = _read("migration/assessment_runbook.md")
    assert "Phase 1" in txt
    assert "Phase 2" in txt

def test_assessment_runbook_mentions_migrate_for_compute():
    txt = _read("migration/assessment_runbook.md")
    assert "Migrate for Compute Engine" in txt

def test_assessment_runbook_has_rollback():
    txt = _read("migration/assessment_runbook.md")
    assert "Rollback" in txt

def test_assessment_runbook_mentions_europe_west2():
    txt = _read("migration/assessment_runbook.md")
    assert "europe-west2" in txt

def test_wave_plan_has_four_waves():
    txt = _read("migration/wave_plan.md")
    assert "Wave 1" in txt
    assert "Wave 2" in txt
    assert "Wave 3" in txt
    assert "Wave 4" in txt

def test_wave_plan_wave_3_database_high_risk():
    txt = _read("migration/wave_plan.md")
    assert "High" in txt and "Database" in txt

def test_wave_plan_mentions_argocd():
    txt = _read("migration/wave_plan.md")
    assert "ArgoCD" in txt or "argocd" in txt

def test_wave_plan_has_rollback_plans():
    txt = _read("migration/wave_plan.md")
    assert "Rollback" in txt

def test_landing_zone_ha_vpn_resource():
    txt = _read("migration/terraform_landing_zone.tf")
    assert 'resource "google_compute_ha_vpn_gateway"' in txt

def test_landing_zone_vpn_tunnel_1():
    txt = _read("migration/terraform_landing_zone.tf")
    assert 'resource "google_compute_vpn_tunnel" "tunnel_1"' in txt

def test_landing_zone_vpn_tunnel_2():
    txt = _read("migration/terraform_landing_zone.tf")
    assert 'resource "google_compute_vpn_tunnel" "tunnel_2"' in txt

def test_landing_zone_bgp_router():
    txt = _read("migration/terraform_landing_zone.tf")
    assert 'resource "google_compute_router"' in txt

def test_landing_zone_bgp_peer():
    txt = _read("migration/terraform_landing_zone.tf")
    assert 'resource "google_compute_router_peer"' in txt

def test_landing_zone_migration_staging_bucket():
    txt = _read("migration/terraform_landing_zone.tf")
    assert 'resource "google_storage_bucket" "migration_staging"' in txt

def test_landing_zone_firewall_migration_traffic():
    txt = _read("migration/terraform_landing_zone.tf")
    assert "allow-migration-traffic" in txt


# ===========================================================================
# 18. APPLICATION CODE
# ===========================================================================

def test_app_imports_flask():
    txt = _read("app/main.py")
    assert "from flask import" in txt

def test_app_imports_prometheus_client():
    txt = _read("app/main.py")
    assert "from prometheus_client import" in txt

def test_app_health_endpoint():
    txt = _read("app/main.py")
    assert "'/health'" in txt or '"/health"' in txt

def test_app_ready_endpoint():
    txt = _read("app/main.py")
    assert "'/ready'" in txt or '"/ready"' in txt

def test_app_metrics_endpoint():
    txt = _read("app/main.py")
    assert "'/metrics'" in txt or '"/metrics"' in txt

def test_app_api_v1_items_endpoint():
    txt = _read("app/main.py")
    assert "/api/v1/items" in txt

def test_app_request_count_counter():
    txt = _read("app/main.py")
    assert "REQUEST_COUNT" in txt

def test_app_request_latency_histogram():
    txt = _read("app/main.py")
    assert "REQUEST_LATENCY" in txt

def test_app_listens_on_8080():
    txt = _read("app/main.py")
    assert "8080" in txt

def test_app_uses_gunicorn_in_dockerfile():
    txt = _read("app/Dockerfile")
    assert "gunicorn" in txt

def test_dockerfile_multi_stage_builder():
    txt = _read("app/Dockerfile")
    assert "AS builder" in txt

def test_dockerfile_non_root_user():
    txt = _read("app/Dockerfile")
    assert "appuser" in txt

def test_dockerfile_expose_8080():
    txt = _read("app/Dockerfile")
    assert "EXPOSE 8080" in txt

def test_dockerfile_healthcheck():
    txt = _read("app/Dockerfile")
    assert "HEALTHCHECK" in txt

def test_dockerfile_python_311():
    txt = _read("app/Dockerfile")
    assert "python:3.11" in txt

def test_dockerfile_no_cache_pip():
    txt = _read("app/Dockerfile")
    assert "--no-cache-dir" in txt

def test_requirements_flask():
    txt = _read("app/requirements.txt")
    assert "flask" in txt.lower()

def test_requirements_prometheus_client():
    txt = _read("app/requirements.txt")
    assert "prometheus-client" in txt.lower()

def test_requirements_gunicorn():
    txt = _read("app/requirements.txt")
    assert "gunicorn" in txt.lower()


# ===========================================================================
# 19. README COMPLETENESS
# ===========================================================================

def test_readme_has_overview():
    txt = _read("README.md")
    assert "Overview" in txt

def test_readme_has_architecture():
    txt = _read("README.md")
    assert "Architecture" in txt

def test_readme_mentions_gke():
    txt = _read("README.md")
    assert "GKE" in txt

def test_readme_mentions_terraform():
    txt = _read("README.md")
    assert "Terraform" in txt

def test_readme_mentions_argocd():
    txt = _read("README.md")
    assert "ArgoCD" in txt

def test_readme_mentions_cloud_armor():
    txt = _read("README.md")
    assert "Cloud Armor" in txt

def test_readme_mentions_vpc_service_controls():
    txt = _read("README.md")
    assert "VPC Service Controls" in txt

def test_readme_mentions_prometheus():
    txt = _read("README.md")
    assert "Prometheus" in txt

def test_readme_mentions_migration():
    txt = _read("README.md")
    assert "migration" in txt.lower() or "Migration" in txt

def test_readme_deploy_instructions():
    txt = _read("README.md")
    assert "terraform init" in txt or "terraform apply" in txt

def test_readme_running_tests_section():
    txt = _read("README.md")
    assert "pytest" in txt

def test_readme_github_link_saikiran():
    txt = _read("README.md")
    assert "saikirangvariganti" in txt

def test_readme_author_saikiran():
    txt = _read("README.md")
    assert "Sai Kiran" in txt
