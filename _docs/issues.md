# Groomed issue map

Issues are created before feature implementation; actual GitHub timestamps are authoritative. QA must verify before closure. #1 covers initial orchestration.

| Issues | Scope | Iteration |
|---|---|---|
| #2–3 | Bootstrap and honest planning | 0 |
| #4–5 | Design shell and deterministic mockService | 1 |
| #6–11 | Dashboard, group/member and expense UI | 1 |
| #12–14 | Equal, exact and percentage allocation | 1 |
| #15–17 | Balances, settlements and analytics | 1 |
| #18 | OpenAPI 3.1 source contract | 2 |
| #19 | FastAPI with in-memory repositories | 3 |
| #20–22 | SQLAlchemy, Alembic and SQLite persistence | 4 |
| #23–24 | HTTP integration and server validation | 5 |
| #25–29 | Math/API/UI/browser/accessibility tests | 6 |
| #30–31 | CI and independent final acceptance | 7 |
| #32–33 | CSV export and authenticated workspaces | Post-MVP, remain open |

Base issue URL: https://github.com/Usmanovkairat/splitwise-pro/issues

## Concrete dependencies
#2/#3 precede #4/#5. #4/#5 precede #6–#11; #10 precedes #12–#14. #12–#14 precede #15, which precedes #16/#17. Mock frontend acceptance precedes #18 contract. #18 precedes #19 memory API. #19 precedes #20 models, #21 migrations and #22 SQLite. #22 and frontend acceptance precede #23 integration. #24 validates all APIs. #25–#29 cover invariant/API/UI/browser/accessibility checks; #30 CI and #31 final acceptance require all relevant checks. #32/#33 are future scope, intentionally open.

## PM grooming audit
All initial issue scopes include the seven requested sections. Concrete prerequisite numbers in the dependency graph above supersede shorthand words in the original creation draft. Acceptance verification includes actual execution rather than document existence alone. API/storage work must preserve the same numerical contract; UI work includes empty/loading/error feedback. Issues are not auto-closed by implementation commits; independent QA records PASS first.

## Observed bug #34 — mobile overflow
Independent QA confirmed document width 498px at viewport390 after 500ms settling with reduced motion. PM groomed the real defect on GitHub: preserve accessible action labels/content, constrain offending layout, assert document width on all main screens, verify form reachability and desktop layout, capture regression screenshot. Suspected table header is a lead, not a claimed root cause. Engineer may fix after QA regression definition; independent QA rerun is required before closure.

## Observed bugs #35 and #36 — PM groomed
#35: QA reproduced duplicate-member error incorrectly rendered with green check success feedback; external toast is aria-hidden by the modal. Require an error alert inside the active dialog, preserved invalid input, no false success, corrected-input success regression. Correct member dependency is #9 plus #24/#29.

#36: QA saved local display name but sidebar retained hardcoded profile. Require immediate application, navigation/refresh persistence, whitespace validation retaining last valid value, consistent initials and no group-member/account mutation. Both are real reported findings; independent QA rerun remains required.

## Observed bug #37 — same-group name uniqueness
QA observed memory API accepting Alice/alice with201 while mock rejects. PM groomed trimmed Unicode-casefold key scoped to group; duplicate422 and unchanged member list; cross-group same name allowed; shared memory/SQLite regression, atomic insert and integrated modal error required. Memory base and separate fix retain chronological evidence; SQLite follows memory publication. No QA PASS claimed.

Independent follow-up: `_docs/qa/bug-37.md` now records all memory/mock/SQLite-restart/integrated segments PASS. Remote closure still requires root/QA publication and final issue action.

## Observed bug #38 — immutable currency leaked into rename payload

Extended real-API browser QA created a KZT group and attempted rename; PUT included currency and correctly failed422 against strict GroupUpdate. PM grooming comment6283144050 requires explicit name/description projection at form and API-adapter boundaries, immutable currency retained, creation currency preserved, an adapter regression with intentional runtime extras, and real KZT rename/description/list/refresh verification. Backend validation and OpenAPI must remain strict. This is an observed integration defect; final group-management acceptance remains pending independent fix rerun.

Fix#38 subsequently published at `571fb77b6f2cd8bcabadf8e1d014489f5f3fdb3f`; independent QA reported all3 integrated tests PASS after the fix.

## Observed bug #39 — direct group URL loses requested context

Fresh browser navigation to `/groups/g2` rendered first group Lisbon getaway instead of The apartment, still wrong after5 seconds. PM grooming comment6283185144 requires valid URL group ID to take precedence over fallback, consistent reload/back/forward and detail-page picker navigation, and missing/deleted-group fallback via replace to the first existing group's detail or `/groups` when empty. QA must retain non-first direct-link regression, use async loading RTL to catch the effect race and repeat dynamic-ID API routing. No final route PASS is claimed before independent verification.

Route fix#39 was published at `72aa759275c653722b201941492309268de185e4`. Root reported direct-link/reload mock regression PASS; final API-mode/current-source route acceptance remains independently reviewed.

## Observed bugs #40 and #41 — existing accessibility requirements

#40: independent keyboard QA opened New group with Enter, traversed10 Tab steps within the dialog, then Escape closed it but left focus on body after5 seconds. PM comment6283219114 requires capture/restoration of actual connected visible opener on Escape/cancel/close and a sensible surviving control after mutation if the opener disappears. Keep Radix initial focus/trapping and avoid global autofocus loops.

#41: actual browser subtitle rgb(124,136,127) on rgb(247,248,244),11px, measured3.463 contrast. PM comment6283226073 requires semantic normal small text (subtitle/stat/detail/sidebar) contrast>=4.5 on actual surfaces; preserve fintech palette, hierarchy, labels and layout. Decorative borders/charts do not expand this bug. QA retains measured failure, corrected color/ratio evidence, screenshots and existing keyboard/mobile regressions. Both defects arise from explicit design-system/issue29 criteria; no new functionality is introduced.
