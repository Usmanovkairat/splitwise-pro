# Testing guidelines

Engineer execution evidence is followed by independent QA verification. Record exact command, actual result, environment and commit; do not replace evidence with an acceptance checkbox. Final recorded results live in `_docs/user-testing.md` and `_docs/iterations.md`.

Backend: pytest and TestClient exercise CRUD, invalid resources/membership, all split algorithms, deterministic tie cases, expense edits/deletes, exact/percentage mismatches, settlement bounds, zero-sum balances, rollback and memory/SQLite behavior parity. Use temporary isolated databases. Upgrade migrations into a fresh database, restart the application and verify durable state.

Frontend: Vitest/React Testing Library exercise deterministic mock mutations, forms, errors/loading/empty states and typed API failures. Test behavior that a user can observe, avoiding tests which merely repeat implementation.

Browser: Playwright against the real server creates a group/members, uses all three split modes with uneven cents, edits/deletes an expense, inspects category/timeline totals, records partial repayment, refreshes, and checks mobile/keyboard workflows. Capture screenshots of working mock frontend and integrated app. Backend restart persistence requires explicit execution evidence beyond a page refresh.

Contract/build: validate OpenAPI 3.1 and runtime endpoint coverage; run production frontend build. GitHub Actions must be inspected on the actual repository; a locally passing command does not prove hosted CI passes.

Defects: only create user-test-bug for an observed failure, with reproducible steps, expected/actual behavior and evidence. PM grooms; QA adds regression expectations; engineer fixes; independent QA reruns and closes only after PASS. All MVP and actual bug issues must be closed before submission; post-MVP remains open.
