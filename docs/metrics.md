# SplitWise Pro metrics

| Prometheus series | Type | Meaning |
| --- | --- | --- |
| `splitwise_http_requests_total` | Counter | One per API request excluding health probes, grouped by environment, operation and HTTP status |
| `splitwise_http_request_duration_seconds` | Histogram | API latency in seconds, with the same grouping. Use the `_bucket` series for p50, p95 and p99 |
| `splitwise_api_errors_total` | Counter | HTTP 5xx API responses, grouped by environment |
| `splitwise_groups_created_total` | Counter | Successful group creation with HTTP 201 |
| `splitwise_expenses_created_total` | Counter | Successful expense creation with HTTP 201 |
| `splitwise_settlements_created_total` | Counter | Successful settlement creation with HTTP 201 |
| `splitwise_expense_creation_duration_seconds` | Histogram | Duration of expense POST requests, grouped by environment and success/failure |
| `splitwise_balance_calculation_duration_seconds` | Histogram | Duration of balance GET requests, grouped by environment and success/failure |
| `splitwise_expense_creation_failures_total` | Counter | Expense POST responses with HTTP 5xx |
| `probe_success` | Gauge | Blackbox result, 1 for passing liveness/readiness and 0 for failure |

A successful creation is counted once after its repository operation succeeds. Failed requests and internal retries cannot add a second success measurement. The API currently treats a second successful POST as a new resource and counts each committed creation. The counters are process telemetry and reset on restart. They describe successful operations and can differ from current ledger size after deletions or restarts.

Operations use fixed route names. Labels never include user, group or expense IDs. Health probes are tracked separately so a lack of genuine application traffic cannot meet the minimum traffic threshold.
