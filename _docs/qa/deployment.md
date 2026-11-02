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
