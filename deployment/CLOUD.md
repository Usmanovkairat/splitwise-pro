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

## Manual production promotion

See [release procedure](../docs/manual-promotion.md). The prior automatic main-to-production workflow has been replaced by manual promotion. Existing protected GCP infrastructure, availability and account dependencies still apply.

## Local validation evidence

- `bash -n infra/gcp/startup.sh.tftpl deployment/deploy-gcp.sh`: passed.
- Terraform 1.13.4 `terraform init -backend=false -input=false`: passed; Google provider 6.50.0 installed and `.terraform.lock.hcl` recorded.
- `terraform fmt -check`: passed. Terraform `templatefile(...)` evaluation of the complete startup script in a provider-free console: passed (3,844 rendered characters).
- Local `terraform validate` is blocked by this environment's provider RPC Unix-socket restriction (`socket: operation not permitted`). The first hosted validation in [Actions run 41450015584](https://github.com/Usmanovkairat/splitwise-pro/actions/runs/41450015584) did execute and found an invalid `all_updates_rule` block: provider 6.50 requires a real notification channel or Pub/Sub topic when that block is present. The block has been removed; threshold rules remain and use default billing IAM email recipients. This follows [Google's default role-based notification behavior](https://docs.cloud.google.com/billing/docs/how-to/budgets-notification-recipients); no fake destination is configured. Hosted schema validation must pass on the corrected revision before readiness is claimed.
- `.github/workflows/deploy.yml` parsed successfully as YAML. The hosted workflow and VM release script have not run against a cloud account.
- Account-dependent `terraform plan/apply`, Docker bootstrap on GCP, IAP connection, cloud persistence and CD: not executed; no connected authorized cloud account is available.

## Hosted schema verification

On commit `41760bcb04c94dbe1d01697ad603a6887c58ed7c`, [run 41450722287](https://github.com/Usmanovkairat/splitwise-pro/actions/runs/41450722287), infrastructure job `125294960276` passed Terraform initialization, formatting and provider schema validation. The actual validator printed `Success! The configuration is valid.` This supersedes the local validation limitation for the committed configuration. No `plan/apply`, cloud resource, IAM connection, first-provider deployment or live CD has occurred.
