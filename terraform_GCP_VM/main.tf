provider "google" {
  credentials = file("Bot2Engg_keys_GCP.json")
  project     = file("project.txt")
  region      = "us-west1"
}

resource "google_compute_network" "vpc_network" {
  name                    = "bot-vpc"
  auto_create_subnetworks = "false"
}

resource "google_compute_subnetwork" "subnetwork" {
  name          = "bot-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = "us-west1"
  network       = google_compute_network.vpc_network.self_link
}

resource "google_compute_firewall" "default-allow-https" {
  name    = "default-allow-https"
  network = google_compute_network.vpc_network.self_link

  allow {
    protocol = "tcp"
    ports    = []
  }

  direction = "EGRESS"
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "default-allow-ssh" {
  name    = "allow-ssh"
  network = google_compute_network.vpc_network.self_link

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  direction = "INGRESS"
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow-icmp" {
  name    = "allow-icmp"
  network = google_compute_network.vpc_network.self_link

  allow {
    protocol = "icmp"
  }

  direction = "EGRESS"
  source_ranges = ["173.194.203.102"]
}

resource "google_compute_instance" "bot_vm" {
  name         = "discord-bot-vm"
  machine_type = "e2-micro"  // This is a small machine type
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network.self_link
    subnetwork = google_compute_subnetwork.subnetwork.name
  }

  metadata = {
    ssh-keys = "user:${file("~/.ssh/id_rsa.pub")}"
  }
}

resource "google_compute_router" "nat-router" {
  name    = "nat-router"
  network = google_compute_network.vpc_network.name
  region  = "us-west1"
}

resource "google_compute_router_nat" "nat-config" {
  name   = "nat-config"
  router = google_compute_router.nat-router.name
  region = google_compute_router.nat-router.region

  nat_ip_allocate_option = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}
