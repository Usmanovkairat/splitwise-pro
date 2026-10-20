# Iteration execution ledger

This ledger records published chronological commits supplied by the orchestrator and cites independent QA records separately. A published stage is not a claim of full final acceptance.

| Order | Stage / publication | Commit | Independent evidence |
|---|---|---|---|
| 0 | Planning and real issue backlog | `d23aa034` | `_docs/qa/planning.md`: #1/#3 planning PASS |
| 1 | Frontend with deterministic mockService | `8517285123a9b5da141cff52fa371c5f9786fe1f` | `_docs/qa/mock-frontend.md`: actual browser runs; real #34–36 identified |
| 2 | Source OpenAPI contract | `da0f6a65` | `_docs/qa/contract.md`: validator exit0 and frontend service coverage PASS |
| 3 | Scoped mobile overflow fix #34 | `02eb73c4` | `_docs/qa/mock-frontend.md`: eight-route containment/actions regression PASS |
| 4 | In-memory FastAPI backend | `0a2ae51c` | `_docs/qa/memory-backend.md`: 26 tests and 13 independent response validations; actual #37 tracked |
| 5 | Scoped modal feedback/profile fixes #35/#36 | `e53dbd72` | `_docs/qa/bugs-35-36.md`: actual5-test browser rerun PASS |
| 6 | Scoped name uniqueness fix #37 | `f2f0d081` | `_docs/qa/bug-37.md`: independent memory segment PASS |
| 7 | Name parity regression tests | `f002a3f8` | `_docs/qa/bug-37.md`: frontend10 tests; memory27 tests at those gates |
| 8 | SQLAlchemy/Alembic SQLite persistence | `81d3af55` | `_docs/qa/sqlite.md`:53 tests, migration/rollback/FK/restart PASS |
| 9 | Typed HTTP integration | `87881d4fca6c88686f6de49b1fcae4838f876733` | `_docs/qa/integration.md`: real SQLite principal lifecycle and #37 integrated segment PASS; extended group management found real #38 |
| 10 | Group rename payload fix #38 | `571fb77b6f2cd8bcabadf8e1d014489f5f3fdb3f` | Engineer regressions and independent integrated group-management rerun; later direct-link check found real #39 |
| 11 | Requested group route fix #39 | `72aa759275c653722b201941492309268de185e4` | Direct/reload mock regression PASS; final API-mode route checks pending |
| 12 | Final verification and delivery | Pending | Final all-suite/build/contract/hosted CI/issue audit pending |

## Methodology reconciliation
The two references emphasize complementary stages: specification/role separation and frontend-first incremental delivery. Where ordering could differ, the explicit master assignment governs: planning → frontend with mockService → OpenAPI → memory API → SQLAlchemy/Alembic SQLite → frontend/backend integration → final testing. Therefore SQLite was deliberately implemented and independently verified before enabling the real HTTP frontend. No stage is retroactively invented, squashed or reordered to imply earlier work. Scoped real bug-fix commits appear where failures were actually found.

## Evidence limits
Independent reports contain exact executed commands, counts, screenshots and observed failures. The SQLite gate reports53 backend tests; the later integration report records54 tests including explicit demo-seed refusal. These are gate-specific results, not a final all-checks claim. #37 now has independent memory/mock/SQLite-restart/integrated PASS. The principal real-API browser workflow passed, while extended group management exposed #38 (rename payload includes immutable currency), which remains a separate pending fix/QA gate. Final hosted GitHub Actions result and final issue closure must be checked directly. See `_docs/qa/issue-matrix.md` for PM traceability and remaining gates; that matrix is not independent QA approval.
