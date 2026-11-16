"""Authenticated, read-only Alertmanager incident responder."""
import hashlib
import hmac
import json
import math
import os
import re
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ALERTS = {
    "HighAPIErrorRate": ("API requests are failing", "Check recent deployments and correlate the 5xx rate with database readiness."),
    "HighAPILatency": ("API requests are slow", "Inspect slow request traces and compare time spent in database spans."),
    "ApplicationDown": ("HTTP liveness probe is failing", "Check the deployment status and the application listener."),
    "DatabaseUnavailable": ("Database readiness probe is failing", "Check PostgreSQL availability, configuration and connection limits."),
    "ExpenseCreationFailure": ("Expense creation has elevated server-side failures", "Inspect the expense operation spans and check database readiness."),
}
CAUSES = {
    "backend": "Backend operation failure",
    "database": "Database connectivity or contention",
    "deployment": "Deployment or listener failure",
    "unknown": "Insufficient evidence to isolate a cause",
}
ACTIONS = {
    "compare_metrics": "Compare error and latency trends with the previous deployment.",
    "check_database": "Check database readiness and connection limits.",
    "inspect_traces": "Inspect recent error traces in Grafana.",
    "check_application": "Check the deployment status and network path to the application.",
}
TRACE_ID = re.compile("[a-f0-9]{32}")
FINGERPRINT = re.compile("[a-f0-9]{8,64}")
ENVIRONMENTS = {"development", "production"}
MAX_BODY = 128 * 1024
MAX_BACKEND_BODY = 2 * 1024 * 1024
MAX_ALERTS = 10


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_json(url, *, params=None, data=None, token=None, timeout=2):
    if params:
        url += "?" + urlencode(params)
    headers = {"Accept": "application/json"}
    payload = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        payload = json.dumps(data).encode()
    if token:
        headers["Authorization"] = "Bearer " + token
    with build_opener(NoRedirect).open(Request(url, data=payload, headers=headers), timeout=timeout) as response:
        body = response.read(MAX_BACKEND_BODY + 1)
    if len(body) > MAX_BACKEND_BODY:
        raise ValueError("Upstream response too large")
    return json.loads(body) if body else {}


def optional_request(url, **kwargs):
    try:
        return request_json(url, **kwargs)
    except (OSError, URLError, ValueError):
        return None


def alert_details(alert):
    if not isinstance(alert, dict) or not isinstance(alert.get("labels"), dict):
        return None
    labels = alert["labels"]
    name, environment = labels.get("alertname"), labels.get("environment")
    if not isinstance(name, str) or name not in ALERTS or environment not in ("development", "production"):
        return None
    status = alert.get("status")
    fingerprint = alert.get("fingerprint")
    if status not in ("firing", "resolved") or not isinstance(fingerprint, str) or not FINGERPRINT.fullmatch(fingerprint):
        return None
    try:
        started = datetime.fromisoformat(alert["startsAt"])
        if started.tzinfo is None:
            return None
        started = started.astimezone(timezone.utc).isoformat()
    except (KeyError, TypeError, ValueError, OverflowError):
        return None
    key = hashlib.sha256(f"{name}/{environment}/{fingerprint}/{started}".encode()).hexdigest()
    severity = "critical" if name in ("HighAPIErrorRate", "ApplicationDown", "DatabaseUnavailable") else "warning"
    return key, name, environment, severity, status


class Responder:
    def __init__(self, state_dir, environment=None):
        config = os.environ if environment is None else environment
        self.token = config.get("ONCALL_WEBHOOK_TOKEN", "")
        if not self.token:
            raise ValueError("ONCALL_WEBHOOK_TOKEN is required")
        self.prometheus = config.get("PROMETHEUS_URL", "http://prometheus:9090").rstrip("/")
        self.loki = config.get("LOKI_URL", "http://loki:3100").rstrip("/")
        self.tempo = config.get("TEMPO_URL", "http://tempo:3200").rstrip("/")
        self.service = config.get("ONCALL_SERVICE_NAME", "splitwise-pro")
        self.api_key = config.get("OPENAI_API_KEY", "")
        self.model = config.get("OPENAI_MODEL", "gpt-4.1-mini")
        self.destination = config.get("ONCALL_NOTIFICATION_URL", "")
        self.notification_token = config.get("ONCALL_NOTIFICATION_TOKEN", "")
        self.environment = config.get("ONCALL_ENVIRONMENT", "")
        if not re.fullmatch("[a-zA-Z0-9_.-]+", self.service):
            raise ValueError("Invalid ONCALL_SERVICE_NAME")
        if self.environment and self.environment not in ENVIRONMENTS:
            raise ValueError("Invalid ONCALL_ENVIRONMENT")
        if self.destination and urlsplit(self.destination).scheme != "https":
            raise ValueError("ONCALL_NOTIFICATION_URL must use HTTPS")
        directory = Path(state_dir)
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.database = directory / "incidents.sqlite3"
        with self.connect() as database:
            database.execute(
                """CREATE TABLE IF NOT EXISTS incident (
                    incident_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    report TEXT NOT NULL,
                    updated REAL NOT NULL
                )"""
            )
        self.rate_lock = threading.Lock()
        self.window_start = time.monotonic()
        self.requests = 0

    @contextmanager
    def connect(self):
        database = sqlite3.connect(self.database, timeout=2)
        try:
            with database:
                yield database
        finally:
            database.close()

    def accept_request(self):
        with self.rate_lock:
            now = time.monotonic()
            if now - self.window_start >= 60:
                self.window_start = now
                self.requests = 0
            if self.requests >= 30:
                return False
            self.requests += 1
            return True

    def metric(self, query):
        response = optional_request(self.prometheus + "/api/v1/query", params={"query": query})
        try:
            value = float(response["data"]["result"][0]["value"][1])
            return round(value, 5) if math.isfinite(value) else None
        except (TypeError, ValueError, KeyError, IndexError):
            return None

    def logs(self, environment):
        response = optional_request(
            self.loki + "/loki/api/v1/query_range",
            params={
                "query": (
                    f'{{service_name="{self.service}"}} '
                    f'| deployment_environment_name="{environment}" | severity_text="ERROR"'
                ),
                "since": "10m",
                "limit": "20",
            },
        )
        try:
            streams = response["data"]["result"]
            matches, trace_ids = 0, set()
            for stream in streams:
                for entry in stream["values"]:
                    matches += 1
                    metadata = entry[2] if len(entry) > 2 and isinstance(entry[2], dict) else {}
                    trace_id = metadata.get("trace_id", stream.get("stream", {}).get("trace_id"))
                    if isinstance(trace_id, str) and TRACE_ID.fullmatch(trace_id):
                        trace_ids.add(trace_id)
            return matches, sorted(trace_ids)[:3]
        except (TypeError, KeyError, AttributeError):
            return None, []

    def evidence(self, environment):
        labels = f'environment="{environment}"'
        queries = {
            "requests_per_second": f'sum(rate(splitwise_http_requests_total{{{labels}}}[5m]))',
            "errors_per_second": f'sum(rate(splitwise_api_errors_total{{{labels}}}[5m]))',
            "app_available": f'min(probe_success{{job="splitwise-probes",probe="app",{labels}}})',
            "database_ready": f'min(probe_success{{job="splitwise-probes",probe="database",{labels}}})',
            "expense_failures_5m": f'sum(increase(splitwise_expense_creation_failures_total{{{labels}}}[5m]))',
            "p95_seconds": (
                'histogram_quantile(0.95, sum by (le) '
                f'(rate(splitwise_http_request_duration_seconds_bucket{{{labels}}}[5m])))'
            ),
        }
        with ThreadPoolExecutor(max_workers=4) as pool:
            metrics = {name: pool.submit(self.metric, query) for name, query in queries.items()}
            logs = pool.submit(self.logs, environment)
            log_matches, trace_ids = logs.result()
            traces = {
                trace_id: pool.submit(optional_request, self.tempo + "/api/traces/" + trace_id)
                for trace_id in trace_ids
            }
            return {
                "metrics": {name: result.result() for name, result in metrics.items()},
                "error_log_samples": log_matches,
                "verified_trace_ids": [trace_id for trace_id, result in traces.items() if result.result()],
            }

    def analyze(self, name, evidence):
        _, action = ALERTS[name]
        analysis = {
            "mode": "fallback",
            "possible_cause": "Insufficient evidence to isolate a cause",
            "recommended_action": action,
        }
        if evidence["metrics"].get("app_available") == 1 and evidence["metrics"].get("database_ready") == 0:
            analysis["possible_cause"] = CAUSES["database"]
            analysis["recommended_action"] = ACTIONS["check_database"]
        if not self.api_key:
            return analysis
        # Only locally generated labels and numeric summaries cross the model boundary.
        model_input = {
            "alert": name,
            "metrics": evidence["metrics"],
            "error_log_samples": evidence["error_log_samples"],
            "verified_trace_count": len(evidence["verified_trace_ids"]),
        }
        response = optional_request(
            "https://api.openai.com/v1/responses",
            token=self.api_key,
            timeout=5,
            data={
                "model": self.model,
                "store": False,
                "instructions": (
                    "Classify a monitoring incident and select one read-only inspection step. "
                    "Use the unknown cause when telemetry does not establish a likely cause."
                ),
                "input": json.dumps(model_input),
                "max_output_tokens": 160,
                "text": {"format": {
                    "type": "json_schema",
                    "name": "incident_classification",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "cause": {"type": "string", "enum": list(CAUSES)},
                            "action": {"type": "string", "enum": list(ACTIONS)},
                        },
                        "required": ["cause", "action"],
                        "additionalProperties": False,
                    },
                }},
            },
        )
        try:
            classification = next(
                json.loads(part["text"])
                for item in response["output"]
                for part in item.get("content", [])
                if part.get("type") == "output_text"
            )
            return {
                "mode": "model",
                "possible_cause": CAUSES[classification["cause"]],
                "recommended_action": ACTIONS[classification["action"]],
            }
        except (KeyError, TypeError, ValueError, StopIteration):
            return analysis

    def handle_alert(self, alert):
        details = alert_details(alert)
        if not details:
            return {"result": "ignored"}
        key, name, environment, severity, status = details
        if self.environment and environment != self.environment:
            return {"result": "ignored"}
        now = time.time()
        with self.connect() as database:
            database.execute("BEGIN IMMEDIATE")
            previous = database.execute("SELECT * FROM incident WHERE incident_id = ?", (key,)).fetchone()
            if previous and (
                previous[1] in (status, "resolved")
                or (previous[1] == "processing" and status == "firing" and previous[3] > now - 120)
            ):
                return {"result": "duplicate", "incident_id": key}
            if status == "firing":
                database.execute(
                    "INSERT OR REPLACE INTO incident VALUES (?, 'processing', '', ?)", (key, now)
                )
            else:
                report = json.loads(previous[2]) if previous and previous[2] else {
                    "incident_id": key, "environment": environment, "service": self.service, "alert_type": name,
                    "severity": severity, "timestamp": datetime.now(timezone.utc).isoformat(),
                    "symptom": ALERTS[name][0], "evidence": {}, "analysis": {},
                }
                report["status"] = status
                database.execute(
                    "INSERT OR REPLACE INTO incident VALUES (?, ?, ?, ?)", (key, status, json.dumps(report), now)
                )
        if status == "firing":
            evidence = self.evidence(environment)
            report = {
                "incident_id": key,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "environment": environment,
                "service": self.service,
                "alert_type": name,
                "severity": severity,
                "symptom": ALERTS[name][0],
                "evidence": evidence,
                "analysis": self.analyze(name, evidence),
                "status": status,
            }
            with self.connect() as database:
                updated = database.execute(
                    """UPDATE incident SET status = ?, report = ?, updated = ?
                       WHERE incident_id = ? AND status = 'processing' AND updated = ?""",
                    (status, json.dumps(report), time.time(), key, now),
                )
                if not updated.rowcount:
                    return {"result": "superseded", "incident_id": key}
        delivered = None
        if self.destination:
            try:
                request_json(self.destination, data=report, token=self.notification_token)
                delivered = True
            except (OSError, ValueError):
                delivered = False
        print(json.dumps({"incident_id": key, "status": status, "notification_delivered": delivered}), flush=True)
        return {"result": status, "incident_id": key}


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *_):
        pass

    def do_GET(self):
        self.reply(200 if self.path == "/health" else 404, {"service": "oncall"})

    def do_POST(self):
        if self.path != "/alerts":
            self.reply(404, {"error": "Unknown endpoint"})
            return
        responder = self.server.responder
        actual = self.headers.get("Authorization", "").encode()
        expected = ("Bearer " + responder.token).encode()
        if not hmac.compare_digest(actual, expected):
            self.reply(401, {"error": "Unauthorized"})
            return
        if not responder.accept_request():
            self.reply(429, {"error": "Rate limit exceeded"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BODY:
                self.reply(413, {"error": "Unsupported payload size"})
                return
            payload = json.loads(self.rfile.read(length))
            alerts = payload.get("alerts") if isinstance(payload, dict) else None
            if not isinstance(alerts, list) or not 0 < len(alerts) <= MAX_ALERTS:
                raise ValueError("Expected a bounded alerts array")
        except (ValueError, OSError):
            self.reply(400, {"error": "Invalid alert payload"})
            return
        with ThreadPoolExecutor(max_workers=MAX_ALERTS) as pool:
            self.reply(200, {"alerts": list(pool.map(responder.handle_alert, alerts))})


class IncidentServer(ThreadingHTTPServer):
    def __init__(self, address, responder):
        super().__init__(address, Handler)
        self.responder = responder
        self.slots = threading.BoundedSemaphore(4)

    def process_request(self, request, client_address):
        if not self.slots.acquire(blocking=False):
            request.settimeout(1)
            try:
                request.sendall(b"HTTP/1.0 503 Service Unavailable\r\nContent-Length: 0\r\n\r\n")
            except OSError:
                pass
            finally:
                self.shutdown_request(request)
            return
        request.settimeout(5)
        super().process_request(request, client_address)

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()


if __name__ == "__main__":
    responder = Responder(os.getenv("ONCALL_STATE_DIR", "/data"))
    IncidentServer(("0.0.0.0", 8080), responder).serve_forever()
