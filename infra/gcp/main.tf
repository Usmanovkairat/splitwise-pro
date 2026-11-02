terraform {
  required_version = ">= 1.5, < 2.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Fail during planning until the account owner explicitly accepts possible charges.
resource "terraform_data" "authorization" {
  lifecycle {
    precondition {
      condition     = var.authorize_billable_resources
      error_message = "Cloud provisioning is disabled. Review costs and obtain explicit owner authorization before setting authorize_billable_resources=true."
    }
  }
}

resource "google_project_service" "required" {
  for_each           = toset(["compute.googleapis.com", "iap.googleapis.com", "oslogin.googleapis.com", "iam.googleapis.com", "cloudresourcemanager.googleapis.com"])
  service            = each.value
  disable_on_destroy = false
  depends_on         = [terraform_data.authorization]
}

resource "google_compute_network" "app" {
  name                    = "splitwise"
  auto_create_subnetworks = false
  depends_on              = [google_project_service.required]
}

resource "google_compute_subnetwork" "app" {
  name          = "splitwise"
  ip_cidr_range = "10.81.0.0/24"
  network       = google_compute_network.app.id
}

resource "google_compute_firewall" "iap_ssh" {
  name          = "splitwise-iap-ssh"
  network       = google_compute_network.app.name
  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["splitwise-iap"]
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}

resource "google_service_account" "vm" {
  account_id   = "splitwise-vm"
  display_name = "SplitWise VM with no project data privileges"
  depends_on   = [google_project_service.required]
}

resource "google_project_iam_member" "iap" {
  for_each = toset(var.operator_members)
  project  = var.project_id
  role     = "roles/iap.tunnelResourceAccessor"
  member   = each.value
}

resource "google_project_iam_member" "os_admin" {
  for_each = toset(var.operator_members)
  project  = var.project_id
  role     = "roles/compute.osAdminLogin"
  member   = each.value
}

resource "google_service_account_iam_member" "ssh" {
  for_each           = toset(var.operator_members)
  service_account_id = google_service_account.vm.name
  role               = "roles/iam.serviceAccountUser"
  member             = each.value
}

resource "google_compute_disk" "data" {
  name = "splitwise-data"
  type = "pd-standard"
  size = 10
  # Retain financial data until a separate, reviewed teardown decision.
  lifecycle {
    prevent_destroy = true
  }
  depends_on = [google_project_service.required]
}

resource "google_compute_instance" "app" {
  name         = "splitwise"
  machine_type = "e2-micro"
  tags         = ["splitwise-iap"]
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      type  = "pd-standard"
      size  = 10
    }
  }
  attached_disk {
    source      = google_compute_disk.data.id
    device_name = "splitwise-data"
  }
  network_interface {
    subnetwork = google_compute_subnetwork.app.id
    # Egress to apt/registry. No ingress rule exposes this IP's app or database.
    # External IPv4 may incur charges even on an otherwise eligible Free Tier VM.
    access_config {}
  }
  service_account {
    email  = google_service_account.vm.email
    scopes = []
  }
  metadata = {
    enable-oslogin           = "TRUE"
    block-project-ssh-keys   = "TRUE"
    disable-legacy-endpoints = "TRUE"
  }
  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }
  metadata_startup_script = templatefile("${path.module}/startup.sh.tftpl", {
    app_image = var.app_image
  })
  depends_on = [google_project_service.required]
}

# Budget notifications are alerts, not an enforced spending cap.
resource "google_billing_budget" "monthly" {
  count           = var.billing_account_id == null ? 0 : 1
  billing_account = var.billing_account_id
  display_name    = "SplitWise monthly project alert"
  budget_filter {
    projects = ["projects/${data.google_project.current.number}"]
  }
  amount {
    specified_amount {
      currency_code = "USD"
      units         = tostring(var.monthly_budget_usd)
    }
  }
  threshold_rules {
    threshold_percent = 0.5
  }
  threshold_rules {
    threshold_percent = 0.9
  }
  threshold_rules {
    threshold_percent = 1.0
  }
  # Omit all_updates_rule: default IAM email recipients receive threshold alerts.
  # Google provider 6.50 requires a real channel/topic if that optional block is set.
  depends_on = [terraform_data.authorization]
}

data "google_project" "current" {
  project_id = var.project_id
}
