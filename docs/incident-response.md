# Incident response

1. Read the incident and verify its environment, severity, and firing status. Match its timestamp to the Grafana metrics window.
2. Check the supplied request rate, errors per second, p95 latency, app liveness, database readiness, and expense failures. A missing value means the responder could not establish that observation.
3. Open verified trace IDs in Grafana Explore and use them to find the matching Loki entries. Use the possible cause as a hypothesis, then verify it against the observed signals and recent deployment history.
4. Assign an owner before changing infrastructure. Use the production approval and release procedures in [manual promotion](manual-promotion.md) for any approved change.
5. Confirm that the affected metric recovers and the alert resolves. Record the actual cause and actions in the team's incident record.

Run this against the development observability Compose stack to inspect incident reports. Use the same Compose files and project options used to start that stack.

```sh
docker compose -f compose.yaml -f compose.observability.yaml exec -T oncall python -c \
  'import sqlite3; db=sqlite3.connect("/data/incidents.sqlite3"); print(*[r[0] for r in db.execute("SELECT report FROM incident WHERE status != ? ORDER BY updated DESC LIMIT 10", ("processing",))], sep="\n")'
```

For a controlled development alert, follow the verification procedure in [alerting](alerting.md). Check that the incident has the development label and includes the evidence available when it fired. Keep the external notification setting empty during local tests unless the destination owner has authorized the test.
