resource "google_monitoring_dashboard" "main" {
  dashboard_json = jsonencode({
    displayName: "Akulearn Infra Dashboard",
    gridLayout: { columns: 2 },
    widgets: [
      {
        title: "GKE CPU Utilization",
        xyChart: {
          dataSets: [{
            timeSeriesQuery: {
              timeSeriesFilter: {
                filter: "metric.type=\"kubernetes.io/container/cpu/core_usage_time\" resource.type=\"k8s_container\"",
                aggregation: { perSeriesAligner: "ALIGN_MEAN" }
              }
            }
          }],
          timeshiftDuration: "0s"
        }
      },
      {
        title: "Cloud SQL Connections",
        xyChart: {
          dataSets: [{
            timeSeriesQuery: {
              timeSeriesFilter: {
                filter: "metric.type=\"cloudsql.googleapis.com/database/database_connections\" resource.type=\"cloudsql_database\"",
                aggregation: { perSeriesAligner: "ALIGN_MEAN" }
              }
            }
          }],
          timeshiftDuration: "0s"
        }
      }
    ]
  })
}

resource "google_logging_project_sink" "archive" {
  name        = "akulearn-logs-archive"
  destination = "storage.googleapis.com/${google_storage_bucket.frontend.name}"
  filter      = ""
  unique_writer_identity = true
}
