# SplitWise Pro baseline audit

Scope covers the previous container and PostgreSQL assignment on `feature/container-postgres-deployment`, its merge into `main`, and the gaps for DevOps and Observability.

| Area | Evidence and finding |
| --- | --- |
| Repository | [PR #71](https://github.com/Usmanovkairat/splitwise-pro/pull/71) merged the deployment branch into `main`. Keep the existing React SPA, FastAPI application, SQLAlchemy repository interfaces and Alembic migrations. |
| Local full-stack deployment | The multi-stage `Dockerfile` builds the Vite frontend and serves it from the FastAPI process. Compose uses PostgreSQL 16, a persistent volume, service health checks, resource limits and a loopback-only app address. The existing startup script migrates the database before Uvicorn starts. |
| PostgreSQL and rollback | [#43](https://github.com/Usmanovkairat/splitwise-pro/issues/43) is closed. The SQLite transfer utility protects the source backup, checks the empty target and validates the transferred rows and balances. Preserve the production database volume during image promotion or rollback. An image rollback may still require a compatible database schema. |
| Automated verification | The `verify` and `infrastructure` jobs in [run 41452285813](https://github.com/Usmanovkairat/splitwise-pro/actions/runs/41452285813) both passed. Job steps confirm OpenAPI, backend tests including PostgreSQL migration, frontend tests and build, mock and integrated Playwright, full-stack Compose browser tests, persistence after recreation, and Terraform validation. These results apply to the prior revision. |
| Deployment infrastructure | GCP Terraform and IAP/SSH access documentation are present. [#45](https://github.com/Usmanovkairat/splitwise-pro/issues/45), [#46](https://github.com/Usmanovkairat/splitwise-pro/issues/46) and [#47](https://github.com/Usmanovkairat/splitwise-pro/issues/47) are open. Prior QA and PR evidence record no verified first-provider deployment, live GCP deployment, production CD or hosted URL. See [cloud readiness](../deployment/CLOUD.md). |
| Deployment workflow | The baseline `.github/workflows/deploy.yml` activates on a successful main verification workflow when deployment is enabled, then builds and publishes an image. Part II needs a development verification record and manual, exact-digest promotion for production. |
| Environment isolation | The baseline Compose setup has one app/PostgreSQL pair and one default host port. Part II needs explicit development and production settings, isolated credentials, networks and volumes, plus an environment label on telemetry. An authenticated access boundary is required for any remote access to this single-workspace application. |
| Observability | The baseline application exposes database-backed readiness at `/api/health`. The new scope adds OTLP export, signal backends, business metrics, dashboards, operational alerts and authenticated incident triage. |

The existing hosted verification is the baseline regression checklist. The observability assignment has its own acceptance evidence and GitHub Issues.

| Issue | Scope |
| --- | --- |
| [#74](https://github.com/Usmanovkairat/splitwise-pro/issues/74) | Development environment |
| [#75](https://github.com/Usmanovkairat/splitwise-pro/issues/75) | Production environment |
| [#76](https://github.com/Usmanovkairat/splitwise-pro/issues/76) | OpenTelemetry SDK and Collector |
| [#77](https://github.com/Usmanovkairat/splitwise-pro/issues/77) | Documentation and runbooks |
| [#78](https://github.com/Usmanovkairat/splitwise-pro/issues/78) | Manual production promotion |
| [#79](https://github.com/Usmanovkairat/splitwise-pro/issues/79) | Business metrics |
| [#80](https://github.com/Usmanovkairat/splitwise-pro/issues/80) | Distributed traces |
| [#81](https://github.com/Usmanovkairat/splitwise-pro/issues/81) | Structured logs |
| [#82](https://github.com/Usmanovkairat/splitwise-pro/issues/82) | Grafana dashboard |
| [#83](https://github.com/Usmanovkairat/splitwise-pro/issues/83) | Alerting |
| [#84](https://github.com/Usmanovkairat/splitwise-pro/issues/84) | AI on-call responder |
| [#85](https://github.com/Usmanovkairat/splitwise-pro/issues/85) | Integration and CI verification |
