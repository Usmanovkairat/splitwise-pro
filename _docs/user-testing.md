# Independent user-workflow verification

Status: pending execution. No browser PASS or defect is claimed by this planning document.

## Required acceptance matrix
Create/rename/delete group; add/remove unreferenced member; reject referenced-member removal; record all split methods; uneven cent rounding; edit/delete expense; inspect zero-sum balances and suggestions; record partial settlement; reject overpayment/nonmember/self transfer; inspect analytics; refresh; restart backend and verify SQLite; invalid inputs; empty/error states; narrow viewport and keyboard navigation.

## Evidence format
For each executed check record: date/environment, issue, exact steps/command, expected result, observed result, PASS/FAIL, commit and screenshot path. QA executes independently of the engineer. Real failures become user-test-bug issues; PM grooms, regression is added, engineer fixes and QA reruns. Do not create fake defects to populate this file.

## Current result
Not yet verified. Populate after actual execution.

## Actual interim findings from independent QA
- #34: at390px, document width498 persisted after500ms/reduced-motion settling. PM groomed responsive fix and regression; final rerun status is not recorded here yet.
- #35: duplicate existing member Kairat leaves modal open but emits green success/check toast, which is aria-hidden outside the modal. PM requires active-dialog alert and success/error distinction.
- #36: saving QA Person in Settings retains input but sidebar remains Kairat Usmanov. PM requires local preference application and refresh/invalid-name regressions.

These observed failures are not final acceptance PASS. Engineers implement; independent QA reruns and root records verified closure/evidence.

- #37: actual memory API returned201 for Alice and alice in one group, unlike mock. PM requires trimmed/casefold same-group uniqueness with422, cross-group allowance, memory/SQLite equivalence and integrated rejection alert. Verification pending independent rerun.
