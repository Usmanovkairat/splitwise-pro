"""Verify an existing Compose stack. --alert stops and restores the development DB."""
import argparse
import base64
import json
import os
import subprocess
import time
from urllib.parse import urlencode


SMOKE_HTTP = """
import json, sys, urllib.error, urllib.request
url, method, payload = sys.argv[1:]
authorization = sys.stdin.read()
headers = {"Content-Type": "application/json"}
if authorization:
    headers["Authorization"] = authorization
request = urllib.request.Request(url, payload.encode() if payload else None, headers, method=method)
try:
    response = urllib.request.urlopen(request, timeout=8)
except urllib.error.HTTPError as error:
    response = error
with response:
    payload = response.read().decode()
    print(json.dumps([response.status, payload]))
"""

INCIDENT_REPORTS = """
import json, sqlite3
with sqlite3.connect("file:/data/incidents.sqlite3?mode=ro", uri=True) as db:
    print(json.dumps([json.loads(record) for record, in db.execute(
        "SELECT report FROM incident WHERE status = ?", ("firing",)
    )]))
"""


def eventually(check, timeout=100):
    deadline = time.monotonic() + timeout
    last_error = None
    while time.monotonic() < deadline:
        try:
            result = check()
            if result:
                return result
        except (subprocess.CalledProcessError, AssertionError, ValueError, KeyError) as error:
            last_error = error
        time.sleep(3)
    raise AssertionError(f"Timed out waiting for {check.__name__}: {last_error}")


def verify(compose, simulate_alert):
    def run(*args, stdin=""):
        return subprocess.check_output([*compose, *args], text=True, timeout=30, input=stdin)

    def http(url, method="GET", payload=None, authorization=""):
        output = run("exec", "-T", "app", "python", "-c", SMOKE_HTTP, url, method,
                     json.dumps(payload) if payload is not None else "", stdin=authorization)
        return json.loads(output)

    def get(url, authorization=""):
        code, raw = http(url, authorization=authorization)
        assert code == 200, f"{url}: HTTP {code}"
        return json.loads(raw)

    def prometheus(query):
        result = get("http://prometheus:9090/api/v1/query?" + urlencode({"query": query}))
        assert result["status"] == "success"
        return result["data"]["result"]

    def deployment():
        return run("exec", "-T", "app", "python", "-c",
                   "import os; print(os.environ.get('SPLITWISE_ENVIRONMENT', 'development'))").strip()

    environment = deployment()
    if simulate_alert and environment != "development":
        raise ValueError("--alert is available only on explicitly selected development stacks")
    health = eventually(lambda: get("http://app:8000/api/health"))
    assert health["database"] == "postgresql", health
    eventually(lambda: get("http://grafana:3000/api/health"))
    password = os.getenv("GRAFANA_ADMIN_PASSWORD")
    if password:
        auth = "Basic " + base64.b64encode(f"admin:{password}".encode()).decode()
        dashboard = eventually(lambda: get(
            "http://grafana:3000/api/dashboards/uid/splitwise-observability", auth
        ))
        assert dashboard["dashboard"]["title"] == "SplitWise Pro — Application Observability"

    label = '{environment="' + environment + '"}'
    counter = "splitwise_groups_created_total" + label

    def total(metric):
        return sum(float(row["value"][1]) for row in prometheus(metric))

    eventually(lambda: prometheus('probe_success' + label))
    before = total(counter)
    code, raw = http("http://app:8000/api/groups", "POST",
                     {"name": "Observability smoke test", "description": "", "currency": "KZT"})
    assert code == 201, code
    group = json.loads(raw)
    group_url = "http://app:8000/api/groups/" + group["id"]
    try:
        get(group_url + "/balances")
        eventually(lambda: total(counter) > before)
        eventually(lambda: prometheus("splitwise_balance_calculation_duration_seconds_count" + label))

        def correlated_trace():
            log_query = '{service_name="splitwise-pro"} | deployment_environment_name="' + environment + '"'
            result = get("http://loki:3100/loki/api/v1/query_range?" + urlencode(
                {"query": log_query, "limit": 30}
            ))
            for stream in result["data"]["result"]:
                for entry in stream["values"]:
                    metadata = {**stream["stream"], **(entry[2] if len(entry) > 2 else {})}
                    trace_id = metadata.get("trace_id")
                    if trace_id and len(trace_id) == 32:
                        code, trace = http("http://tempo:3200/api/traces/" + trace_id)
                        if code == 200 and json.loads(trace):
                            return True
            return False

        eventually(correlated_trace)
        print("PostgreSQL, Grafana, exported metrics, Loki logs and correlated Tempo traces verified")
    finally:
        assert http(group_url, "DELETE")[0] == 204, "Could not remove the test group"

    if simulate_alert:
        def firing_reports():
            try:
                return json.loads(run("exec", "-T", "oncall", "python", "-c", INCIDENT_REPORTS))
            except subprocess.CalledProcessError:
                return []

        previous = {row["incident_id"] for row in firing_reports()}
        errors = "splitwise_api_errors_total" + label
        baseline_errors = total(errors)
        try:
            run("stop", "db")
            code, _ = http("http://app:8000/api/health")
            assert code == 503, code
            code, _ = http("http://app:8000/api/groups")
            assert code == 500, code
            eventually(lambda: total(errors) > baseline_errors)

            def report_received():
                return any(row["incident_id"] not in previous
                           and row["alert_type"] == "DatabaseUnavailable"
                           and row["environment"] == "development"
                           and row["evidence"]["metrics"]["app_available"] == 1
                           and row["evidence"]["metrics"]["database_ready"] == 0
                           for row in firing_reports())

            eventually(report_received, timeout=150)
            print("Development database failure reached Alertmanager and generated an incident with evidence")
        finally:
            run("start", "db")
            eventually(lambda: get("http://app:8000/api/health"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alert", action="store_true")
    parser.add_argument("compose_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    compose_args = args.compose_args
    if compose_args[:1] == ["--"]:
        compose_args = compose_args[1:]
    verify(["docker", "compose", *compose_args], args.alert)


if __name__ == "__main__":
    main()
