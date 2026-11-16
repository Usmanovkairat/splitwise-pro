# Alerts

Prometheus evaluates rules every 15 seconds and sends firing alerts to Alertmanager. Alertmanager authenticates to the on-call webhook with a token held in a Compose secret. Reports are recorded locally and the responder can use its configured notification URL. Alert identity includes the environment.

| Alert | Condition | Sustain | Severity | First check |
| --- | --- | --- | --- | --- |
| HighAPIErrorRate | API 5xx rate >5% with at least 20 requests in five minutes | 5 min | Critical | Check recent API errors and correlated traces |
| HighAPILatency | p95 API latency >1 s with at least 20 requests in five minutes | 5 min | Warning | Inspect traces for expensive database or business operations |
| ApplicationDown | Application liveness fails | 2 min | Critical | Check container, host and probe health |
| DatabaseUnavailable | Application is live but database readiness fails | 1 min | Critical | Check PostgreSQL process, connectivity and pool limits |
| ExpenseCreationFailure | At least three expense-creation HTTP 5xx responses in five minutes | 1 min | Warning | Inspect expense operation errors and database health |

On a disposable development stack only, run the integration smoke test with `--alert` to exercise the monitoring pipeline, a controlled database failure and incident generation. See the observability CI job for the exact commands. Use Prometheus rule-unit tests to check the other thresholds without delaying a live system.
