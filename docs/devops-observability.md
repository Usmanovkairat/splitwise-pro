# SplitWise Pro — DevOps and observability

Start with [isolated environments](environments.md). Grafana provisions the **SplitWise Pro — Application Observability** dashboard. See [telemetry](opentelemetry.md), [metrics](metrics.md), [alerts](alerting.md), [AI on-call](ai-oncall.md), [incident response](incident-response.md), and [release promotion](manual-promotion.md).

```mermaid
flowchart TD
    CI["GitHub Actions CI"] --> Dev["Development app and PostgreSQL"]
    Dev -->|"Manual promotion of verified digest"| Prod["Production app and PostgreSQL"]
    Dev --> DevObs["Development observability stack"]
    Prod --> ProdObs["Production observability stack"]
```

Each environment runs this telemetry path independently.

```mermaid
flowchart TD
    App["SplitWise Pro API"] -->|"OTLP"| Collector["OpenTelemetry Collector"]
    Collector --> Prometheus
    Collector --> Tempo
    Collector --> Loki
    Prometheus --> Grafana
    Tempo --> Grafana
    Loki --> Grafana
    Prometheus --> Alertmanager --> Agent["On-call responder"]
```

The GitHub-hosted development deployment is disposable. For screenshots, use a running local deployment and capture the dashboard after generating traffic. See [audit](devops-audit.md) for the status inherited from the deployment assignment.
