# PM issue acceptance audit matrix

This is a PM traceability audit, **not an independent QA PASS declaration**. The “support” column cites existing independent QA records. A prior-stage PASS does not establish final integrated acceptance. Root/QA must compare current real issue criteria, commit and execution evidence before posting closure comments. #1/#3 were closed after the planning gate. Final suite, hosted CI and final open-issue audit remain pending at this revision.

| Issue | Acceptance mapping: implementation and checks | Existing independent support / remaining gate |
|---|---|---|
| #1 Scope/workflow | AGENTS.md; _docs/plan.md/process.md; team roles | planning.md records independent PASS; closed by root |
| #2 Bootstrap | README.md, Makefile, frontend/package.json, backend/requirements.txt, ignore rules | Final clean-install/run instructions and tracked-file audit pending |
| #3 Honest documentation | chat-brainstorm.md; architecture/design/role/plan documents | planning.md records independent PASS; closed by root |
| #4 Design/shell | frontend/src/App.tsx/styles.css; design-system.md; workflows.spec.ts mobile routes/screenshots | mock-frontend.md covers layout and #34; final integrated responsive/keyboard review pending |
| #5 Mock service | services/types.ts/mockService.ts; mockService.test.ts | mock-frontend.md principal workflow; bug-37.md frontend Unicode parity; final source review pending |
| #6 Dashboard | App.tsx overview; mock charts/activity; workflows and integration.spec.ts | Mock screenshots/principal flow verified; integrated currency/activity/error-state review pending |
| #7 Group create/rename | App.tsx forms; service methods; backend test_crud_and_isolation; browser create | Mock create tested; final integrated rename/currency/list checks pending |
| #8 Detail/delete group | Group detail; mockService cascade test; backend CRUD and transactional cascade | API/memory/SQLite support; final UI confirm/cancel check pending |
| #9 Members/protection | App member form; domain/service repositories; mock protection test; API CRUD/duplicate test | Memory/SQLite data checks; integrated referenced-removal and duplicate alert gate pending |
| #10 Expense/history | Expense form; schemas/service; test_crud_and_isolation; browser expense lifecycle | Mock and shared API support; integrated final workflow pending |
| #11 Edit/delete expense | App expense form/delete confirmation; CRUD tests; workflows.spec.ts | Mock edit/delete verified; final integrated recalc/confirm/cancel pending |
| #12 Equal rounding | domain.py and mockService; test_rounding/test_mathematical_invariants; mock rounding test | memory-backend.md independent invariant coverage; final integrated cents check pending |
| #13 Exact split | domain.py; schemas; invalid split tests; form validation and mock flow | Mock rejects mismatched total; API validation support; integrated parity pending |
| #14 Percent split | Integer basis-point domain allocation; mockService.test.ts; backend rounding | Mock/API percentage and stable sums supported; integrated final check pending |
| #15 Balances/suggestions | domain.py/service.py; math invariants; partial settlement tests | Memory independent zero-sum/suggestions support; integrated edit/delete settlement sequence pending |
| #16 Settlements | service validation; schemas; partial-settlement API test; browser lifecycle | Mock and shared API bounds support; integrated partial history/invalid repayment pending |
| #17 Analytics | Backend category/time/contribution aggregation; App charts; API test_partial_settlement_and_analytics | Memory and SQLite analytics support; integrated charts/totals/currency review pending |
| #18 Contract | openapi.yml; service types; openapi_spec_validator | contract.md independent source-contract PASS; final runtime conformance rerun pending |
| #19 Memory API | main.py/repository.py/service.py/schemas.py; test_memory.py | memory-backend.md independent PASS; separate #37 fix tracked |
| #20 ORM/boundary | models.py, database.py, sql_repository.py; shared API fixture | sqlite.md independent PASS for #20–22 |
| #21 Migration | migrations/versions/0001_initial_ledger.py; alembic.ini/env.py; migration roundtrip test | sqlite.md no metadata drift, downgrade/upgrade PASS |
| #22 SQLite transactions/restart | sql_repository.py; rollback/FK/actual_uvicorn_process_restart tests | sqlite.md independent atomicity/restart PASS; final integrated persistence pending |
| #23 Typed HTTP integration | services/index.ts and typed adapters/config; integration.spec.ts; development CORS | Integration implementation underway; independent integrated QA required |
| #24 Server validation/errors | schemas/service/repositories; invalid atomicity/filter tests; OpenAPI errors | Memory/SQLite invalid cases supported; #37 integrated parity and uniform UI error check pending |
| #25 Math tests | test_rounding; 250 randomized invariant cases; invalid splits; settlement conservation | memory-backend.md independent mathematical-foundation PASS |
| #26 API/persistence tests | Shared memory/SQLite acceptance fixture; test_persistence.py; rollback/restart | sqlite.md independent #26 PASS, 53 backend tests executed at that gate |
| #27 Frontend tests | App.test.tsx, mockService.test.ts; service rejection/form/name assertions | bugs-35-36.md and bug-37.md actual frontend checks; HTTP loading/error test and final rerun pending |
| #28 Browser E2E | workflows.spec.ts; integration.spec.ts; isolated api-server.py runner | Mock browser suite executed; integrated expense/settlement/refresh/mobile acceptance pending |
| #29 Responsive/accessibility | mobile-width route assertions; dialogs/alerts/focus; #34/#35 regressions | mock-frontend.md and bugs-35-36.md support; final integrated viewport/keyboard review pending |
| #30 Hosted CI | GitHub workflow; backend/frontend/build/OpenAPI commands | Actual GitHub Actions run/status must be inspected; currently pending |
| #31 Final acceptance | SUBMISSION.md; README commands; screenshots; all QA records; final issue audit | Pending final integrated suites/build/contract/CI and closure audit; do not close yet |
| #34 Mobile overflow bug | Positioned table scroll container; workflows.spec.ts eight-route width/actions test | mock-frontend.md independently records regression PASS; root handles final closure evidence |
| #35 Dialog error feedback bug | App mutation error handling; App.test.tsx; browser duplicate/corrected submission | bugs-35-36.md independent PASS; integrated duplicate check reinforced by #37 |
| #36 Local profile preference bug | App preference state/localStorage; App.test.tsx; browser save/navigation/reload | bugs-35-36.md independent PASS |
| #37 Member-name parity bug | Trim/casefold scoped uniqueness; memory/SQL/mock tests; unique constraint | bug-37.md memory/mock/SQLite-restart segments PASS; integrated dialog segment still pending |
| #38 Group rename payload bug | GroupForm and typed HTTP update projection; adapter and integrated group-management regression | Actual integrated rename422 reproduced; PM groomed; engineer fix and independent rerun pending |
| #39 Direct group route bug | Group context derived from requested route before fallback; async-route RTL and browser regression | Actual fresh non-first /groups/g2 rendered first group after5 seconds; PM groomed, fix/recheck pending |
| #40 Dialog return-focus bug | Dialog opener capture and Radix close-focus lifecycle; keyboard browser regression | Actual New group Enter/10Tab/Escape ended focus on body after5 seconds; PM groomed, fix/recheck pending |
| #41 Small-text contrast bug | Scoped semantic muted text colors on actual light/dark surfaces | Browser measured subtitle3.463 at11px; target>=4.5; PM groomed, correction/recheck pending |

## Closure checklist for root and independent QA

1. Fetch the real issue's latest acceptance criteria and ensure no later grooming changed the scope.
2. Identify the published implementation/fix commit and independent command/browser evidence. Do not infer hosted CI from local tests.
3. For UI/API features, require the integrated app checks after the HTTP adapter; mock-only results are stage evidence.
4. Post a QA comment naming exact criteria verified, commands/results, relevant screenshots and any limits. A clear scoped PASS permits root/QA to close; engineering self-approval does not.
5. Final audit must find all #1–31 MVP and actual bugs #34–41 closed with evidence. #32/#33 are intentionally open post-MVP. Report any remaining open MVP/bug explicitly.
6. Record actual test counts/CI status/limitations in SUBMISSION.md and README; remove pending entries only after the evidence exists.

No new feature, fabricated defect, unexecuted test or final PASS is introduced by this PM matrix.

## Latest independent integration evidence

Published integration commit: `87881d4fca6c88686f6de49b1fcae4838f876733`. `_docs/qa/integration.md` records actual SQLite-backed principal browser lifecycle PASS: group creation, three members, duplicate-name dialog, all three allocation methods and uneven rounding, expense edit/delete, partial repayment, zero-sum balances, analytics, refresh persistence and390px containment. `_docs/qa/bug-37.md` records the full name-uniqueness regression PASS across memory/mock/SQLite-restart/integrated UI. Extended loading/503/retry tests passed. Extended group-management acceptance found #38; therefore #7 and the broad final group-CRUD gate remain pending its independent fix verification. These observations update the earlier gate-specific “pending” cells above without implying final all-issue PASS.

## Actual remote status audit before final verification

On20 October2026 the PM fetched both pages of the live open-issues listing:28 MVP open (#2,#4–17,#19–31),2 actual bugs open (#37/#38),2 post-MVP open (#32/#33). MVP#1/#3/#18 and bugs#34–36 were already closed. This is a point-in-time audit, not the final closure count. Final status must be refreshed after QA and publication; no implementation issue was closed by this PM audit.

## Subsequent actual audit and route finding

PM fetched all39 actual issue bodies into `current-issue-criteria.md`, including individually fetched closed issues. At this later audit #37 was also closed; #38/#39,28 MVP and2 post-MVP remained open. Rename fix#38 was published at `571fb77b6f2cd8bcabadf8e1d014489f5f3fdb3f`; independent QA reported current backend54/OpenAPI OK, frontend22/build, five original mock tests and three integrated tests PASS. A new non-first direct group-route regression exposed #39. This supersedes earlier status counts without asserting final acceptance. QA must use current real criteria and current-source execution to determine closure.
