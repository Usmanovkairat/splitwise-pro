# Iteration 1 independent browser acceptance

Mock interface acceptance: PASS for principal workflows; mobile defect #34 was observed and independently verified after its scoped fix. Additional mutation feedback and display preference issues were reported to root for PM grooming; these remain outside any full final acceptance claim.

Executed actual Playwright browser via `QA_CHROMIUM_PATH=/tmp/chromium npx playwright test` from frontend. The committed runner uses a Vite webServer fixture because server processes in separate execution sessions were not reachable. Local bundled Chromium works without `--single-process`; that option initially caused later contexts to exit, an environment configuration issue corrected in the runner.

Verified principal workflow (test passed 3.9s): create QA trip; empty-member state; add Alice/Bob/Carol; equal1.00 uneven split; reject exact3.00 allocated2.00; correct exact shares; percentage10.00 at50/25/25; edit description; confirmed expense deletion; Alice balance+5.66 after exact deletion; partial Bob→Alice1.00 settlement; history note; analytics total11.00.

Screenshots: `_docs/screenshots/mock-desktop.png`, `_docs/screenshots/mock-mobile.png`. Captures wait for chart animation to finish. Desktop1440×1000; mobile390×844. Mobile navigation, group creation dialog and Escape dismissal verified.

## Observed defect #34 and verification

Initial stable390px viewport document.scrollWidth=498 vs innerWidth390. Table is intentionally scroll-contained but absolutely positioned screen-reader-only Actions header escaped its positioning context. Reproduced after500ms/reduced motion; real bug reported, PM groomed, engineer added positioning context to table container. QA regression passed across overview,groups,group-detail,expenses,balances,settlements,analytics,settings. Actions column retains accessible name; internal table scrollLeft>0 and edit action reachable. No global overflow hiding used.

## Additional observed defects (pending IDs)

Duplicate member Kairat on /groups/g1 produces text “A member with this name already exists.” in green `.toast`, computed rgb(77,121,65), circle-check icon. Toast lies outside modal and is aria-hidden while modal remains open; accessible role lookup requires includeHidden. Settings saves display name QA Person but sidebar still shows Kairat Usmanov. Root notified for real issue creation and PM scope/grooming; reproduction test records observations without claiming fix.

Final independent rerun for this gate: Playwright4/4 passed13.9s (one test records pending defect observations, not fixed assertions); Vitest7/7 passed across2 files; `npm run build` exit0, Vite built2283 modules. Build emitted nonfatal large bundle warning808.55kB JS (243.77kB gzip). These results were actually executed after #34 fix.
