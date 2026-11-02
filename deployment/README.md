# Container deployment and SQLite cutover

The multi-stage Dockerfile builds the Vite frontend and serves its static files and FastAPI from one non-root Python container. Compose runs that image with PostgreSQL 16, a persistent volume, readiness checks and CPU/memory limits. One Uvicorn worker preserves the current process-local settlement lock.

## Start an empty local workspace

1. Copy `.env.example` to `.env`.
2. Generate a password with `python -c "import secrets; print(secrets.token_hex(24))"` and replace the placeholder. Use URL-safe letters/numbers because Compose interpolates it into a database URL.
3. Run `docker compose up --build --wait`.
4. Visit http://127.0.0.1:8000; readiness is http://127.0.0.1:8000/api/health. API documentation remains at `/docs`.
5. `docker compose down` stops services and preserves data. **`docker compose down -v` permanently deletes the local volume.**

No database port is published. The app binds the host loopback interface only. The app has no multi-user authentication; keep it behind the documented IAP SSH tunnel rather than exposing private financial data.

`SPLITWISE_STORAGE=sqlite` is the legacy name for the SQLAlchemy repository; the actual database is selected by `DATABASE_URL`. The readiness response includes the actual database dialect.

## Transfer an existing SQLite ledger

Stop both SQLite and PostgreSQL application processes before transfer. Keep them stopped until validation and cutover are complete. Do not start an empty replacement and discard your old file.

```sh
# Start only the empty target database and run its schema migration.
docker compose up -d --wait db
docker compose run --rm --no-deps app python -m alembic -c backend/alembic.ini upgrade head
# Mount the existing ledger read-only and a separate writable backup folder.
# Create backups first; adapt these absolute directories to your system.
mkdir -p backups
docker compose run --rm --no-deps --user "$(id -u):$(id -g)" \
  -v "$PWD/backend:/source:ro" -v "$PWD/backups:/backup" app \
  python -m backend.scripts.migrate_sqlite_to_postgres \
  --source /source/splitwise.db --backup /backup/before-postgres.db
```

Build the app image first with `docker compose build app`. The source database must already be at the same Alembic revision as the target; migrate the original SQLite installation and retain its original backup before transferring if necessary. The utility refuses an existing backup path or a non-empty target. It creates a 0600 SQLite backup using the SQLite backup API, checks integrity and foreign keys, preserves identifiers and relationships, then compares full rows and reconciles balances in one PostgreSQL transaction. Failures roll back target inserts; retain the backup for investigation. CLI errors intentionally omit potentially sensitive driver details.

After the command prints verified row counts and `balances_reconciled: true`, run `docker compose up -d --wait app` and inspect groups, expenses, repayments and balances. Retain both original and backup offline. PostgreSQL needs separate ongoing backups; this one-time transfer is not a backup policy.

Rollback before any new writes: stop the PostgreSQL app and point the original local installation back to its original SQLite file or protected backup. After new PostgreSQL writes, pause both installations and reconcile those writes before switching back; never silently discard them. Schema downgrades are not a safe substitute for data restoration.

## Test the integrated application

```sh
# Disposable PostgreSQL database only; pytest creates/drops its own UUID schemas.
TEST_POSTGRES_URL=postgresql+psycopg://user:password@localhost/test_db .venv/bin/python -m pytest backend/tests -q
# Temporary SQLite fixture by default; dedicated PG fixture with QA_DATABASE_URL.
cd frontend
QA_DATABASE_URL=postgresql+psycopg://user:password@localhost/test_db npx playwright test --config playwright.integration.config.ts
# Against the running real Compose app (returns to root for persistence script):
QA_BASE_URL=http://127.0.0.1:8000 npx playwright test --config playwright.integration.config.ts
cd ..
python deployment/verify_compose.py
```

The browser fixtures create and remove only their own groups. The PostgreSQL fixture creates a uniquely named schema; its database role needs schema creation permission. Never target production for automated tests. The persistence script recreates both containers while retaining the volume and compares records, rounded shares, partial settlements, balances and analytics.

CI runs unit tests, OpenAPI validation, SQLite/PostgreSQL integration, browser scenarios against SQLite/PostgreSQL/Compose, the full Docker build and container recreation. Failure traces, screenshots and container logs are uploaded. Local and hosted verification evidence must be read separately in `_docs/qa/deployment.md` and the linked Actions run; configured checks do not imply successful execution.

See [GCP infrastructure and account setup](../infra/gcp/README.md) for the protected deployment option. No resources are provisioned by committing these files.
