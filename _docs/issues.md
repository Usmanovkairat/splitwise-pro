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
