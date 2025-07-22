resource "google_compute_network" "vpc" {
  name                    = "akulearn-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "backend" {
  name          = "backend-subnet"
  ip_cidr_range = "10.10.0.0/20"
  region        = var.region
  network       = google_compute_network.vpc.id
}

resource "google_compute_subnetwork" "frontend" {
  name          = "frontend-subnet"
  ip_cidr_range = "10.20.0.0/20"
  region        = var.region
  network       = google_compute_network.vpc.id
}

resource "google_compute_firewall" "allow-internal" {
  name    = "allow-internal"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }
  source_ranges = ["10.10.0.0/16"]
}

resource "google_compute_firewall" "allow-ssh" {
  name    = "allow-ssh"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  source_ranges = var.ssh_source_ranges
}

resource "google_compute_firewall" "allow-http-https" {
  name    = "allow-http-https"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }
  source_ranges = ["0.0.0.0/0"]
}
