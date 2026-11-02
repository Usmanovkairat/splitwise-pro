# Cloud deployment readiness and account-dependent work

No cloud deployment URL is available. No cloud resource, billing upgrade or account connection was created. The application remains a private single-workspace tool; do not expose its financial API to the public internet without application authentication/authorization or a verified identity-aware access layer.

## First-provider compatibility review — 2026-11-02

| Provider | Officially documented behavior | Effect on this assignment |
|---|---|---|
| Railway | [Dockerfiles documentation](https://docs.railway.com/builds/dockerfiles) supports importing Compose services and volumes as staged project changes, with incomplete coverage of Compose options. [Deployment guide](https://railway.com/guides/deploy-scale-docker-containers-railway) describes translation into Railway services rather than a production Compose orchestrator. | Best candidate for the requested initial provider. Importing `compose.yaml` is a supported starting point, but is not the same as running `docker compose up` unchanged. Verify translated secrets, networking, health dependencies and volumes. Account access and explicit cost approval remain required. |
| Render | [Docker deployments](https://render.com/docs/docker) build/run individual Docker services; [Blueprints](https://render.com/docs/blueprint-spec) define services and databases using Render's `render.yaml` schema. | An app image plus Render Postgres is an adaptation, not evidence of a direct Compose deployment. Do not label it as such. |
| Vercel | [Compose compatibility](https://vercel.com/i/can-you-run-docker-compose-on-vercel) says Compose itself is not a deployment target; its components must be translated, with stateful databases/volumes moved to external services. | The current PostgreSQL Compose volume cannot run unchanged there. Docker image support does not imply Compose support. |

A strict “Docker Compose only” production requirement therefore needs instructor acceptance of Railway's import/translation or a VM that actually runs Compose. The supplied GCP VM does run Docker Compose, but does not satisfy the separately requested initial Render/Railway/Vercel deployment. That first deployment remains blocked; no URL or passing cloud test is claimed.

## GCP Terraform implementation

See [`infra/gcp/README.md`](../infra/gcp/README.md) for provisioning, private access, backups, data migration, rollback and cleanup. The configuration includes one small VM, custom VPC, IAP-only SSH firewall, persistent database disk, OS Login, a VM service account with no project data privileges, resource-limited Compose services, and optional project budget alerts. Planning is blocked by default until the owner explicitly permits possible charges.

The application is reached at local `http://127.0.0.1:8000` through an encrypted SSH/IAP tunnel. This is a protected remote deployment design, not a public HTTPS website. A verified HTTPS public endpoint remains future work requiring identity/access decisions.

Official references checked during implementation:

- [Google IAP TCP forwarding](https://docs.cloud.google.com/iap/docs/using-tcp-forwarding): authorized encrypted TCP forwarding and the `35.235.240.0/20` ingress range.
- [Linux VM startup scripts](https://docs.cloud.google.com/compute/docs/instances/startup-scripts/linux): metadata startup scripts run as root at boot.
- [Terraform Google compute instance](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance) and [billing budget](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/billing_budget) resource definitions.
- [Google Free Program](https://docs.cloud.google.com/free/docs/free-cloud-features): account eligibility, trial duration and resource quotas must be checked for the actual account. This implementation neither upgrades an account nor guarantees zero cost.

## Gated continuous deployment

`.github/workflows/deploy.yml` listens only for a successful `Verify SplitWise Pro` run on `main` in this repository. It checks out that exact verified commit, refuses an obsolete main revision, builds/pushes its image, and deploys an immutable digest through IAP. The `production` environment gates credentials. Failed CI does not trigger a deployment. Deployment concurrency is serialized.

The VM script `deployment/deploy-gcp.sh` pulls the image before downtime, stops the app, makes a protected `pg_dump`, replaces the app image, waits for Compose health and checks the HTTP health endpoint. A failed release restores the prior Compose configuration and attempts image rollback, then fails the job. A schema-incompatible migration can still require a reviewed restore from the backup; an automatic image rollback is not a promise that database downgrade is safe. The script retains backups and needs a retention/off-VM backup policy before long-term operation.

Before enabling CD, the account owner must:

1. Provision the reviewed Terraform infrastructure with explicit cost approval. Configure the `production` GitHub Environment, restrict it to `main`, and add required reviewers if available for the repository plan.
2. Configure Google Workload Identity Federation for GitHub OIDC. Restrict provider conditions to this exact repository and `refs/heads/main`; prefer numeric repository/owner IDs as additional conditions. Grant the deploy identity only the needed instance lookup, IAP tunnel and OS Login admin permissions, and service-account-user permission on the VM's service account. Bind `roles/iam.workloadIdentityUser` only to the scoped GitHub principal. No JSON service-account key is required.
3. Publish the GHCR package and explicitly make the application image anonymously pullable, or implement a separately reviewed private-registry credential mechanism. The VM has no GHCR token. A private package makes the initial `docker pull` fail before the current app is stopped.
4. Set repository/environment variables: `GHCR_IMAGE` (lowercase `ghcr.io/OWNER/splitwise-pro`), `GCP_PROJECT_ID`, `GCP_ZONE`, `GCP_VM_NAME`, `GCP_WORKLOAD_IDENTITY_PROVIDER` (full provider resource), and `GCP_DEPLOY_SERVICE_ACCOUNT` (email). Keep `DEPLOY_ENABLED` unset/false until the tested VM, WIF and image permissions are ready. Then explicitly set `DEPLOY_ENABLED=true`.
5. Merge a verified change into `main`, approve the production environment if required, inspect the deployment logs, open the IAP tunnel and run browser acceptance checks. Record the actual revision, image digest and result in the GitHub deployment issue.

GitHub Environment access and Google IAM permissions are account-side settings and have not been created or verified. The automatic path is prepared, not active.

## Local validation evidence

- `bash -n infra/gcp/startup.sh.tftpl deployment/deploy-gcp.sh`: passed.
- Terraform 1.13.4 `terraform init -backend=false -input=false`: passed; Google provider 6.50.0 installed and `.terraform.lock.hcl` recorded.
- `terraform fmt -check`: passed. Terraform `templatefile(...)` evaluation of the complete startup script in a provider-free console: passed (3,844 rendered characters).
- `terraform validate`: blocked by this execution environment. The installed provider cannot open its local RPC Unix socket (`listen unix /tmp/plugin...: socket: operation not permitted`). Configuration schema validation has therefore **not** passed; rerun it in a normal Terraform environment before planning.
- `.github/workflows/deploy.yml` parsed successfully as YAML. The hosted workflow and VM release script have not run against a cloud account.
- Account-dependent `terraform plan/apply`, Docker bootstrap on GCP, IAP connection, cloud persistence and CD: not executed; no connected authorized cloud account is available.
