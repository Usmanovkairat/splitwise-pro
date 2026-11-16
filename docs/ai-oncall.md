# AI on-call responder

Alertmanager sends firing and resolved events to the internal Python responder at `POST /alerts`. The service authenticates the Bearer token, accepts the five documented alert types, and recognizes development and production labels. It queries environment-scoped Prometheus vectors, counts recent error records in Loki, and checks up to three correlated trace IDs against Tempo.

The service keeps reports in `/data/incidents.sqlite3` in the `oncall_data` volume. It keys incidents by environment, alert type, fingerprint, and start time, so repeated webhooks update one incident. The report preserves the observed metrics, sampled error-log count, and verified trace IDs. During a telemetry outage, missing values appear as `null` and the fallback can still record the alert and recommend a check.

## Configuration

| Setting | Purpose |
| --- | --- |
| `ONCALL_WEBHOOK_TOKEN` | Required shared secret. Use a random high-entropy value and keep it outside Git. |
| `OPENAI_API_KEY` | Optional. Configuring a key enables OpenAI Responses API calls and any usage charges associated with that key. |
| `OPENAI_MODEL` | Optional container environment override for the structured-output model. Default is `gpt-4.1-mini`. |
| `ONCALL_NOTIFICATION_URL` | Optional approved HTTPS endpoint that accepts the incident report as JSON and routes it to the person on call. |
| `ONCALL_NOTIFICATION_TOKEN` | Optional container environment override for the notification endpoint's Bearer token. |
| `ONCALL_ENVIRONMENT` | Optional container environment override to handle only the specified environment. |

The service emits a delivery result to its container logs. Notification delivery is attempted once per incident transition. If it fails, the report stays in SQLite and staff can forward it from there. Without a notification URL all reports stay local.

## Data and access

Model input contains a known alert identifier, numeric values and counts. Raw alert annotations, log lines, trace payloads, and trace IDs never enter the prompt. The service only accepts model output that matches its fixed cause and action options. The model has no tool access. The responder reads monitoring APIs, writes to its report volume, and optionally posts the report to the configured notification endpoint. No application database, deployment, or infrastructure credentials are required. Keep the monitoring network and incident volume restricted to operators.

The fallback handles missing credentials, model timeouts, and unusable responses. Local verification uses the fallback and a mocked model call:

```sh
python -m unittest discover -s oncall -v
```
