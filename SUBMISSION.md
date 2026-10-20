# Submission readiness

Repository: https://github.com/Usmanovkairat/splitwise-pro

Product: SplitWise Pro, a local-first group expense manager with three split methods, precise integer balances, partial settlements and analytics. Separate from StudyFlow.

Status: implementation and principal integrated workflow verified; final route/accessibility regressions, hosted CI and final issue closure audit remain pending. This is not yet a final success claim.

| Requirement | Evidence |
|---|---|
| React/TypeScript frontend and mock iteration | Published `85172851`; independent `_docs/qa/mock-frontend.md` |
| OpenAPI 3.1 validation | Published `da0f6a65`; independent `_docs/qa/contract.md` PASS |
| In-memory FastAPI iteration | Published `0a2ae51c`; independent `_docs/qa/memory-backend.md` |
| SQLAlchemy/Alembic SQLite and restart persistence | Published `81d3af55`; independent `_docs/qa/sqlite.md` PASS |
| Integrated user workflows | Published `87881d4f`; rename fix `571fb77b` retested; route fix `72aa7592` published; final route/accessibility regressions pending |
| Automated suites and production build | Stage-specific executed results in QA reports; final full rerun pending |
| Independent browser QA and screenshots | `_docs/qa/integration.md`; `_docs/screenshots/integrated-desktop.png` and `integrated-mobile.png` |
| Actual hosted GitHub Actions result | Pending |
| Closed MVP and actual user-test-bug issue counts | Pending |
| Distinct chronological iteration commits | `_docs/iterations.md` records actual stages and bug-fix commits |

Final submission should include this public repository URL, installation commands from README, test evidence, screenshot paths and explicit remaining limitations. Do not submit as complete until final QA audits open MVP/bug issues and actual CI. Post-MVP CSV/authentication issues intentionally stay open. Brainstorming provenance is documented honestly in `chat-brainstorm.md`.
