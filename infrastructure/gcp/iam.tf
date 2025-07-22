resource "google_project_iam_custom_role" "backend_dev" {
  role_id     = "backendDeveloper"
  title       = "Akulearn Backend Developer"
  description = "Least-privilege backend developer role"
  permissions = [
    "container.clusters.get",
    "container.clusters.list",
    "container.deployments.get",
    "container.deployments.list",
    "container.pods.get",
    "container.pods.list",
    "container.services.get",
    "container.services.list",
    "sql.instances.get",
    "sql.instances.list",
    "sql.databases.get",
    "sql.databases.list"
  ]
}

resource "google_project_iam_custom_role" "sre" {
  role_id     = "siteReliabilityEngineer"
  title       = "Akulearn Site Reliability Engineer"
  description = "SRE role for monitoring and ops"
  permissions = [
    "monitoring.dashboards.get",
    "monitoring.dashboards.list",
    "logging.sinks.get",
    "logging.sinks.list",
    "resourcemanager.projects.get"
  ]
}

resource "google_service_account" "backend_dev" {
  account_id   = "backend-dev"
  display_name = "Backend Developer Service Account"
}

resource "google_service_account" "sre" {
  account_id   = "sre"
  display_name = "Site Reliability Engineer Service Account"
}

resource "google_project_iam_member" "backend_dev_role" {
  role   = google_project_iam_custom_role.backend_dev.name
  member = "serviceAccount:${google_service_account.backend_dev.email}"
}

resource "google_project_iam_member" "sre_role" {
  role   = google_project_iam_custom_role.sre.name
  member = "serviceAccount:${google_service_account.sre.email}"
}
