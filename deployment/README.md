# Container deployment (work in progress)

Run locally:
1. Copy .env.example to .env and replace POSTGRES_PASSWORD.
2. Run `docker compose up --build -d`.
3. Open http://127.0.0.1:8000 and http://127.0.0.1:8000/api/health.
4. Run `docker compose down` to stop without deleting data.

The app image contains both the static Vite build and FastAPI; PostgreSQL is a separate Compose service. Alembic migrations run before the web server starts. Do not expose this app publicly yet: it has no authentication and its application-level write lock is process-local. The Compose port intentionally binds localhost only.

Existing SQLite records are NOT automatically migrated by this setup. A separate verified export/import and reconciliation process is required before switching a populated installation. No cloud infrastructure has been provisioned.
