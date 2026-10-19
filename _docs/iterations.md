# Iteration execution ledger

This ledger separates intended stages from executed evidence. Pending entries are not claims of completion. Update each row with the real commit and exact check outcomes after execution.

| Stage | Deliverable | Evidence status |
|---|---|---|
| 0 | Planning, roles, design, issue backlog | Published planning commit `d23aa034`; independent planning QA PASS for #1/#3; frontend not yet published |
| 1 | Complete frontend with mockService | Pending |
| 2 | Validated openapi.yml | Pending |
| 3 | Independent in-memory API | Pending |
| 4 | ORM, migration and restart persistence | Pending |
| 5 | Typed frontend/backend integration | Pending |
| 6 | Browser acceptance and real bug regressions | Pending |
| 7 | Final suites, build, hosted CI and issue audit | Pending |

Do not collapse stages or rewrite history to imply work happened earlier. Record actual commands, return results, screenshot locations and independent QA decisions below as they occur.

## Interim mock-stage evidence and defects
Frontend mock stage published as `8517285123a9b5da141cff52fa371c5f9786fe1f`. Independent browser testing produced actual issues #34 (390px overflow), #35 (success-styled/inaccessible modal error) and #36 (saved profile preference unapplied). PM groomed each; fix and QA rerun evidence must be recorded separately. This entry does not claim final frontend acceptance.
