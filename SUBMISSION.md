# SplitWise Pro — Part II submission

## Final verified implementation — 2026-11-02

Independent QA verified commit `23407fba510e13fbac195a25ee9c5f0868bbdaab` in successful [Actions run 41452285813](https://github.com/Usmanovkairat/splitwise-pro/actions/runs/41452285813): **68 backend tests, 28 frontend tests, 8 mock browser tests, and 22 browser scenarios each against SQLite, PostgreSQL and the actual Docker Compose image passed**. Full-ledger recreation retained groups, members, expenses/shares, partial settlements, balances and analytics. Both verification and infrastructure jobs passed; Terraform schema validation passed. The final source includes separately named expense creation, navigation and persistence acceptance scenarios.

The existing application is preserved; additions include expense search/category filters, safe PostgreSQL transfer, production readiness checks, full-stack Compose, granular E2E, CI, protected GCP Terraform and default-disabled OIDC CD. Independent issue closure is approved for #42–44, #48–68, #70, #72 and #73; #69 was already verified. Cloud #45–47 remain open. No first-provider deployment, GCP apply, live CD, public HTTPS endpoint or cloud URL is claimed. See [cloud account steps](deployment/CLOUD.md) and [full QA evidence](_docs/qa/deployment.md).

Repository: https://github.com/Usmanovkairat/splitwise-pro

Project: local-first shared expense manager, distinct from StudyFlow.

## Verified implementation

- React/TypeScript/Vite frontend, deterministic mockService and real API mode.
- FastAPI REST backend with separately documented in-memory iteration.
- Source OpenAPI contract: `openapi.yml`.
- SQLite persistence via SQLAlchemy 2 and Alembic.
- Groups, members, expenses, equal/exact/percentage splits, balance calculation, partial settlements and analytics.
- Actual chronological iterations and agent/PM/QA documentation in `_docs/`.
- Genuine available brainstorming provenance in `chat-brainstorm.md`.

## Executed QA evidence

See `_docs/qa/final.md` for exact executed commands and acceptance criteria.

- Backend: **54 passed**.
- Frontend: **27 passed**.
- Mock browser: **8 passed**.
- SQLite integration browser: **3 passed**.
- OpenAPI validation: PASS.
- Frontend production build: PASS.
- Real screenshots: `_docs/screenshots/integrated-desktop.png` and `integrated-mobile.png`.

Hosted GitHub Actions workflow run **39369274006** on commit `3a1f5aa442a4d0801143959fbb6db95ed6964f96` completed **success** on 2026-10-20: https://github.com/Usmanovkairat/splitwise-pro/actions/runs/39369274006

## Installation

Follow the tested instructions in [README.md](README.md), including separate backend/frontend terminals and initial Alembic migration. The app is available at `http://127.0.0.1:5173` when running locally.

## Issue closure and limitations

Independent QA records PASS for functional and browser acceptance, including previously observed bugs #38–#41. Verified passing MVP/bug issues are being closed against their acceptance evidence. **Do not interpret this document as a guarantee that every GitHub Issue is closed:** inspect the live issue list before final submission. Post-MVP #32 (CSV export) and #33 (authentication) are intentionally open.

Limitations: single local workspace, no authentication or real-money payments, no cloud deployment; one backend worker recommended. Settlement suggestions are deterministic but not proven globally minimum transfer count. A successful CI run does not certify all possible accessibility criteria.

StudyFlow remains unchanged.

## Test, Containerise and Deploy assignment — current branch

Delivery is tracked in PR [#71](https://github.com/Usmanovkairat/splitwise-pro/pull/71), on `feature/container-postgres-deployment`. The older Part II results above are historical and do not establish PostgreSQL or cloud deployment success.

Implemented: full-stack multi-stage image, PostgreSQL Compose with health/resource limits and persistent volume, safe transactional SQLite transfer with backup and reconciliation, 22 independent integrated Playwright scenarios, search/category filters, PostgreSQL/Compose CI, protected GCP Terraform and default-disabled OIDC deployment workflow. Required role documents and granular `e2e-test` issues are present.

Local independent evidence: **65 backend tests passed / 3 PostgreSQL tests skipped; 28 frontend tests passed; contract and frontend build passed.** The real built SPA and readiness regressions passed outside Docker. Local Chromium download, PostgreSQL runtime and Docker runtime were unavailable. The hosted workflow must verify those checks; see [independent QA](_docs/qa/deployment.md) and the latest [Actions runs](https://github.com/Usmanovkairat/splitwise-pro/actions).

No first-provider deployment, GCP resources or public HTTPS URL is claimed. Terraform formatting/init/template checks succeeded; provider schema validation was blocked locally by a Unix-socket restriction and is included in hosted CI. Account-dependent steps, provider compatibility, access controls, cost approval, secrets/variables, backup and cleanup are documented in [cloud readiness](deployment/CLOUD.md). Keep cloud and browser-dependent issues open until their actual acceptance checks succeed.

Hosted verification of commit `41760bcb04c94dbe1d01697ad603a6887c58ed7c` completed successfully: [Actions run 41450722287](https://github.com/Usmanovkairat/splitwise-pro/actions/runs/41450722287). It ran **68 backend tests (including real PostgreSQL), 28 frontend tests, 8 mock browser tests and 20 browser scenarios each against SQLite, PostgreSQL and the actual Compose image**. Docker build/readiness, full-ledger container recreation and Terraform schema validation passed. The expanded 22-scenario suite adds distinct creation/persistence coverage; its exact hosted result is recorded separately in the QA evidence and latest PR checks. This is test evidence, not a cloud deployment claim.
