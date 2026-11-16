# OpenTelemetry

The FastAPI backend sends metrics, traces and logs by OTLP/gRPC to the Collector when `OTEL_EXPORTER_OTLP_ENDPOINT` is set. Set `SPLITWISE_ENVIRONMENT` to development or production. The Compose overlay sets the internal endpoint. Outside this private network use an authenticated encrypted OTLP endpoint.

1. Open Grafana at http://127.0.0.1:3000 for development or http://127.0.0.1:3001 for production-like testing. Sign in as `admin` with the corresponding `GRAFANA_ADMIN_PASSWORD`.
2. Create a test group, add an expense or inspect balances to generate traffic. Allow an export and scrape interval before checking **SplitWise Pro — Application Observability**. Select the environment of the running stack. The two Grafana endpoints can be viewed side by side.
3. In Explore, select Tempo and search for service `splitwise-pro`. Look for the server span, the enclosing business operation and `database.query` spans.
4. In Explore, select Loki and use `{service_name="splitwise-pro"}`. Match an OTLP log's `trace_id` with a Tempo trace of the same ID.

App log records carry an OTLP timestamp, severity, environment, operation, status, trace ID and span ID. Server exceptions contribute a bounded error-class identifier. SQL spans record the database dialect and omit query text and arguments. Telemetry omits raw HTTP paths, query strings, request bodies, account identifiers and ledger amounts. Prometheus, Tempo, Loki and Collector ports stay on the internal Compose network. Use protected access to Grafana in any remote environment.
