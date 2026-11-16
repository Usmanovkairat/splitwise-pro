# Isolated environments

Copy `.env.development.example` to `.env.development` and `.env.production.example` to `.env.production`. Use distinct URL-safe database passwords and distinct telemetry administration credentials. Keep the environment files outside Git.

```sh
docker compose --env-file .env.development -p splitwise-dev -f compose.yaml -f compose.observability.yaml up -d --build --wait
docker compose --env-file .env.production -p splitwise-prod -f compose.yaml -f compose.observability.yaml up -d --build --wait
```

These run independent Compose projects with independent networks and PostgreSQL volumes. The apps listen at http://127.0.0.1:8000 and http://127.0.0.1:8001. Append `/api/health` to inspect health, including the database. Each service uses an environment label in its telemetry. Apply observability credentials and bind-port settings from the telemetry guide before starting both stacks. Keep local bind addresses private since the app lacks login.

Run `docker compose` with the same env file, project and Compose files plus `down` to stop one environment and retain its data. Production-like testing is separate from a deployed GCP production host.
