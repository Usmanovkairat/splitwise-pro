# Independent user-workflow verification

Status: pending execution. No browser PASS or defect is claimed by this planning document.

## Required acceptance matrix
Create/rename/delete group; add/remove unreferenced member; reject referenced-member removal; record all split methods; uneven cent rounding; edit/delete expense; inspect zero-sum balances and suggestions; record partial settlement; reject overpayment/nonmember/self transfer; inspect analytics; refresh; restart backend and verify SQLite; invalid inputs; empty/error states; narrow viewport and keyboard navigation.

## Evidence format
For each executed check record: date/environment, issue, exact steps/command, expected result, observed result, PASS/FAIL, commit and screenshot path. QA executes independently of the engineer. Real failures become user-test-bug issues; PM grooms, regression is added, engineer fixes and QA reruns. Do not create fake defects to populate this file.

## Current result
Not yet verified. Populate after actual execution.
