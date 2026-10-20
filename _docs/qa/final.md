# Independent final local acceptance

**Local runtime verdict: PASS.** The independent QA agent reran actual tests against the final engineer handoffs. Hosted CI, clean remote publication and final issue-state audit remain separate gates; no green CI or all-closed claim is made in this revision.

## Actual commands and results

| Command | Executed result |
|---|---|
| `.venv/bin/python -m pytest backend/tests -q` |54 passed in 6.81 s; includes actual Uvicorn process restart, isolated migrations, transactions / foreign keys and optional demo refusal. One upstream Starlette/httpx deprecation warning. |
| `.venv/bin/python -m openapi_spec_validator openapi.yml` |OK, exit 0. |
| `npm --prefix frontend test` |27 passed across 4 files in 5.82 s. |
| `npm --prefix frontend run build` |exit 0; 2,285 modules; 836.10 kB JavaScript / 254.20 kB gzip, nonfatal chunk size warning. |
| `QA_CHROMIUM_PATH=/tmp/chromium npx playwright test` from frontend |8 passed in 24.2 s: mock lifecycle, desktop / mobile, feedback / profile, eight-route containment, deep links / history, keyboard focus and contrast. |
| `QA_CHROMIUM_PATH=/tmp/chromium npx playwright test --config playwright.integration.config.ts` from frontend |3 passed in 19.2 s: real migrated SQLite workflows, group rename / description / reload, cancellation / confirmation / protection, and recoverable 503 / loading states. |
| `/tmp/splitwise-clean-lock/bin/python -m pip check` plus independent requirement/version comparison |No broken requirements; all 41 active locked packages match fresh interpreter; Windows-only Colorama pinned; Black excluded. DevOps separately ran 54 tests in this fresh environment. |

The final test-runner source is frozen after the above three-test integration rerun. The API browser fixture runs Uvicorn in the same Python process, avoiding orphan-child shutdown; temporary databases are migrated and isolated. Runtime provisioning and original failures remain in the earlier QA records. Test harness mistakes (premature asynchronous label lookup, a reused Response fixture, and an exact label omitting a dynamic badge) were corrected and are not represented as product bugs.

Additional independent actual API checks: both local Vite origins pass CORS preflight; a foreign origin is rejected with 400 and no allow-origin header; an exact zero share is accepted; zero, negative, fractional and boolean settlement amounts receive 422 without mutation; editing an expense from 1,001 to 900 minor units changes member balances to 600 / -300 / -300; recording all deterministic suggestions settles every balance to zero; settlements do not inflate spending; expense deletion resets spending and preserves the zero-sum ledger. All 19 required documents exist and are nonempty. These checks used a memory TestClient in addition to the common memory / SQLite suite.

Screenshots: `_docs/screenshots/mock-desktop.png`, `mock-mobile.png`, `integrated-desktop.png`, `integrated-mobile.png`. The real SQLite overview shows 11.00 after partial repayment. Screenshots are actual browser captures after chart animation.

## Acceptance criteria audit

QA read the actual live GitHub issue bodies preserved in `current-issue-criteria.md` and the PM-groomed #40 / #41 comments. PASS below applies to each listed criterion, with the evidence following it. Issues #2, #30 and #31 retain explicit remote/control gates. Post-MVP issues #32 / #33 remain intentionally open.

### Issue #1 — PASS

- **PASS:** Scope and role handoffs documented.
- **PASS:** Money rounding and settlement rules specified.

Evidence: Planning files and planning.md specify scope, separated agent handoffs, integer rounding and settlement bounds.

### Issue #2 — PENDING remote/control gate

- **PENDING remote/control gate:** Verify clean checkout installs through an executed acceptance check.
- **PENDING remote/control gate:** Verify local commands documented through an executed acceptance check.
- **PENDING remote/control gate:** Verify no StudyFlow changes through an executed acceptance check.

Evidence: All 41 active pinned packages match a fresh isolated Python installation, and pip check is clean. A clean remote checkout and npm installation must be confirmed from the hosted run before final closure.

### Issue #3 — PASS

- **PASS:** Verify required planning/role files exist through an executed acceptance check.
- **PASS:** Verify real excerpts distinguished from PM analysis through an executed acceptance check.

Evidence: All 19 required documents exist and are nonempty. User excerpts are explicitly distinguished from PM analysis; no invented dialogue is presented as history.

### Issue #4 — PASS

- **PASS:** Verify desktop sidebar/mobile navigation through an executed acceptance check.
- **PASS:** Verify visible focus through an executed acceptance check.
- **PASS:** Verify readable contrast through an executed acceptance check.
- **PASS:** Verify documented states through an executed acceptance check.

Evidence: Desktop and mobile screenshots, eight routes at 390 px, keyboard Enter / Tab / Escape, and sampled semantic text contrast from 5.345 to 7.044:1. Interaction states are documented.

### Issue #5 — PASS

- **PASS:** Verify typed async CRUD through an executed acceptance check.
- **PASS:** Verify deterministic seed through an executed acceptance check.
- **PASS:** Verify mock changes reflected through an executed acceptance check.
- **PASS:** Verify no API dependency through an executed acceptance check.

Evidence: Six mock service tests and eight independent browser tests execute deterministic seeded CRUD without an API server.

### Issue #6 — PASS

- **PASS:** Verify currency totals kept separate through an executed acceptance check.
- **PASS:** Verify activity links through an executed acceptance check.
- **PASS:** Verify loading/error/empty states through an executed acceptance check.

Evidence: Actual mock and SQLite dashboard screenshots; group-scoped queries preserve currency context. Loading, empty onboarding, a 503 alert and Try again recovery were exercised.

### Issue #7 — PASS

- **PASS:** Verify create/rename persist in service through an executed acceptance check.
- **PASS:** Verify required name/currency through an executed acceptance check.
- **PASS:** Verify navigable list through an executed acceptance check.

Evidence: Actual KZT group creation, name and description rename through PUT, immutable currency, refresh retention and list navigation. Adapter and form payload regressions pass.

### Issue #8 — PASS

- **PASS:** Verify cancel preserves data through an executed acceptance check.
- **PASS:** Verify confirm removes group and descendants through an executed acceptance check.
- **PASS:** Verify empty detail state through an executed acceptance check.

Evidence: Actual group detail and empty-member state; cancellation and confirmed deletion; list absence afterwards. Shared API tests cover descendant cascades and rollback.

### Issue #9 — PASS

- **PASS:** Verify names validated through an executed acceptance check.
- **PASS:** Verify payer/share/settlement references block removal through an executed acceptance check.
- **PASS:** Verify clear errors through an executed acceptance check.

Evidence: Actual add / remove / cancel and referenced-member rejection with an alert. Unicode casefold uniqueness is tested atomically across memory, SQLite and mock services.

### Issue #10 — PASS

- **PASS:** Verify group members only through an executed acceptance check.
- **PASS:** Verify valid date/category through an executed acceptance check.
- **PASS:** Verify participant selection through an executed acceptance check.
- **PASS:** Verify sorted history through an executed acceptance check.

Evidence: Real expenses exercise payer, category, date, participants and all split methods. Shared API tests reject foreign members and invalid dates, and verify history filters.

### Issue #11 — PASS

- **PASS:** Verify edits recalculate balances through an executed acceptance check.
- **PASS:** Verify cancel deletion safe through an executed acceptance check.
- **PASS:** Verify deletion updates all summaries through an executed acceptance check.

Evidence: The real browser checks editing, deletion cancellation and confirmed deletion. An additional API check changes 1,001 to 900 minor units, verifies balances 600 / -300 / -300, then verifies deletion resets spending and preserves zero-sum balances.

### Issue #12 — PASS

- **PASS:** Verify shares sum to amount through an executed acceptance check.
- **PASS:** Verify 100 cents/3 yields deterministic 34/33/33 through an executed acceptance check.
- **PASS:** Verify no float money through an executed acceptance check.

Evidence: Actual API shares for 100 minor units among three members are 33 / 33 / 34. Stable-ID tie tests and 250 seeded randomized allocation cases preserve integer totals.

### Issue #13 — PASS

- **PASS:** Verify reject sum mismatch/negative/duplicate/nonmember through an executed acceptance check.
- **PASS:** Verify support zero shares through an executed acceptance check.

Evidence: The browser rejects a mismatched exact total and accepts correction. API checks cover invalid amounts and members; a separate executed zero-share case yields 0 / 100. Participant record keys are unique.

### Issue #14 — PASS

- **PASS:** Verify percentages sum 100% through an executed acceptance check.
- **PASS:** Verify max 2 decimals through an executed acceptance check.
- **PASS:** Verify exact cent sum through an executed acceptance check.
- **PASS:** Verify deterministic ID ties through an executed acceptance check.

Evidence: The browser records a 10.00 expense at 50 / 25 / 25 percent. Integer basis points, invalid totals and fractional basis points are checked; deterministic allocation preserves the cent total.

### Issue #15 — PASS

- **PASS:** Verify net sum zero through an executed acceptance check.
- **PASS:** Verify deterministic sorted pairing through an executed acceptance check.
- **PASS:** Verify suggestions settle all outstanding debt through an executed acceptance check.

Evidence: Additional API checks verify recalculation after an amount edit, repeated deterministic suggestions, and complete settlement of every suggested debt to zero. Partial repayment and deletion preserve conservation.

### Issue #16 — PASS

- **PASS:** Verify positive integer amount through an executed acceptance check.
- **PASS:** Verify distinct members through an executed acceptance check.
- **PASS:** Verify debtor negative/creditor positive through an executed acceptance check.
- **PASS:** Verify reject overpayment through an executed acceptance check.

Evidence: Actual partial Bob-to-Alice repayment of 100 minor units appears in history after refresh. API checks reject overpayment, reverse direction, self-transfer, foreign members and invalid numeric values without mutation.

### Issue #17 — PASS

- **PASS:** Verify settlement excluded from spending through an executed acceptance check.
- **PASS:** Verify each currency separated through an executed acceptance check.
- **PASS:** Verify useful charts and empty states through an executed acceptance check.

Evidence: Real SQLite analytics show 1,100 minor units after a partial settlement. Category, timeline and contribution assertions pass; settlements are excluded from spending and currency remains group-scoped.

### Issue #18 — PASS

- **PASS:** Verify all frontend operations described through an executed acceptance check.
- **PASS:** Verify schemas/examples/errors/filters through an executed acceptance check.
- **PASS:** Verify validation command succeeds through an executed acceptance check.

Evidence: The source OpenAPI validator passes. Frontend service methods and API routes were reviewed against the contract; the contract QA record covers 16 operations and 13 response-schema checks.

### Issue #19 — PASS

- **PASS:** Verify health and MVP routes through an executed acceptance check.
- **PASS:** Verify injectable memory repository through an executed acceptance check.
- **PASS:** Verify testClient success/validation cases through an executed acceptance check.

Evidence: Memory mode remains available. The common 54-test suite exercises CRUD, validation and membership rules in both memory and migrated SQLite repositories.

### Issue #20 — PASS

- **PASS:** Verify sQLAlchemy 2 models through an executed acceptance check.
- **PASS:** Verify integer money through an executed acceptance check.
- **PASS:** Verify foreign keys through an executed acceptance check.
- **PASS:** Verify matching repository interface through an executed acceptance check.

Evidence: Normalized group, member, expense, share and settlement ORM models were reviewed; the shared API suite, foreign-key failure checks and repository-boundary tests pass.

### Issue #21 — PASS

- **PASS:** Verify upgrade fresh database through an executed acceptance check.
- **PASS:** Verify downgrade/upgrade verified through an executed acceptance check.
- **PASS:** Verify fK enabled through an executed acceptance check.
- **PASS:** Verify databases ignored through an executed acceptance check.

Evidence: Migration upgrade / downgrade, metadata parity and fresh temporary databases are executed by the passing backend suite.

### Issue #22 — PASS

- **PASS:** Verify atomic expenses/shares through an executed acceptance check.
- **PASS:** Verify isolated tests through an executed acceptance check.
- **PASS:** Verify restart preserves data through an executed acceptance check.
- **PASS:** Verify relationship protection through an executed acceptance check.

Evidence: The suite actually stops and restarts Uvicorn and checks retained ledger data. Failed share and group-delete transactions roll back; foreign keys and isolated databases are tested.

### Issue #23 — PASS

- **PASS:** Verify real API default through an executed acceptance check.
- **PASS:** Verify mock mode retained through an executed acceptance check.
- **PASS:** Verify invalidation/loading/errors through an executed acceptance check.
- **PASS:** Verify configured local origins through an executed acceptance check.

Evidence: Default API and explicit mock modes both execute in browser suites. Loading, invalidation and 503 recovery are covered. Both local CORS origins pass preflight; a foreign origin is rejected.

### Issue #24 — PASS

- **PASS:** Verify 404 unknown resource through an executed acceptance check.
- **PASS:** Verify 422 malformed input through an executed acceptance check.
- **PASS:** Verify conflict responses through an executed acceptance check.
- **PASS:** Verify no stack leaks through an executed acceptance check.

Evidence: API tests and extra requests confirm 404, 422 and 409 string-detail responses, strict input rules and atomic failure without stack-trace responses. Active-dialog alerts work in the browser.

### Issue #25 — PASS

- **PASS:** Verify all split methods tested through an executed acceptance check.
- **PASS:** Verify tie cases through an executed acceptance check.
- **PASS:** Verify net sum zero through an executed acceptance check.
- **PASS:** Verify settlement conservation through an executed acceptance check.
- **PASS:** Verify invalid inputs through an executed acceptance check.

Evidence: All split methods, stable ties and 250 seeded randomized allocation cases pass. Additional API execution records all suggested settlements and reaches zero balances.

### Issue #26 — PASS

- **PASS:** Verify create/edit/delete/group cascade through an executed acceptance check.
- **PASS:** Verify rollback through an executed acceptance check.
- **PASS:** Verify invalid member references through an executed acceptance check.
- **PASS:** Verify restart verified through an executed acceptance check.

Evidence: All 54 backend tests pass, including shared repository CRUD, cascade, rollback, foreign members and an actual backend process restart.

### Issue #27 — PASS

- **PASS:** Verify validation prevents bad submit through an executed acceptance check.
- **PASS:** Verify mock operations through an executed acceptance check.
- **PASS:** Verify aPI error/loading rendering through an executed acceptance check.
- **PASS:** Verify tests execute through an executed acceptance check.

Evidence: All 27 frontend tests pass across four files, covering forms, exact validation, mock casefold rules, HTTP adapter behavior, loading / error / retry and dialog focus.

### Issue #28 — PASS

- **PASS:** Verify create group/members through an executed acceptance check.
- **PASS:** Verify all split modes through an executed acceptance check.
- **PASS:** Verify edit/delete through an executed acceptance check.
- **PASS:** Verify partial settlement through an executed acceptance check.
- **PASS:** Verify refresh through an executed acceptance check.
- **PASS:** Verify assertions through an executed acceptance check.

Evidence: The real SQLite suite passes three tests in 19.2 s: groups, members, splits, editing, cancellation / deletion, partial repayment, refresh, invariants and mobile layout. The mock suite passes eight tests in 24.2 s.

### Issue #29 — PASS

- **PASS:** Verify no horizontal overflow through an executed acceptance check.
- **PASS:** Verify labeled forms through an executed acceptance check.
- **PASS:** Verify focusable controls through an executed acceptance check.
- **PASS:** Verify dialog escape/focus behavior through an executed acceptance check.

Evidence: Eight routes fit a 390 px viewport. Accessible table actions remain available through internal scrolling. Labels, initial focus, ten Tab steps, Escape and focus return are checked; RTL also covers a removed opener.

### Issue #30 — PENDING remote/control gate

- **PENDING remote/control gate:** Verify workflow installs pinned dependencies through an executed acceptance check.
- **PENDING remote/control gate:** Verify validates OpenAPI through an executed acceptance check.
- **PENDING remote/control gate:** Verify real run checked before final pass through an executed acceptance check.

Evidence: The workflow installs the exact Python graph and npm lock, then runs contract, backend, frontend, build and both browser suites. The full actual hosted conclusion remains a separate acceptance gate.

### Issue #31 — PENDING remote/control gate

- **PENDING remote/control gate:** Verify exact commands/results and screenshots recorded through an executed acceptance check.
- **PENDING remote/control gate:** Verify issues audited through an executed acceptance check.
- **PENDING remote/control gate:** Verify limitations explicit through an executed acceptance check.

Evidence: This report records actual commands, results, screenshots and criterion mappings. Final submission metadata, issue states and full hosted CI must be checked before overall closure.

### Issue #34 — PASS

- **PASS:** At 390px document.scrollWidth <= viewport width on all main screens.
- **PASS:** Navigation and expense forms remain reachable.
- **PASS:** Desktop layout retains readable charts and table.

Evidence: The original 498 px overflow at a 390 px viewport was reproduced. The scoped positioning fix passes eight-route width, internal table scrolling and accessible action checks.

### Issue #35 — PASS

- **PASS:** Duplicate member failure shows visible error styling and text.
- **PASS:** Error is announced inside the active dialog via role alert.
- **PASS:** Successful mutations retain success feedback.

Evidence: A duplicate-member error is exposed as an alert inside the active dialog; input is preserved and correction succeeds. Mock and integrated browser regressions pass.

### Issue #36 — PASS

- **PASS:** Saved display name updates the sidebar profile.
- **PASS:** It remains after page refresh.
- **PASS:** Empty names show validation and retain last valid value.

Evidence: Saving QA Person updates the profile and initials immediately and survives navigation and reload. Whitespace cannot replace a valid preference.

### Issue #37 — PASS

- **PASS:** Same-group trimmed casefold duplicate names return422 and do not add a row.
- **PASS:** Distinct groups may each have member Alice.
- **PASS:** Memory and SQLite repositories enforce equivalent behavior.
- **PASS:** Integrated UI shows duplicate failure inside member dialog.

Evidence: Trimmed Unicode casefold duplicates receive 422 without mutation, while other groups may reuse a name. Memory, SQLite, mock, engine restart and integrated dialog checks all pass.

### Issue #38 — PASS

- **PASS:** Rename updates group heading and list through real SQLite API.
- **PASS:** Description changes persist after refresh.
- **PASS:** Update request contains name and description only; currency remains immutable.
- **PASS:** Creation still sends selected currency.

Evidence: The real KZT group retains renamed name, description and currency after refresh. Both form and adapter omit currency from update payloads while creation retains it.

### Issue #39 — PASS

- **PASS:** Fresh direct /groups/g2 renders The apartment and matching details.
- **PASS:** Reload and back/forward keep URL and selected group consistent.
- **PASS:** Group selector on detail page updates URL and group together.
- **PASS:** Missing/deleted group gracefully falls back without redirect loops.

Evidence: Actual non-first direct link, reload, selector URL, browser Back / Forward and missing-group fallback pass. RTL covers an empty workspace; SQLite browser refresh uses real dynamic IDs.

### Issue #40 — PASS

- **PASS:** Escape/cancel/close restore the actual connected visible opener.
- **PASS:** Mutation closure restores a surviving control or sensible visible fallback if opener disappeared.
- **PASS:** Initial focus and Tab containment are preserved.

Evidence: Actual keyboard opening sets initial focus, ten Tab presses remain trapped, and Escape returns focus to the opener. Two RTL tests cover Escape / Close / Save and a disconnected opener.

### Issue #41 — PASS

- **PASS:** Small semantic subtitle/stat/detail/sidebar text reaches4.5:1 against actual surface.
- **PASS:** Essential labels, hierarchy, layout and palette remain present; no hiding of low-contrast text.

Evidence: Measured subtitle contrast is 5.345:1; card labels / details 5.701; table headers 5.489; sidebar / profile 6.200–7.044; dialog description 5.701. Every sampled small semantic label exceeds 4.5:1; no comprehensive WCAG certification is claimed.

## Practical limits

The application uses one local workspace and one backend worker, with no authentication, real payments or cloud hosting. All supported currencies have two decimal places; groups do not convert currencies. Settlement suggestions are deterministic and do not guarantee a globally minimum transfer count. The frontend bundle-size warning and upstream test-client deprecation warning do not fail the checks. Keyboard, mobile and key semantic text contrast were tested; this is not certification against every WCAG criterion. The optional demo command is explicit and refuses an existing workspace. StudyFlow was not modified; all writes target this new repository.

Final root publication must record the source commit, actual GitHub Actions conclusion and issue closure counts before marking the submission complete.
