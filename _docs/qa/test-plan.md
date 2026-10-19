# Independent QA acceptance plan

QA owner: independent QA agent, separate from frontend/backend authors. Status: awaiting iteration handoffs; this document records planned checks, not passed tests.

## Iteration gates

1. Mock frontend: run frontend test/build scripts; operate group, member, expense and settlement flows using mock service; inspect desktop/mobile layout and capture screenshots. No persistent backend expected here.
2. Contract: validate OpenAPI 3.1 syntax, operation coverage, error schemas and frontend compatibility.
3. In-memory API: independently run pytest; test CRUD, invalid identifiers, split validation, protected relationships, settlement effects, and zero-sum balances. Persistence is deliberately absent.
4. ORM persistence: run migrations, use isolated temporary database, create expenses/settlements, restart application against the same file, compare resources and balances.
5. Integration: exercise actual frontend/API workflows, loading/error/empty states, refresh and persisted data.
6. Final: rerun automated suites and build, browser regression suite, desktop/mobile screenshots, inspect all MVP/bug acceptance evidence and actual CI result.

## Money and relationship cases

- Equal 100 minor units across three stable member IDs must produce deterministic 34/33/33 shares.
- Exact positive/nonnegative shares must sum to total; reject mismatched totals.
- Percentage basis points must total 10000; distributed shares must sum to expense amount.
- Net group balances sum to zero before/after partial settlement, editing/deleting expenses.
- Reject foreign-group payer/participant/member and invalid or same-person settlement.
- Inspect member removal with referenced transactions and group deletion confirmation.
- Validate date, amount, member selection, empty group and duplicate submission behavior.

## Browser workflow

Create group → add at least three members → add equal/exact/percentage expenses → inspect balances/analytics → edit and delete expense → record partial settlement → inspect history → refresh. Repeat critical actions at 390px viewport; check horizontal overflow and usable dialogs.

## Defect handling

Report only reproducible observed defects to root for real `user-test-bug` issue creation. PM grooms; engineer fixes; QA independently verifies original reproduction and regression cases before PASS. Record actual commands, counts, outputs and evidence paths without inventing outcomes.
