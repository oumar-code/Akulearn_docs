resource "google_container_cluster" "backend" {
  name     = "akulearn-backend-cluster"
  location = var.region
  network  = google_compute_network.vpc.id
  subnetwork = google_compute_subnetwork.backend.id

  remove_default_node_pool = true
  initial_node_count      = 1

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  node_config {
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    service_account = google_service_account.gke_nodes.email
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 5
  }
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  cluster    = google_container_cluster.backend.name
  location   = var.region
  node_count = 1

  node_config {
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    service_account = google_service_account.gke_nodes.email
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 5
  }
}

resource "google_service_account" "gke_nodes" {
  account_id   = "gke-nodes"
  display_name = "GKE Node Service Account"
}
