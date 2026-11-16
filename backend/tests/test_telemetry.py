from concurrent.futures import ThreadPoolExecutor

import grpc
import pytest
from fastapi.testclient import TestClient
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2, logs_service_pb2_grpc
from opentelemetry.proto.collector.metrics.v1 import metrics_service_pb2, metrics_service_pb2_grpc
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2, trace_service_pb2_grpc

from backend.app.database import make_engine
from backend.app.main import create_app
from backend.app.models import Base
from backend.app.sql_repository import SQLAlchemyRepository


class SignalReceiver:
    """An in-process OTLP endpoint tests the actual exporters and protobuf data."""

    def __init__(self, response_type):
        self.messages = []
        self.response_type = response_type

    def Export(self, request, context):
        self.messages.append(request)
        return self.response_type()


@pytest.fixture
def collector(monkeypatch):
    traces = SignalReceiver(trace_service_pb2.ExportTraceServiceResponse)
    metrics = SignalReceiver(metrics_service_pb2.ExportMetricsServiceResponse)
    logs = SignalReceiver(logs_service_pb2.ExportLogsServiceResponse)
    with ThreadPoolExecutor() as pool:
        server = grpc.server(pool)
        trace_service_pb2_grpc.add_TraceServiceServicer_to_server(traces, server)
        metrics_service_pb2_grpc.add_MetricsServiceServicer_to_server(metrics, server)
        logs_service_pb2_grpc.add_LogsServiceServicer_to_server(logs, server)
        port = server.add_insecure_port("127.0.0.1:0")
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", f"http://127.0.0.1:{port}")
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_INSECURE", "true")
        monkeypatch.setenv("OTEL_TRACES_SAMPLER", "parentbased_always_on")
        monkeypatch.setenv("OTEL_METRIC_EXPORT_INTERVAL", "60000")
        monkeypatch.setenv("OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE", "cumulative")
        monkeypatch.setenv("SPLITWISE_ENVIRONMENT", "development")
        server.start()
        try:
            yield traces.messages, metrics.messages, logs.messages
        finally:
            server.stop(0).wait()


def attributes(values):
    return {item.key: item.value.string_value for item in values}


def test_otlp_signals_and_correlated_redacted_failures(collector, tmp_path, monkeypatch):
    engine = make_engine(f"sqlite:///{tmp_path / 'telemetry.db'}")
    Base.metadata.create_all(engine)
    repository = SQLAlchemyRepository(engine)
    secret = "sensitive-field-never-exported"
    trace_id = "bbad4c127b95e32d2d885a0ccdc9321c"
    parent_id = "00f067aa0ba902b7"
    headers = {
        "traceparent": f"00-{trace_id}-{parent_id}-01",
        "authorization": f"Bearer {secret}",
    }
    try:
        with TestClient(create_app(repository)) as client:
            group = client.post(
                "/api/groups", json={"name": secret, "currency": "USD", "description": secret}
            )
            assert group.status_code == 201
            base_path = f"/api/groups/{group.json()['id']}"
            ids = [
                client.post(f"{base_path}/members", json={"name": name}).json()["id"]
                for name in ("Alice", "Bob")
            ]
            expense_url = f"{base_path}/expenses"
            expense = {
                "description": secret,
                "amount_minor": 1000,
                "payer_id": ids[0],
                "category": "Other",
                "date": "2026-10-20",
                "split_type": "equal",
                "split_values": dict.fromkeys(ids, 1),
            }
            assert client.post(expense_url, json=expense).status_code == 201
            assert client.post(expense_url, json={**expense, "amount_minor": 0}).status_code == 422
            assert client.get(f"{base_path}/balances").status_code == 200
            assert client.post(f"{base_path}/settlements", json={
                "from_member_id": ids[1],
                "to_member_id": ids[0],
                "amount_minor": 500,
                "date": "2026-10-20",
                "note": secret,
            }).status_code == 201

            def fail(*args, **kwargs):
                raise RuntimeError(secret)

            monkeypatch.setattr(repository, "save", fail)
            response = client.post(f"{expense_url}?unused={secret}", json=expense, headers=headers)
            assert response.status_code == 500
            assert secret not in response.text
            assert client.get("/api/health").status_code == 200
            assert client.get("/api/live").status_code == 200

        trace_requests, metric_requests, log_requests = collector
        assert trace_requests and metric_requests and log_requests
        for request, resource_key in (
            (trace_requests[-1], "resource_spans"),
            (metric_requests[-1], "resource_metrics"),
            (log_requests[-1], "resource_logs"),
        ):
            resource = getattr(request, resource_key)[0].resource
            labels = attributes(resource.attributes)
            assert labels["service.name"] == "splitwise-pro"
            assert labels["deployment.environment.name"] == "development"

        for request in trace_requests + metric_requests + log_requests:
            assert secret.encode() not in request.SerializeToString()
            assert group.json()["id"].encode() not in request.SerializeToString()

        spans = [
            span for request in trace_requests
            for resource in request.resource_spans
            for scope in resource.scope_spans
            for span in scope.spans
        ]
        failed_span = next(span for span in spans if span.parent_span_id.hex() == parent_id)
        assert failed_span.name == "POST /api/groups/{group_id}/expenses"
        assert failed_span.trace_id.hex() == trace_id
        assert failed_span.status.code == 2
        business_span = next(span for span in spans if span.parent_span_id == failed_span.span_id)
        assert business_span.name == "add_expense"
        assert any(
            span.name == "database.query" and span.parent_span_id == business_span.span_id
            for span in spans
        )
        logs = [
            log for request in log_requests
            for resource in request.resource_logs
            for scope in resource.scope_logs
            for log in scope.log_records
        ]
        error_log = next(log for log in logs if log.severity_text == "ERROR")
        assert error_log.time_unix_nano > 0
        assert error_log.trace_id == failed_span.trace_id
        assert error_log.span_id == failed_span.span_id
        assert attributes(error_log.attributes)["error.type"] == "RuntimeError"

        exported = {
            metric.name: metric for resource in metric_requests[-1].resource_metrics
            for scope in resource.scope_metrics
            for metric in scope.metrics
        }
        for metric_name in (
            "splitwise_groups_created", "splitwise_expenses_created",
            "splitwise_settlements_created", "splitwise_api_errors",
            "splitwise_expense_creation_failures",
        ):
            points = exported[metric_name].sum.data_points
            assert sum(point.as_int for point in points) == 1
            assert {attributes(point.attributes)["environment"] for point in points} == {"development"}
        for metric_name, sample_count in (
            ("splitwise_http_request_duration", 8),
            ("splitwise_expense_creation_duration", 3),
            ("splitwise_balance_calculation_duration", 1),
        ):
            metric = exported[metric_name]
            assert metric.unit == "s"
            points = metric.histogram.data_points
            assert sum(point.count for point in points) == sample_count
            assert all(1.0 in point.explicit_bounds for point in points)
    finally:
        engine.dispose()


def test_liveness_independent_of_database(tmp_path):
    engine = make_engine(f"sqlite:///{tmp_path / 'unmigrated.db'}")
    try:
        with TestClient(create_app(SQLAlchemyRepository(engine))) as client:
            assert client.get("/api/health").status_code == 503
            assert client.get("/api/live").json() == {"status": "ok"}
    finally:
        engine.dispose()
