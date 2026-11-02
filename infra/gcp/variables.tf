variable "project_id" {
  type        = string
  description = "Existing GCP project; this configuration does not create or upgrade a billing account."
}
variable "region" {
  type    = string
  default = "us-central1"
}
variable "zone" {
  type    = string
  default = "us-central1-a"
}
variable "app_image" {
  type        = string
  description = "Publicly pullable, tested application image pinned by sha256 digest; build it in CI, not on the small VM."
  validation {
    condition     = can(regex("^[a-zA-Z0-9][a-zA-Z0-9./:_-]*@sha256:[a-f0-9]{64}$", var.app_image))
    error_message = "Use an immutable OCI image digest, e.g. ghcr.io/owner/splitwise-pro@sha256:<64 lowercase hex characters>."
  }
}
variable "operator_members" {
  type        = list(string)
  description = "Explicit IAM user/group principals allowed IAP + OS Login admin access. Do not use allUsers."
  validation {
    condition     = length(var.operator_members) > 0 && alltrue([for member in var.operator_members : can(regex("^(user|group):[^[:space:]]+@[^[:space:]]+$", member))])
    error_message = "Provide at least one explicit user:email or group:email operator."
  }
}
variable "authorize_billable_resources" {
  type        = bool
  default     = false
  description = "Owner-controlled gate. Never set true without explicit approval for potential VM, IPv4, disk and network charges."
}
variable "billing_account_id" {
  type        = string
  default     = null
  description = "Optional existing billing account ID for project-scoped email budget alerts; requires billing-budget permissions. No billing account is created or upgraded."
}
variable "monthly_budget_usd" {
  type    = number
  default = 5
  validation {
    condition     = var.monthly_budget_usd >= 1 && floor(var.monthly_budget_usd) == var.monthly_budget_usd
    error_message = "Budget must be an integer of at least 1 USD. It is an alert, not a hard cap."
  }
}
