# Deployment assignment audit — 2026-11-02

Source audited: existing `feature/container-postgres-deployment`, starting commit `c40265804ad01c13298657cd43e59c3581c9ce8f`. Existing features and history were preserved. The PM reviewed the live issue backlog before grooming it; no historical conversation, tests or dates were fabricated.

| Area | Starting state | Work in this iteration | Verification gate |
| --- | --- | --- | --- |
| Product | Working groups, members, expense CRUD, equal/exact/percentage splitting, balances, partial repayments, analytics | Preserve existing functionality; implement description/category filtering | Unit tests and real integrated browser scenarios |
| Architecture | React/Vite static frontend, FastAPI, SQLAlchemy/Alembic SQLite; in-memory/mock stages retained | Keep stack and history; use DATABASE_URL PostgreSQL driver | Backend tests and metadata parity on PostgreSQL |
| Container | Existing multi-stage image and Compose database volume | Pin driver; app readiness, resource limits; test mounted SPA and unknown API paths | Build image, browser acceptance and full-ledger recreation in CI |
| Existing data | Schema migration only; no SQLite data transfer | Read-only SQLite backup, integrity/FK checks, empty-target guard, transactions, row/ID verification and balance reconciliation | Safety regression plus real PostgreSQL transfer tests |
| Browser tests | Eight mock scenarios; three large integrated SQLite workflows | Twenty independent real-API scenarios, schema-isolated PostgreSQL fixture and external Compose target | SQLite, PostgreSQL and real image runs |
| CI | Contract/backend/frontend/build/mock/SQLite only | Add real PostgreSQL tests, full-stack Compose build, browser tests, recreation and failure evidence; Terraform validate | Hosted Actions results |
| Security | No application authentication; single local workspace | Preserve localhost binding; private GCP IAP design; no public financial API; protected backup files and no committed secrets | Static review; cloud IAM/tunnel checks remain account-dependent |
| Cloud | No infrastructure, CD or verified cloud URL | Terraform protected VM/disk/budget, disabled OIDC deployment, health/backup/image rollback; provider compatibility review | Terraform validation; account authorization, plan/apply, IAM and live acceptance still required |
| Documentation | Genuine brainstorming and previous iteration evidence; limited role aliases | Complete required roles, root aliases, migration/cloud instructions and independent evidence | File/source review and honest delivery status |

Initial inspection incorrectly suspected a static-assets path defect; a path regression test proved the original directory calculation was correct. No such defect was claimed as fixed. Actual defects were tracked separately: bare `/api` SPA fallback (#69), mobile overflow discovered by hosted Playwright (#72), and invalid optional Terraform budget notification block (#73). Search/filter implementation is #70 and browser acceptance is #55. Existing #42–56 were groomed; #57–68 provide per-feature E2E traceability.

Independent local QA and hosted results are recorded separately in `_docs/qa/deployment.md`. Local environment limitations do not establish failures of PostgreSQL/Docker themselves. Cloud configurations are prepared, but a Terraform validation PASS is not a deployment and a default-disabled workflow is not a running CD service.
