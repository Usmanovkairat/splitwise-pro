# Backend

From repository root:

```sh
python -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
.venv/bin/uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
.venv/bin/python -m pytest backend/tests -q
```

This iteration uses an isolated in-memory repository. Restarting intentionally clears data. The application factory accepts a repository, keeping domain rules independent of persistence. The committed `openapi.yml` is the source contract; `/docs` is FastAPI's interactive route documentation.

All mutation validation occurs before repository writes. A process-local lock serializes requests including settlement validation against current balances. This is a single-process local workspace. It has no authentication and must bind to localhost; it does not transfer money.
