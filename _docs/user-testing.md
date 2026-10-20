# Independent user-workflow verification

The reports in `_docs/qa/` distinguish actual independent execution from engineer checks. Final acceptance remains pending current-source route/accessibility regressions, hosted CI and final issue audit at this revision.

| Gate | Actual independent evidence | Result |
|---|---|---|
| Planning and role separation | `qa/planning.md`, actual GitHub criteria and documents reviewed | PASS |
| Mock frontend | `qa/mock-frontend.md`, principal lifecycle and mobile routes; screenshots | PASS for tested workflows after #34; later defects tracked separately |
| Source contract | `qa/contract.md`, validator exit 0 and service operation/schema mapping | PASS |
| Memory backend | `qa/memory-backend.md`, 26 pytest and 13 response-schema checks | PASS foundation; duplicate drift separately fixed as #37 |
| SQLite/Alembic | `qa/sqlite.md`, 53 pytest, migration roundtrip, FK/rollback and actual Uvicorn restart | PASS |
| Modal error and profile fixes | `qa/bugs-35-36.md`, 5 Playwright tests passed 15.3s | PASS |
| Name uniqueness | `qa/bug-37.md`, memory/mock/SQLite-restart/integrated duplicate-dialog checks | PASS all groomed segments |
| Real API principal lifecycle | `qa/integration.md`, 1 Playwright workflow passed 6.9s/10.3s total against migrated temporary SQLite | PASS |
| Extended loading/error recovery | `qa/integration.md`, delayed loading and 503 → Try again → live recovery | PASS |
| Extended group management | Real KZT rename initially returned422; fix571fb77b projects fields; QA subsequently reported3 integrated tests PASS | PASS reported after fix; final current-source review remains |
| Non-first group direct links | Fresh /groups/g2 rendered first group after5 seconds | FAIL #39; PM groomed, fix/rerun pending |
| Optional demo population | Integration report reran 54 backend tests including seed/refusal | PASS explicit optional seed; no automatic population |
| Hosted CI and final closure audit | Actual remote result and open issue listing required | Pending |

## Verified real-API journey

The browser created Integrated QA trip, added Alice/Bob/Carol and submitted padded ALICE to confirm the active-dialog duplicate alert and preserved input. It recorded equal 1.00, exact 3.00 with 1/1/1 and percentage 10.00 with 50/25/25. API assertions verified shares sum to each expense and uneven-dollar shares are 33/33/34. It edited the percentage expense, confirmed exact-expense deletion, recorded a partial Bob→Alice 1.00 repayment, checked zero-sum balances and analytics 1100 minor units, then refreshed and retained the real settlement row. Overview screenshots show 11.00. Desktop 1440px and mobile 390px screenshots were captured after chart animation; mobile width stayed within 390px and no browser JavaScript errors occurred.

Screenshots: `_docs/screenshots/integrated-desktop.png`, `_docs/screenshots/integrated-mobile.png`; initial mock counterparts are preserved too. The API fixture migrates and removes its own temporary database. Backend persistence testing explicitly terminates and restarts Uvicorn against the same database; a page refresh alone is not presented as restart evidence.

## Actual defect lifecycle

- #34: stable 390px page overflowed to 498px. PM groomed; engineer positioned the table scroll container; QA checked eight routes, reachable actions and preserved desktop. Fix published and closed.
- #35: duplicate-member failure appeared as a green success check outside the modal accessibility tree. PM groomed; engineer added an active-dialog alert; QA verified preserved input, correction and success. Fix published and closed.
- #36: saved local name left the sidebar unchanged. PM groomed; engineer applied local state/storage; QA verified profile/initials, refresh and invalid-name retention. Fix published and closed.
- #37: memory API accepted Alice/alice while mock rejected. PM groomed casefold uniqueness per group; memory/mock/SQLite-restart/integrated regressions independently passed. Final remote closure pending.
- #38: integrated group rename sent immutable currency and failed422. Fix `571fb77b6f2cd8bcabadf8e1d014489f5f3fdb3f` projects update fields while preserving strict backend/OpenAPI. Independent QA reported three integrated tests PASS after the fix; final report/closure follows current-source review.
- #39: fresh non-first direct group URL rendered the first group's data even after5 seconds. PM groomed URL precedence, reload/history/picker and missing/deleted fallback; engineer fix and independent regression pending.
- #40: keyboard New group Enter/10Tab/Escape closed the dialog but left focus on body after5 seconds. Existing return-focus requirement; PM groomed opener restoration and safe surviving-control fallback without weakening focus containment.
- #41: actual subtitle text rgb(124,136,127) on rgb(247,248,244) at11px measured contrast3.463. Existing AA requirement; PM groomed semantic subtitle/stat/detail/sidebar text>=4.5, preserving design and content.

## Remaining final gate

QA must rerun current frontend/backend/browser suites, build and contract validation, verify final criteria including group/member deletion and keyboard behavior, inspect actual hosted CI, then authorize issue closure. Final audit must find all31 MVP and all8 actual bug issues closed;2 post-MVP issues intentionally remain open. The user deadline is approximately12:33 Asia/Qyzylorda on20 October2026, inferred from the user's10-hour deadline at02:33. Actual GitHub timestamps remain authoritative.
