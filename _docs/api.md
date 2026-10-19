# API guide

The reviewed source contract is `openapi.yml`, produced in iteration 2 after mock frontend acceptance. This planning guide records the agreed resource shape; it does not claim backend implementation or contract validation yet.

All resource identifiers are strings. Monetary inputs/outputs are integer minor units. Group currency is KZT, USD, EUR or GBP; one currency per group. Expense `split_type` is equal/exact/percentage; `split_values` maps member ID to 1/exact minor units/integer basis points respectively. Percentage basis points sum to 10000. Returned shares contain `member_id` and `amount_minor`.

Planned routes: group list/create/detail/update/delete under `/api/groups`; nested members, expenses and settlements under `/api/groups/{group_id}`; balances and analytics read routes in the same context. Expense fields: description, amount_minor, payer_id, category, date, split_type, split_values. Settlement fields: from_member_id, to_member_id, amount_minor, date, note. Balances expose paid_minor, owed_minor, net_minor and simplified suggestions.

Require positive integer expenses/settlements, valid group members and deterministic allocation. Unknown resources return not-found; malformed input returns validation errors; referenced-member removal or invalid debt repayment returns an actionable conflict/validation response as specified by the final contract. Settlements record repayments without transferring funds.

Pagination/filter semantics, concrete examples, operation IDs and full error schemas must be read from the completed contract. Check actual runtime behavior against it during integration.
