# Product and delivery plan

## Users and problem
Roommates, friends planning trips, and event organizers need an auditable answer to who paid, who owes, and how to settle without rounding drift. The core journey is create group → add members → record a shared expense → inspect balances → record partial repayment.

## MVP
Single local workspace; multiple groups; KZT/USD/EUR/GBP currency per group; group rename/delete; members with reference protection; expense create/edit/delete; equal/exact/percentage allocation; deterministic balances and simplified suggestions; partial settlements; category/timeline/contribution analytics; responsive accessible interface; real SQLite storage.

User stories: As an organizer I create a trip group and add participants. As a payer I split a bill using the agreed method. As a member I see my net debt and record a partial settlement. As a group I review spending by category and date. As a returning user I retain records after refresh and backend restart.

## Numerical and data constraints
Store currency values as integer minor units; API IDs are strings. `amount_minor > 0`; exact `split_values` values sum to the expense; percentage values are integer basis points totaling 10000; equal uses a value of 1 per participant. Largest remainder allocation sorts equal remainders by member ID. Member deletion is forbidden when referenced by payer, shares, or settlements. Settlements go from a current debtor to a current creditor and cannot exceed either outstanding amount. No cross-currency aggregation.

## Technical risks and controls
Money drift: integer arithmetic and invariant tests. Duplicate/stale resource references: membership validation and database foreign keys. Repository behavior divergence: shared API acceptance tests. Partial write failure: transactions. Overpayment: recompute balances before settlement. Data loss: migrations and restart tests. Schedule pressure: keep cloud hosting/authentication/export outside MVP.

## Iterations
0 planning and issues; 1 React frontend with deterministic mockService; 2 OpenAPI 3.1; 3 in-memory FastAPI; 4 SQLAlchemy/Alembic SQLite; 5 typed HTTP integration; 6 independent browser QA, real bug issues and fixes; 7 final suites/build/CI audit and submission. Each stage receives a separate commit and evidence in `_docs/iterations.md`.

The user said the deadline was ten hours from approximately 02:33 on 20 October 2026 (Asia/Qyzylorda): about 12:33 local. GitHub creation/closure timestamps are genuine service timestamps.
