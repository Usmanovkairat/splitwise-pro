output "tunnel_command" {
  value = "gcloud compute ssh splitwise --project=${var.project_id} --zone=${var.zone} --tunnel-through-iap -- -N -L 8000:127.0.0.1:8000"
}
output "application_url" {
  value       = "http://127.0.0.1:8000 (only while the authorized SSH/IAP tunnel is open)"
  description = "No public application endpoint is created."
}
output "data_disk" {
  value = google_compute_disk.data.name
}
