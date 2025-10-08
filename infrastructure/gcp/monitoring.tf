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
      {
        title: "GKE Memory Utilization",
        xyChart: {
          dataSets: [{
            timeSeriesQuery: {
              timeSeriesFilter: {
                filter: "metric.type=\"kubernetes.io/container/memory/used_bytes\" resource.type=\"k8s_container\"",
                aggregation: { perSeriesAligner: "ALIGN_MEAN" }
              }
            }
          }],
          timeshiftDuration: "0s"
        }
      },
      {
        title: "Pod Restarts",
        xyChart: {
          dataSets: [{
            timeSeriesQuery: {
              timeSeriesFilter: {
                filter: "metric.type=\"kubernetes.io/container/restart_count\" resource.type=\"k8s_container\"",
                aggregation: { perSeriesAligner: "ALIGN_SUM" }
              }
            }
          }],
          timeshiftDuration: "0s"
        }
      }
    ]
  })
}

# Alerting policies
resource "google_monitoring_alert_policy" "cpu_high" {
  display_name = "GKE CPU High"
  combiner     = "OR"
  conditions {
    display_name = "CPU > 80%"
    condition_threshold {
      filter          = "metric.type=\"kubernetes.io/container/cpu/core_usage_time\" resource.type=\"k8s_container\""
      comparison      = "COMPARISON_GT"
      threshold_value = 0.8
      duration        = "300s"
      aggregations {
        alignment_period     = "60s"
        per_series_aligner  = "ALIGN_MEAN"
      }
    }
  }
  notification_channels = [google_monitoring_notification_channel.email.id]
}

resource "google_monitoring_alert_policy" "sql_conn_high" {
  display_name = "Cloud SQL Connections High"
  combiner     = "OR"
  conditions {
    display_name = "SQL Connections > 100"
    condition_threshold {
      filter          = "metric.type=\"cloudsql.googleapis.com/database/database_connections\" resource.type=\"cloudsql_database\""
      comparison      = "COMPARISON_GT"
      threshold_value = 100
      duration        = "300s"
      aggregations {
        alignment_period     = "60s"
        per_series_aligner  = "ALIGN_MEAN"
      }
    }
  }
  notification_channels = [google_monitoring_notification_channel.email.id]
}

resource "google_monitoring_notification_channel" "email" {
  display_name = "DevOps Email"
  type         = "email"
  labels = {
    email_address = "devops@akulearn.com"
  }
}

resource "google_logging_project_sink" "archive" {
  name        = "akulearn-logs-archive"
  destination = "storage.googleapis.com/${google_storage_bucket.frontend.name}"
  filter      = ""
  unique_writer_identity = true
}
