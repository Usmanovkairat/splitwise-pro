# Current real GitHub issue criteria

Fetched live by PM for independent QA review; these are actual current issue bodies, not the PM traceability matrix. State is a point-in-time snapshot. Actual service timestamps in GitHub remain authoritative. Closed issue bodies were individually fetched as well as both open-list pages.

## Issue #1: Plan MVP scope and AI-native delivery workflow

State: closed; labels: mvp

## Goal
Define the shared expense MVP before implementation.
## Description
Plan frontend mock, OpenAPI, memory API, SQLite and integration iterations.
## Acceptance Criteria
- [ ] Scope and role handoffs documented.
- [ ] Money rounding and settlement rules specified.
## Out of Scope
Authentication and real transfers.
## Constraints
React, FastAPI, SQLAlchemy; genuine evidence only.
## Dependencies
None.
## Test Expectations
QA checks planning documents against assignment.

---

## Issue #2: Bootstrap repository and reproducible development commands

State: open; labels: mvp

## Goal
Bootstrap repository and reproducible development commands

## Description
Provide clean frontend/backend layouts, ignored databases/secrets and setup commands.

## Acceptance Criteria
- [ ] Verify clean checkout installs through an executed acceptance check.
- [ ] Verify local commands documented through an executed acceptance check.
- [ ] Verify no StudyFlow changes through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#1 (approved scope).

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #3: Document honest brainstorm, scope and team handoffs

State: closed; labels: mvp

## Goal
Document honest brainstorm, scope and team handoffs

## Description
Record actual user selection and PM product decisions without invented conversation.

## Acceptance Criteria
- [ ] Verify required planning/role files exist through an executed acceptance check.
- [ ] Verify real excerpts distinguished from PM analysis through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#1; user attachment and actual conversation.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #4: Define fintech visual system and accessible responsive shell

State: open; labels: mvp

## Goal
Define fintech visual system and accessible responsive shell

## Description
Implement detailed tokens and navigation inspired by Linear, Ramp and Mercury.

## Acceptance Criteria
- [ ] Verify desktop sidebar/mobile navigation through an executed acceptance check.
- [ ] Verify visible focus through an executed acceptance check.
- [ ] Verify readable contrast through an executed acceptance check.
- [ ] Verify documented states through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#3 (design specification).

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

PM detail: verify desktop and 390px navigation, labels, visible focus, contrast and loading/empty/error/success variants against `_docs/design-system.md`.

---

## Issue #5: Build typed mockService with deterministic demonstration data

State: open; labels: mvp

## Goal
Build typed mockService with deterministic demonstration data

## Description
Frontend-first repository for groups, members, expenses, balances and settlements.

## Acceptance Criteria
- [ ] Verify typed async CRUD through an executed acceptance check.
- [ ] Verify deterministic seed through an executed acceptance check.
- [ ] Verify mock changes reflected through an executed acceptance check.
- [ ] Verify no API dependency through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#4 (shared types and UI shell).

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #6: Build workspace dashboard and recent activity

State: open; labels: mvp

## Goal
Build workspace dashboard and recent activity

## Description
Provide spending overview with group-aware totals and recent changes.

## Acceptance Criteria
- [ ] Verify currency totals kept separate through an executed acceptance check.
- [ ] Verify activity links through an executed acceptance check.
- [ ] Verify loading/error/empty states through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#5.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #7: Implement group list, creation and rename

State: open; labels: mvp

## Goal
Implement group list, creation and rename

## Description
Support named groups in KZT, USD, EUR or GBP with one currency each.

## Acceptance Criteria
- [ ] Verify create/rename persist in service through an executed acceptance check.
- [ ] Verify required name/currency through an executed acceptance check.
- [ ] Verify navigable list through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#5.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #8: Implement group detail and confirmed cascade deletion

State: open; labels: mvp

## Goal
Implement group detail and confirmed cascade deletion

## Description
Show group summary and expenses; remove group only after explicit confirmation.

## Acceptance Criteria
- [ ] Verify cancel preserves data through an executed acceptance check.
- [ ] Verify confirm removes group and descendants through an executed acceptance check.
- [ ] Verify empty detail state through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#7.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #9: Implement member lifecycle and reference protection

State: open; labels: mvp

## Goal
Implement member lifecycle and reference protection

## Description
Add members with unique stable IDs and remove only unreferenced members.

## Acceptance Criteria
- [ ] Verify names validated through an executed acceptance check.
- [ ] Verify payer/share/settlement references block removal through an executed acceptance check.
- [ ] Verify clear errors through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#7.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #10: Implement expense create and history

State: open; labels: mvp

## Goal
Implement expense create and history

## Description
Capture description, positive amount, payer, category, date and participants.

## Acceptance Criteria
- [ ] Verify group members only through an executed acceptance check.
- [ ] Verify valid date/category through an executed acceptance check.
- [ ] Verify participant selection through an executed acceptance check.
- [ ] Verify sorted history through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#9.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #11: Implement expense edit and confirmed deletion

State: open; labels: mvp

## Goal
Implement expense edit and confirmed deletion

## Description
Allow correcting recorded expenses and deleting them safely.

## Acceptance Criteria
- [ ] Verify edits recalculate balances through an executed acceptance check.
- [ ] Verify cancel deletion safe through an executed acceptance check.
- [ ] Verify deletion updates all summaries through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#10.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #12: Implement equal splitting and deterministic cent rounding

State: open; labels: mvp

## Goal
Implement equal splitting and deterministic cent rounding

## Description
Allocate integer minor units with largest remainder and stable member-ID tie breaks.

## Acceptance Criteria
- [ ] Verify shares sum to amount through an executed acceptance check.
- [ ] Verify 100 cents/3 yields deterministic 34/33/33 through an executed acceptance check.
- [ ] Verify no float money through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#10.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #13: Implement exact amount splitting

State: open; labels: mvp

## Goal
Implement exact amount splitting

## Description
Allocate nonnegative per-participant integer shares with exact total.

## Acceptance Criteria
- [ ] Verify reject sum mismatch/negative/duplicate/nonmember through an executed acceptance check.
- [ ] Verify support zero shares through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#10.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #14: Implement percentage splitting

State: open; labels: mvp

## Goal
Implement percentage splitting

## Description
Accept decimal percentages with integer basis points and largest remainder.

## Acceptance Criteria
- [ ] Verify percentages sum 100% through an executed acceptance check.
- [ ] Verify max 2 decimals through an executed acceptance check.
- [ ] Verify exact cent sum through an executed acceptance check.
- [ ] Verify deterministic ID ties through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#10.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #15: Implement balances and simplified settlement suggestions

State: open; labels: mvp

## Goal
Implement balances and simplified settlement suggestions

## Description
Compute paid, owed, settled and net values plus deterministic debt-credit suggestions.

## Acceptance Criteria
- [ ] Verify net sum zero through an executed acceptance check.
- [ ] Verify deterministic sorted pairing through an executed acceptance check.
- [ ] Verify suggestions settle all outstanding debt through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#12, #13, #14.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

PM detail: net = paid − owed + sent − received; assert zero-sum balances after expense edit/delete and partial repayment; stable member-ID ordering defines deterministic suggestions.

---

## Issue #16: Implement partial settlements and history

State: open; labels: mvp

## Goal
Implement partial settlements and history

## Description
Record debt-to-credit transfers bounded by both outstanding balances.

## Acceptance Criteria
- [ ] Verify positive integer amount through an executed acceptance check.
- [ ] Verify distinct members through an executed acceptance check.
- [ ] Verify debtor negative/creditor positive through an executed acceptance check.
- [ ] Verify reject overpayment through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#15.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

PM detail: reject nonpositive/noninteger, self-transfer, foreign group members, non-debtor sender, non-creditor receiver and amount exceeding either current outstanding amount. Record date/note and recompute balances.

---

## Issue #17: Build category, timeline and contribution analytics

State: open; labels: mvp

## Goal
Build category, timeline and contribution analytics

## Description
Present expense totals/categories/dates/contributions and outstanding balances.

## Acceptance Criteria
- [ ] Verify settlement excluded from spending through an executed acceptance check.
- [ ] Verify each currency separated through an executed acceptance check.
- [ ] Verify useful charts and empty states through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#15.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #18: Specify and validate complete OpenAPI 3.1 contract

State: closed; labels: mvp

## Goal
Specify and validate complete OpenAPI 3.1 contract

## Description
Publish openapi.yml after frontend mock iteration and before backend.

## Acceptance Criteria
- [ ] Verify all frontend operations described through an executed acceptance check.
- [ ] Verify schemas/examples/errors/filters through an executed acceptance check.
- [ ] Verify validation command succeeds through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#5–#17 mock frontend handoff.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #19: Implement FastAPI application with in-memory repositories

State: open; labels: mvp

## Goal
Implement FastAPI application with in-memory repositories

## Description
Deliver contract-aligned API independently of SQLite.

## Acceptance Criteria
- [ ] Verify health and MVP routes through an executed acceptance check.
- [ ] Verify injectable memory repository through an executed acceptance check.
- [ ] Verify testClient success/validation cases through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#18 validated contract.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #20: Define SQLAlchemy models and repository boundary

State: open; labels: mvp

## Goal
Define SQLAlchemy models and repository boundary

## Description
Persist group/member/expense/share/settlement relationships portably.

## Acceptance Criteria
- [ ] Verify sQLAlchemy 2 models through an executed acceptance check.
- [ ] Verify integer money through an executed acceptance check.
- [ ] Verify foreign keys through an executed acceptance check.
- [ ] Verify matching repository interface through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#19 memory repository behavior.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #21: Add Alembic initial migration and SQLite configuration

State: open; labels: mvp

## Goal
Add Alembic initial migration and SQLite configuration

## Description
Provide reproducible schema initialization and SQLite transaction configuration.

## Acceptance Criteria
- [ ] Verify upgrade fresh database through an executed acceptance check.
- [ ] Verify downgrade/upgrade verified through an executed acceptance check.
- [ ] Verify fK enabled through an executed acceptance check.
- [ ] Verify databases ignored through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#20 models.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #22: Implement transactional SQLite repositories and restart persistence

State: open; labels: mvp

## Goal
Implement transactional SQLite repositories and restart persistence

## Description
Replace memory storage through configuration without changing API behavior.

## Acceptance Criteria
- [ ] Verify atomic expenses/shares through an executed acceptance check.
- [ ] Verify isolated tests through an executed acceptance check.
- [ ] Verify restart preserves data through an executed acceptance check.
- [ ] Verify relationship protection through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#20, #21.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #23: Integrate typed HTTP service and development CORS

State: open; labels: mvp

## Goal
Integrate typed HTTP service and development CORS

## Description
Connect completed frontend screens to backend with selectable service mode.

## Acceptance Criteria
- [ ] Verify real API default through an executed acceptance check.
- [ ] Verify mock mode retained through an executed acceptance check.
- [ ] Verify invalidation/loading/errors through an executed acceptance check.
- [ ] Verify configured local origins through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#18, #22 and mock frontend acceptance.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #24: Enforce backend validation and uniform API error handling

State: open; labels: mvp

## Goal
Enforce backend validation and uniform API error handling

## Description
Protect all money, membership and resource constraints server-side.

## Acceptance Criteria
- [ ] Verify 404 unknown resource through an executed acceptance check.
- [ ] Verify 422 malformed input through an executed acceptance check.
- [ ] Verify conflict responses through an executed acceptance check.
- [ ] Verify no stack leaks through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#18, #19; apply equally to #22.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #25: Add mathematical invariant and edge-case unit tests

State: open; labels: mvp

## Goal
Add mathematical invariant and edge-case unit tests

## Description
Independently exercise splits, balances and settlements.

## Acceptance Criteria
- [ ] Verify all split methods tested through an executed acceptance check.
- [ ] Verify tie cases through an executed acceptance check.
- [ ] Verify net sum zero through an executed acceptance check.
- [ ] Verify settlement conservation through an executed acceptance check.
- [ ] Verify invalid inputs through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#12–#16 domain behavior.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #26: Add CRUD, transaction and persistence integration tests

State: open; labels: mvp

## Goal
Add CRUD, transaction and persistence integration tests

## Description
Test API against memory and isolated SQLite repositories.

## Acceptance Criteria
- [ ] Verify create/edit/delete/group cascade through an executed acceptance check.
- [ ] Verify rollback through an executed acceptance check.
- [ ] Verify invalid member references through an executed acceptance check.
- [ ] Verify restart verified through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#19, #22, #24.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #27: Add frontend component, form and service tests

State: open; labels: mvp

## Goal
Add frontend component, form and service tests

## Description
Test meaningful UI behavior against deterministic service fixtures.

## Acceptance Criteria
- [ ] Verify validation prevents bad submit through an executed acceptance check.
- [ ] Verify mock operations through an executed acceptance check.
- [ ] Verify aPI error/loading rendering through an executed acceptance check.
- [ ] Verify tests execute through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#5, #23.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #28: Add Playwright complete user workflows

State: open; labels: mvp

## Goal
Add Playwright complete user workflows

## Description
Verify real browser operations connected to persistent backend.

## Acceptance Criteria
- [ ] Verify create group/members through an executed acceptance check.
- [ ] Verify all split modes through an executed acceptance check.
- [ ] Verify edit/delete through an executed acceptance check.
- [ ] Verify partial settlement through an executed acceptance check.
- [ ] Verify refresh through an executed acceptance check.
- [ ] Verify assertions through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#23, #25, #26, #27.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #29: Verify mobile responsiveness and keyboard accessibility

State: open; labels: mvp

## Goal
Verify mobile responsiveness and keyboard accessibility

## Description
Inspect key workflows at narrow viewport and using keyboard.

## Acceptance Criteria
- [ ] Verify no horizontal overflow through an executed acceptance check.
- [ ] Verify labeled forms through an executed acceptance check.
- [ ] Verify focusable controls through an executed acceptance check.
- [ ] Verify dialog escape/focus behavior through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#4, #23.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #30: Add CI for tests, build and contract validation

State: open; labels: mvp

## Goal
Add CI for tests, build and contract validation

## Description
Run backend/frontend suites and production build on GitHub Actions.

## Acceptance Criteria
- [ ] Verify workflow installs pinned dependencies through an executed acceptance check.
- [ ] Verify validates OpenAPI through an executed acceptance check.
- [ ] Verify real run checked before final pass through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#25–#29; workflow may be authored before execution.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #31: Execute independent final acceptance and prepare submission

State: open; labels: mvp

## Goal
Execute independent final acceptance and prepare submission

## Description
Run full checks, publish evidence and close only QA-verified MVP issues.

## Acceptance Criteria
- [ ] Verify exact commands/results and screenshots recorded through an executed acceptance check.
- [ ] Verify issues audited through an executed acceptance check.
- [ ] Verify limitations explicit through an executed acceptance check.

## Out of Scope
Authentication, payment processing, cloud hosting and post-MVP integrations.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#2–#30 and independent QA evidence.

## Test Expectations
Run relevant automated tests and actual acceptance workflow; record command, result and commit in QA handoff. Include invalid-input and empty-state cases where applicable.

---

## Issue #32: Export group statement as CSV (post-MVP)

State: open; labels: post-mvp

## Goal
Export group statement as CSV (post-MVP)

## Description
Add downloadable expense/share/settlement statement after MVP acceptance.

## Acceptance Criteria
- [ ] Verify future scope only through an executed acceptance check.
- [ ] Verify safe CSV escaping through an executed acceptance check.
- [ ] Verify integer-derived amounts through an executed acceptance check.
- [ ] Verify per-group currency through an executed acceptance check.

## Out of Scope
Current MVP implementation and closure.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#31 final MVP acceptance; future work only.

## Test Expectations
Design review in a later iteration.

---

## Issue #33: Introduce multi-workspace authentication (post-MVP)

State: open; labels: post-mvp

## Goal
Introduce multi-workspace authentication (post-MVP)

## Description
Explore authenticated workspaces without enlarging current local-first MVP.

## Acceptance Criteria
- [ ] Verify future scope only through an executed acceptance check.
- [ ] Verify tenancy/authorization design and migration plan required through an executed acceptance check.

## Out of Scope
Current MVP implementation and closure.

## Constraints
Local-first single workspace. React/TypeScript and FastAPI. Integer minor units; one two-decimal currency per group. Never claim unexecuted tests or QA approval. Engineer submits evidence; independent QA verifies before closure.

## Dependencies
#31 final MVP acceptance; future work only.

## Test Expectations
Design review in a later iteration.

---

## Issue #34: Fix horizontal page overflow at 390px mobile width

State: closed; labels: user-test-bug

## Goal
Keep the application viewport within mobile width.
## Description
Independent QA observed the actual mock app at 390px viewport: document.scrollWidth=498px, producing 108px unintended horizontal overflow. Desktop renders correctly. Screenshot: _docs/screenshots/mock-mobile.png (next evidence commit).
## Acceptance Criteria
- [ ] At 390px document.scrollWidth <= viewport width on all main screens.
- [ ] Navigation and expense forms remain reachable.
- [ ] Desktop layout retains readable charts and table.
## Out of Scope
New product functionality.
## Constraints
Fix responsive CSS/layout without removing information. PM grooming and independent QA rerun required.
## Dependencies
#4 #29.
## Test Expectations
Playwright viewport390 check document scrollWidth, navigate main screens and capture regression screenshot.

---

## Issue #35: Distinguish mutation failures from success and announce errors in dialogs

State: closed; labels: user-test-bug

## Goal
Show accessible error feedback for rejected mutations.
## Description
Independent browser QA submitted existing member Kairat. Dialog stays open but failure toast is green rgb(77,121,65) with lucide-circle-check. Toast outside open modal is aria-hidden, so assistive users cannot hear it.
## Acceptance Criteria
- [ ] Duplicate member failure shows visible error styling and text.
- [ ] Error is announced inside the active dialog via role alert.
- [ ] Successful mutations retain success feedback.
## Out of Scope
New features.
## Constraints
Keep rejected input and dialog open; do not mask server failures.
## Dependencies
#8 #24 #29.
## Test Expectations
Browser duplicate-member repro; RTL accessible failure regression; success feedback check.

---

## Issue #36: Apply saved display-name preference to workspace profile

State: closed; labels: user-test-bug

## Goal
Make the display-name setting visibly apply.
## Description
Independent browser QA saved QA Person in Settings; the input persists but sidebar profile still displays Kairat Usmanov.
## Acceptance Criteria
- [ ] Saved display name updates the sidebar profile.
- [ ] It remains after page refresh.
- [ ] Empty names show validation and retain last valid value.
## Out of Scope
Account authentication and backend profiles.
## Constraints
Local preference only; no claim of account changes.
## Dependencies
#29.
## Test Expectations
Save a distinct display name, inspect sidebar, reload and verify.

---

## Issue #37: Reject duplicate member names consistently in backend and mock

State: closed; labels: user-test-bug

## Goal
Preserve unambiguous member names and mock/API parity.
## Description
Independent QA posted member Alice then alice to same group in memory API. Both returned201, whereas mock rejects duplicate member names. This makes participants ambiguous and prevents integrated rejection-feedback regression.
## Acceptance Criteria
- [ ] Same-group trimmed casefold duplicate names return422 and do not add a row.
- [ ] Distinct groups may each have member Alice.
- [ ] Memory and SQLite repositories enforce equivalent behavior.
- [ ] Integrated UI shows duplicate failure inside member dialog.
## Out of Scope
Renaming members and account identity.
## Constraints
Validate atomically and preserve existing member records.
## Dependencies
#9 #19 #24 #35.
## Test Expectations
API Alice/alice/whitespace variants duplicate, cross-group allowance; shared memory/SQLite regression and integrated browser duplicate.

---

## Issue #38: Fix group rename request to match GroupUpdate contract

State: open; labels: user-test-bug

## Goal
Allow renaming an existing group through the real API.
## Description
Independent integrated browser QA: create KZT group ManagementQA; Edit group; change name to RenamedQA; Save. Dialog stays open with role alert body.currency: Extra inputs are not permitted. GroupForm sends currency through updateGroup although GroupUpdate schema only accepts name/description.
## Acceptance Criteria
- [ ] Rename updates group heading and list through real SQLite API.
- [ ] Description changes persist after refresh.
- [ ] Update request contains name and description only; currency remains immutable.
- [ ] Creation still sends selected currency.
## Out of Scope
Changing group currency after creation.
## Constraints
Preserve OpenAPI GroupUpdate source contract; fix typed payload projection.
## Dependencies
#7 #23 #24.
## Test Expectations
API adapter request body regression; integrated create KZT/edit/refresh/list flow, verify currency unchanged.

---

## Issue #39: Preserve requested group on direct links and page reload

State: open; labels: user-test-bug

## Goal
Open the group named by the group detail URL.
## Description
Independent QA actual browser fresh goto /groups/g2 rendered first group Lisbon getaway rather than The apartment, still wrong after5 seconds. Frontend route-selection effects overwrite the explicit route with first-group fallback.
## Acceptance Criteria
- [ ] Fresh direct /groups/g2 renders The apartment and matching details.
- [ ] Reload and back/forward keep URL and selected group consistent.
- [ ] Group selector on detail page updates URL and group together.
- [ ] Missing/deleted group gracefully falls back without redirect loops.
## Out of Scope
Additional routing features.
## Constraints
Preserve source contract and existing group create/delete behavior.
## Dependencies
#7 #8 #23.
## Test Expectations
Browser regression non-first direct link, reload, group switch, history; API-mode dynamic IDs; RTL route selection test.

---

## Issue #40: Restore keyboard focus to the opening control when dialogs close

State: open; labels: user-test-bug

## Goal
Keep keyboard users in context after closing a dialog.
## Description
Independent actual browser QA focused New group, pressed Enter, verified initial field focus and10Tab containment. Escape closed dialog but focus remained body rather than returning to New group after5seconds. Existing design-system and accessibility issue29 require return focus.
## Acceptance Criteria
- [ ] Escape returns focus to dialog opening button when it still exists.
- [ ] Close button and cancel restore focus likewise.
- [ ] Initial focus and focus containment remain functional.
- [ ] Successful mutation closure moves focus to an appropriate surviving control.
## Out of Scope
New dialog functionality.
## Constraints
Use accessible Radix focus lifecycle; preserve form error focus and avoid global autofocus loops.
## Dependencies
#4 #29.
## Test Expectations
Keyboard New group Enter/Tab/Escape trigger-focus regression; expense/member dialogs close focus; successful closure appropriate target.

---

## Issue #41: Raise contrast of small dashboard text to the documented accessibility target

State: open; labels: user-test-bug

## Goal
Make small dashboard labels readable at WCAG AA text contrast.
## Description
Independent actual browser computed .page-subtitle rgb(124,136,127) on rgb(247,248,244): ratio3.463 at11px, below4.5. Stat labels/details also pale. Existing design-system and issue4 promise accessible contrast. QA added failing computed-style browser regression.
## Acceptance Criteria
- [ ] Small body/subtitle/stat label/detail text has contrast>=4.5 on actual backgrounds.
- [ ] Sidebar muted small text is readable at>=4.5 where normal text.
- [ ] Essential labels remain present and hierarchy remains clear.
- [ ] Dark text/buttons/errors/focus styles retain readability.
## Out of Scope
Visual redesign or removing information.
## Constraints
Adjust semantic tokens scoped to actual text; preserve fintech identity and chart content.
## Dependencies
#4 #29.
## Test Expectations
Browser computed foreground/background ratio on subtitle/stat labels/details/sidebar; desktop/mobile screenshots and existing keyboard/mobile regressions.


