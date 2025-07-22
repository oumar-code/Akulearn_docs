resource "google_storage_bucket" "frontend" {
  name          = "akulearn-frontend-bucket-${var.project_id}"
  location      = var.region
  force_destroy = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_member" "cdn" {
  bucket = google_storage_bucket.frontend.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

resource "google_compute_backend_bucket" "frontend_cdn" {
  name        = "akulearn-frontend-cdn"
  bucket_name = google_storage_bucket.frontend.name
  enable_cdn  = true
}
