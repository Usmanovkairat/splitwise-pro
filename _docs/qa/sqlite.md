# Iteration 4 independent SQLite QA

Result: PASS #20–22 and #26 persistence gate. Independently executed `.venv/bin/python -m pytest backend/tests -q`:53 passed,1 Starlette deprecation warning,4.87s. Source contract validator rerun: `openapi.yml: OK`.

Reviewed shared API fixture: each API acceptance runs against isolated memory and Alembic-migrated temporary SQLite repositories. Reviewed/executed persistence suite: metadata has no migration diff; upgrade/downgrade/upgrade succeeds; foreign key failure leaves no orphan; failed expense/share update restores original ledger; injected deletion failure rolls back entire group; normalized-name unique constraint; actual Uvicorn process termination/restart retains group,members,expense,settlement,balances,analytics and300 minor outstanding after partial payment.

Independent extra scenario: migrated a separate temporary database; created Straße; disposed engine; constructed fresh engine/repository/app against same file; padded STRASSE returns422 and member list remains exactly original row. This independently verifies #37 SQLite/restart segment. Full #37 integrated modal segment remains pending stage5.

Reviewed normalized SQLAlchemy models and repository transaction abstraction; app default SQLite, configurable DATABASE_URL, SQLite foreign keys enabled per connection. No user database file is required or added to Git. Local single-worker locking limitations documented explicitly.
