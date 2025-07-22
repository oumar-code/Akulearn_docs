output "gke_endpoint" {
  value = google_container_cluster.backend.endpoint
}

output "db_connection_name" {
  value = google_sql_database_instance.main.connection_name
}

output "db_password" {
  value     = random_password.db_password.result
  sensitive = true
}

output "frontend_bucket_url" {
  value = google_storage_bucket.frontend.url
}
