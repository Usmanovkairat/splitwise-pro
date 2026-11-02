# Protected GCP Compose infrastructure

Prepared configuration; no cloud resources have been provisioned by this change. This is a single-VM teaching deployment, not a high-availability service. Keep the application private because the product has no user authentication or workspace authorization.

The VM runs the real app image and PostgreSQL with Docker Compose. A separate 10 GB standard persistent disk retains PostgreSQL and its generated secret across VM replacement. Only SSH from Google's IAP forwarding range is allowed inbound. The app listens on VM localhost; the operator accesses it through an IAM-authorized, encrypted SSH tunnel. No public HTTP URL or public database port is created. The VM has an egress IPv4 address to install Docker and pull images, with a possible IPv4 charge.

## Before provisioning

1. Obtain explicit account-owner authorization for possible VM, IPv4, disks and network charges. Do not upgrade a Free Trial account, enter payment details or assume credits imply zero cost.
2. Choose an existing project and verify Free Trial/Free Tier eligibility and remaining quota in its billing console. Defaults are one `e2-micro` in `us-central1-a` with 20 GB total `pd-standard` disks. Other projects' usage counts toward account limits. External IPv4, outbound network traffic, snapshots and quota overages may cost money. Neither the budget nor the authorization flag enforces a spending cap.
3. Build and test the application image in CI; publish a public, immutable `ghcr.io/...@sha256:...` image. The VM is intentionally too small for a dependable Node build. Do not place private registry credentials into Terraform variables or startup metadata.
4. Install Terraform >=1.5 and Google Cloud CLI. Sign in with `gcloud auth login` and `gcloud auth application-default login`. The operator applying Terraform needs permissions to enable APIs, create VPC/firewall/VM/disk/service-account resources and grant the listed IAM roles. Budget setup also requires billing-budget permissions; leave `billing_account_id` null if unavailable and configure account-console alerts manually before applying.
5. Copy `terraform.tfvars.example` to ignored `terraform.tfvars`. Set project ID, real image digest and explicit IAM operators. The example is deliberately invalid until filled in. Keep `authorize_billable_resources=false` until approval is recorded.

## Local validation and reviewed plan

From this directory:

```sh
terraform init -backend=false
terraform fmt -check
terraform validate
# After account-owner approval only:
terraform plan -out=reviewed.tfplan
# Inspect the complete plan, resource region, IAM bindings and costs first.
terraform apply reviewed.tfplan
```

The default false gate intentionally blocks planning resources. Never commit `.tfstate`, saved plans, local variables, credentials or database dumps. State contains infrastructure metadata and operator identities; use a protected remote state backend before shared production operation. This configuration generates the database password on the VM, so it is absent from Terraform state and metadata.

An optional `google_billing_budget` sends default billing IAM recipients alerts at 50%, 90% and 100% of the configured project budget (5 USD by default). Enable `billingbudgets.googleapis.com` and confirm notification recipients in the account before relying on it. Alerts can lag and do not stop resources. No billing-account creation, paid-account upgrade, managed database, load balancer or NAT gateway is included.

## Access and verify

Run the command printed by `terraform output -raw tunnel_command`; keep it running. Visit `http://127.0.0.1:8000` locally. The browser's HTTP connection terminates at local loopback and travels through encrypted SSH/IAP to the VM; this is not a public HTTPS deployment.

Use the same `gcloud compute ssh ... --tunnel-through-iap` prefix without `-- -N -L ...` for an administrative shell. Then:

```sh
sudo systemctl status splitwise.service
sudo journalctl -u google-startup-scripts.service --no-pager
sudo sh -c 'cd /srv/splitwise/config && docker compose ps'
curl --fail http://127.0.0.1:8000/api/health
```

Create a test group, reload, restart the VM, reconnect the tunnel and verify the same group still exists. Run the repository's real integrated Playwright suite through the tunnel against the configured URL. Do not point destructive test fixtures at a populated workspace. Record actual test output and image digest in the issue before marking deployment complete.

For existing SQLite data, stop writes and use `backend/scripts/migrate_sqlite_to_postgres.py` plus its backup/reconciliation instructions before allowing users to write to PostgreSQL. Never automatically import into a populated database.

## Backup and rollback

Before a release, create a protected logical database backup on the attached disk (never commit it):

```sh
sudo sh -c 'umask 077; cd /srv/splitwise/config; docker compose exec -T db pg_dump -U splitwise -d splitwise --format=custom > /srv/splitwise/pre-release.dump'
```

Copy that backup to separately controlled backup storage; a dump on the same disk does not protect against disk loss. For image rollback run `deployment/deploy-gcp.sh` on the VM with the prior tested digest. The startup script preserves the current Compose image on reboot and replacement; `app_image` controls only the first bootstrap when no Compose file exists. Terraform's `metadata_startup_script` changes can replace the VM; the separately attached data disk remains. Database schema changes may prevent an old image from reading current data; use a fresh database restored from the pre-release backup rather than blindly downgrading the schema. Test restore before relying on backups. This deployment is single-instance and has release downtime.

## Stop and cleanup

Stop the VM in the console or with `gcloud compute instances stop splitwise --project=PROJECT --zone=ZONE` to stop CPU usage. Disk and IPv4-related costs may remain; stopping is not complete cleanup.

For full teardown, first verify an off-VM backup. The data disk has `prevent_destroy=true`: a normal `terraform destroy` is intentionally blocked. With explicit data-deletion authorization, remove that one lifecycle guard in your local copy, review `terraform plan -destroy` to verify every resource and IAM grant, and run `terraform destroy`. This deletes the database and secret permanently. Confirm no VM, boot/data disks, reserved IPs, snapshots or registry images remain in the project. Required APIs are left enabled (`disable_on_destroy=false`) to avoid breaking unrelated workloads. Remove any manually enabled billing alerts only if no longer needed.

## Validation status

See `deployment/CLOUD.md` for actual local validation evidence and provider compatibility sources. No account-dependent `terraform plan`, cloud apply, tunnel, health check or cloud persistence test has been claimed.
