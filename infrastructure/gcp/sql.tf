resource "random_password" "db_password" {
  length  = 16
  special = true
}

resource "google_sql_database_instance" "main" {
  name             = "akulearn-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-custom-1-3840"
    availability_type = "REGIONAL"
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
    backup_configuration {
      enabled = true
    }
  }
}

resource "google_sql_database" "prod" {
  name     = "akulearn_prod"
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "app" {
  name     = "akulearn_app"
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}
