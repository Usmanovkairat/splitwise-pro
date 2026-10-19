# Iteration 3 independent in-memory API QA

Result: PASS for #19 memory API stage and #25 mathematical foundation; #24 full validation/parity remains subject to tracked duplicate-name drift #37 and final integration. No SQLite persistence is claimed at this stage.

Executed `.venv/bin/python -m pytest backend/tests -q`:26 passed,1 Starlette TestClient deprecation warning,0.88s. Reviewed tests independently: CRUD/isolation, stable rounding cases,250 randomized invariant iterations, invalid input atomicity, partial settlement bounds, category/date/contribution analytics, filters and health.

Executed independent TestClient scenario with jsonschema validation against source openapi.yml:13 response validations passed (Group,Member,Expense,Balances,Settlement,Analytics,404Error,422Error). Created3 members, equal100/exact300/percentage1001 expenses, checked sums, zero-sum balance, recorded partial1-minor settlement, checked analytics, group cascade, and new application factory resets memory. Command: `PYTHONPATH=. .venv/bin/python /tmp/qa-memory.py` (temporary QA harness, described here rather than falsely presented as committed suite).

Observed parity gap reported as real issue #37: POST Alice then alice succeeds201 in backend; mockService rejects case-insensitive duplicate member names. PM must decide/groom explicit invariant; final #24 cannot assert parity until resolved. No other failure found in this gate. Source has no SQL repository at time of this review, preserving required iteration order.
