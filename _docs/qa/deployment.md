# Independent deployment QA — 2026-11-02

Independent QA ran these checks in the checked-out deployment branch. This records the current run; it does not reuse the older Part II results.

| Check | Actual result |
| --- | --- |
| `.venv/bin/python -m pytest backend/tests -q` | 64 passed, 3 skipped in 11.50s; skipped tests require `TEST_POSTGRES_URL` |
| `.venv/bin/python -m openapi_spec_validator openapi.yml` | PASS: `openapi.yml: OK` |
| `npm --prefix frontend test` | 28 passed, including case-insensitive search plus category filter and recovery from no results |
| `npm --prefix frontend run build` | PASS; Vite warned about a JavaScript chunk over 500 kB |
| Real built SPA through `backend.app.production` with TestClient, memory storage | PASS: root and deep link 200; compiled JS and CSS 200 with correct MIME types; API health 200; unknown API 404 |
| Production route regression #69 | PASS: `/api` and `/api/missing` return 404; static tests also check missing asset and encoded traversal |
| Readiness check | PASS: unmigrated/unavailable storage returns 503; memory fixture returns 200 |
| Search regression #70 | PASS at component-test level: combined search/category filtering and empty-result recovery; browser acceptance remains unverified |
| Playwright integration discovery | PASS: 20 separately defined scenarios |
| Playwright mock discovery | PASS: 8 scenarios |
| Real Playwright integration execution | BLOCKED: backend/Vite started, first test failed before interactions because Chromium executable was absent; 19 did not run; trace written to ignored `frontend/test-results/` |
| PostgreSQL integration | NOT EXECUTED locally: no running PostgreSQL; 3 conditional tests skipped |
| Docker build, Compose startup and recreation | NOT EXECUTED locally: Docker executable unavailable |
| GitHub Actions workflow | YAML parsed; configuration reviewed. Hosted run not verified in this QA record |
| Python deployment scripts | `compileall` PASS; enhanced persistence script API payloads/comparison/cleanup exercised against temporary real SQLite API with Docker subprocess explicitly stubbed; this does not test recreation |

The production tests exercise mounted temporary assets and the actual compiled frontend separately. Neither check substitutes for running the image. The corrected route behavior is suitable for closing #69; #70 has implementation/component evidence only, so any browser-specific acceptance must remain open until exercised.

## Inspection findings

- Compose publishes the app only on localhost, does not publish the database, requires an environment-supplied password, persists PostgreSQL in a named volume, and defines application/database health checks and resource limits.
- Startup migrates the schema before launching a single Uvicorn worker. The application has no authentication; public exposure of private financial records is not approved by these local checks.
- Migration code creates a restrictive-permission SQLite backup, validates backup integrity/foreign keys, requires a matching target revision and empty ledger, locks PostgreSQL ledger tables, compares full rows and reconciles balances inside one target transaction. Executed SQLite safety tests pass; actual PostgreSQL transfer tests remain conditional.
- CI includes PostgreSQL service tests, SQLite and PostgreSQL browser tests, a full image/Compose browser run, persistence recreation and failure artifacts. This is a configuration review, not a CI success claim.
- `deployment/verify_compose.py` recreates both services without deleting the volume and compares group fields, members, expense shares, a partial settlement, balances and analytics. It requires Docker and was not executed here.

## Environment limitations

Python 3.12.14 and Node 24.22.1 were available. Python and frontend dependencies were installed. An initial simultaneous npm install caused missing commands; after the frontend engineer repaired the install, the independent tests/build succeeded. Chromium download attempts by the frontend engineer returned invalid ZIP archives. No browser binary was found locally.

An attempt to obtain a native PostgreSQL runtime encountered a truncated package and a process-identity restriction: this container runs as UID 0 without setuid/setgid capabilities, while PostgreSQL requires a non-root process. `runuser` failed with `cannot set groups: Operation not permitted`. No escalation or cloud resource was used.

The test run emitted a Starlette/httpx deprecation warning. It did not fail the backend tests. No issues were closed by this QA agent, and no cloud deployment or financial resource provisioning was performed.

## Independent GCP IaC/CD review

Reviewed `infra/gcp/`, `deployment/deploy-gcp.sh` and `.github/workflows/deploy.yml` without cloud credentials or provisioning.

Executed checks:

- `bash -n infra/gcp/startup.sh.tftpl deployment/deploy-gcp.sh`: PASS.
- Terraform 1.13.4 `fmt -check`: PASS.
- Terraform `validate`: NOT PASSED. Provider schema loading failed before validation: Google provider 6.50.0 did not negotiate its local plugin handshake (`Failed to read any lines from plugin's stdout`). The orchestrator separately observed a local Unix-socket restriction. This is an environment blocker, not proof that the provider configuration is valid.
- Deployment workflow YAML parses; explicit successful-main, same-repository, opt-in and production-environment gates are present. Deploy concurrency is serialized and the checked-out source is the verified SHA; an obsolete main SHA is rejected before publishing.
- Rendered startup Compose YAML parses after template substitutions. It selects the provided immutable image with no build override, keeps PostgreSQL credentials as Compose environment interpolation, exposes only localhost application port, leaves database unpublished and binds data to the attached persistent disk.
- Deterministic mocked release-script success/failure checks: PASS. The script pulls before stopping the app, creates a mode-0600 database dump, updates only the app image, and on failed rollout restores the exact previous Compose file, attempts restart and exits nonzero. Docker/curl commands were mocks; this does not verify a live rollout, schema compatibility, backup restorability or actual container readiness.

The bootstrap preserves an existing Compose release and `.env` on reboot. Deployment takes a lock; rollback changes the image/configuration without automatically overwriting or downgrading database contents. A backup on the same data disk is not off-VM disaster recovery. Schema-incompatible migrations still require a reviewed restore. No public HTTP firewall rule exists; app access requires the protected tunnel. Owner billing authorization defaults false; a budget alert is optional and is not a spending cap. The protected disk deliberately blocks normal destruction until an explicit deletion decision.

Remaining account-side requirements include provider schema validation in a normal runtime, reviewed plan, actual cost approval, IAM/WIF/environment setup, anonymously pullable registry image, cloud apply, tunnel access and live deployment/rollback/restore tests. No cloud operation ran during this review. Hosted CI status is tracked separately by the orchestrator; this section does not assert a completed Actions run.

## Hosted verification superseding local runtime blockers

Independent QA retrieved GitHub Actions job metadata and decoded logs through the connected GitHub tools. Local absence of Docker/PostgreSQL/Chromium no longer means those checks are unexecuted everywhere; retain the local results above as their actual historical run.

On commit `64baf` (run [41450332170](https://github.com/Usmanovkairat/splitwise-pro/actions/runs/41450332170), verification job `125293662168`), decoded logs independently confirm:

- Backend: **67 passed**; frontend: **28 passed**.
- Mock Playwright: **8 passed**.
- Real SQLite browser suite: **20 passed**.
- Real PostgreSQL browser suite: **20 passed**.
- Multi-stage Docker image built; application and PostgreSQL containers became healthy.
- Browser tests against the actual Compose image: **20 passed**.
- Forced Compose service recreation: logged `PASS: groups, members, expense shares, partial settlement, balances and analytics survived Compose recreation`.

The long-name 390px responsive regression is part of those 20 browser tests. The earlier failure was reproduced in hosted CI; the repaired maximum-length-name fixture passed SQLite, PostgreSQL and actual-image suites. These are real hosted checks, not the local mocked release tests.

For commit `41760bcb04c94dbe1d01697ad603a6887c58ed7c`, push run [41450722287](https://github.com/Usmanovkairat/splitwise-pro/actions/runs/41450722287), independent QA retrieved infrastructure job `125294960276` logs. Terraform 1.13.4 initialized locked Google provider 6.50.0 and `terraform validate -no-color` printed **`Success! The configuration is valid.`** Shell syntax and Terraform formatting also passed. This verifies repair #73; it does not provision a budget or cloud instance. The local final backend run separately produced **65 passed, 3 PostgreSQL-only skips** after the health/OpenAPI contract regression was added.

A later test-only commit `d2e770215c35daa83070061beaefb7643e3fd696` strengthens the existing search scenario by comparing unchanged analytics and editing/deleting an expense with an active filter. Its hosted result will be recorded after completion. No default-disabled continuous deployment or cloud endpoint is claimed.

The complete `41760bcb04c94dbe1d01697ad603a6887c58ed7c` push run **41450722287 finished successfully**, with both jobs successful. Independent QA decoded verification job `125294960596`: **68 backend tests**, **28 frontend tests**, **8 mock browser tests**, **20 SQLite browser tests**, **20 PostgreSQL browser tests** and **20 actual Compose-image browser tests passed**; the full ledger recreation check printed PASS. This includes the health/OpenAPI contract test and the repaired mobile regression. Feature issue closure is held pending separately named persistence/baseline-expense scenarios requested by PM; the successful 20-scenario run is retained as its actual evidence, not relabeled as a 22-scenario run.

Expanded-suite run [41451724291](https://github.com/Usmanovkairat/splitwise-pro/actions/runs/41451724291) on `e518e045cd0fecc3ed26f2a9b5de9fe4c9054953` failed a newly authored exact-match category selector in the standalone #50 scenario. Independent decoded job `125298290299` confirms **21 SQLite scenarios passed and 1 failed before category selection**, alongside 68 passing backend tests, 28 frontend tests and 8 mock browser tests. The failure is retained as actual evidence; it is not an application feature failure or a passing 22-scenario run. The selector was corrected in test-only commit `23407fba510e13fbac195a25ee9c5f0868bbdaab`; its replacement hosted result is pending.

## Final independent acceptance — verified revision 23407fba

Final PR run [41452285813](https://github.com/Usmanovkairat/splitwise-pro/actions/runs/41452285813) on exact commit `23407fba510e13fbac195a25ee9c5f0868bbdaab` completed with **both jobs successful**. Independent QA read the actual job metadata and decoded logs for verification job `125300174284` and infrastructure job `125300173903`.

| Final executed check | Result |
| --- | --- |
| Backend including PostgreSQL transfer/integration | **68 passed**, 1 deprecation warning, 7.65s |
| Frontend unit/component tests | **28 passed** |
| OpenAPI contract and frontend production build | **PASS** |
| Mock browser workflows | **8 passed** |
| Real SQLite browser workflows | **22 passed**, 39.7s |
| Real PostgreSQL browser workflows | **22 passed**, 40.3s |
| Built full-stack Compose image browser workflows | **22 passed**, 23.3s |
| App and PostgreSQL recreation | **PASS**: groups, members, expense shares, partial settlement, balances and analytics survived |
| Terraform init/format/provider schema validation | **PASS**; decoded log says `Success! The configuration is valid.` |

The separately named baseline expense-creation #50 and reopened-page persistence #68 scenarios passed in all three integrated browser environments. Navigation #67 has its own scenario. Equal/exact/percentage splitting check relevant invalid allocations before correction. The mobile regression verifies a valid 80-character unbroken name at 390px, then checks navigation/dialog layout and keyboard dismissal. Search verifies case-insensitive matching, combined category filtering, no-results recovery, unchanged analytics and edit/delete while the filter remains active. Test data is isolated and owned records are cleaned up. Relevant validation/error coverage is implemented as independent tests and selected feature-specific negative/correction assertions; this does not claim that every conceivable negative case is repeated inside every feature scenario.

Independent QA approves closure of **#42, #43, #44, #48–#68, #70, #72 and #73** against the committed implementation, named browser scenarios, database regression tests and this final hosted evidence. #69 was separately verified earlier. This approval concerns implemented/tested acceptance, not an assertion of exhaustive security, accessibility, performance or cloud-operation certification. The QA agent did not close issues; the orchestrator links the verified revision and records delivery.

**#45, #46 and #47 remain open/account-dependent** as requested: provider deployment and protected cloud provisioning/CD are not activated or demonstrated. The prepared Terraform configuration now validates, but no cloud `plan/apply`, budget creation, VM deployment, HTTPS public endpoint, IAP session or enabled continuous deployment is asserted. The `DEPLOY_ENABLED` gate remains a configuration requirement; successful CI is not a cloud deployment URL.
