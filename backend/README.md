# Backend

Run these commands from the repository root:

```sh
python -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
.venv/bin/alembic -c backend/alembic.ini upgrade head
.venv/bin/uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

On Windows use `.venv\Scripts\python.exe -m pip`, `-m alembic`, and `-m uvicorn` instead. The default database is `backend/splitwise.db`. Run migrations before first launch; the application deliberately does not silently create tables. Set `DATABASE_URL` for another SQLAlchemy connection URL. SQLite foreign keys are enabled on every connection. Data files are ignored by Git.

For the historical in-memory implementation:

```sh
SPLITWISE_STORAGE=memory .venv/bin/uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Memory mode starts empty and loses data on restart. SQLite is the final default. API and domain rules are shared through the repository interface. ORM records normalize group/member/expense/share/settlement data; monetary columns are 64-bit integers. A unique normalized member name constraint complements casefold validation. Expense/share replacement and group cascade deletion each use one transaction.

```sh
.venv/bin/python -m pytest backend/tests -q
.venv/bin/python -m openapi_spec_validator openapi.yml
```

The API suite runs against both isolated memory and migrated temporary SQLite repositories. Additional tests check Alembic upgrade/downgrade and metadata consistency, foreign keys, rollback on a failed share update, injected group deletion failure, normalized-name database uniqueness, and actual Uvicorn process termination/restart with the same SQLite ledger.

The committed `openapi.yml` is the source contract. `/docs` provides interactive route documentation. Monetary inputs use integer minor units; all supported currencies have two decimals. Exact splits must sum to the amount, percentages are basis points summing to 10000, and largest fractional remainder allocation breaks ties by ascending member ID. Suggested settlements are deterministic and do not promise a globally minimal transfer count.

A process-local lock serializes all API reads and writes, including settlement validation and insertion. Run one Uvicorn worker: this is a local single-workspace application, not a multi-worker service. It has no authentication, binds to localhost, and records settlements without transferring money. CORS allows only the two local Vite development origins.
