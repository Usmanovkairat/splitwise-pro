# Independent QA: group-update payload regression #38

Scoped fix verification PASS. The original integrated browser failure was PUT group rename returning 422 `body.currency: Extra inputs are not permitted`. PM groomed the real issue; engineer changed both GroupForm update submission and the typed API adapter to project only name and description. Group creation retains selected currency.

Independent commands after engineer handoff:

- `npm --prefix frontend test`: 22 passed across 3 files, 4.62s; includes adapter runtime-extra-field payload regression and RTL rename payload regression.
- `npm --prefix frontend run build`: exit 0; 2285 modules, 835.52 kB JavaScript / 253.99 kB gzip. Nonfatal large-chunk warning remains documented.
- `QA_CHROMIUM_PATH=/tmp/chromium npx playwright test --config playwright.integration.config.ts` from frontend: 3 passed in 16.6s. Real migrated SQLite management scenario creates a KZT group, verifies currency disabled during edit, renames through actual PUT, removes an unreferenced member with cancel/confirm checks, deletes the group with cancel/confirm, and rejects removing referenced Alice. Full expense/split/partial-settlement workflow and recoverable 503/loading test also pass.

A separate fresh-link issue was independently discovered during final review: `/groups/g2` displays the first group, Lisbon getaway, rather than The apartment after 5 seconds. A new failing browser regression records it. This is a route-selection defect, not a reason to claim final whole-product acceptance; root was asked to create/groom a separate real bug before its fix. Final group deep-link/reload acceptance remains pending that issue.
