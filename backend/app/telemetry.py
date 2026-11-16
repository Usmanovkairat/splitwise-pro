"""Privacy-preserving OpenTelemetry signals for the SplitWise API."""

import os
from time import perf_counter, time_ns

from opentelemetry._logs import SeverityNumber
from opentelemetry.trace import SpanKind, StatusCode, get_current_span
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


SERVICE_NAME = "splitwise-pro"
CREATE_METRICS = {
    "create_group": "splitwise_groups_created",
    "add_expense": "splitwise_expenses_created",
    "add_settlement": "splitwise_settlements_created",
}
DURATION_METRICS = {
    "add_expense": "splitwise_expense_creation_duration",
    "balances": "splitwise_balance_calculation_duration",
}
BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 10.0)
PROPAGATOR = TraceContextTextMapPropagator()
PROBE_PATHS = {"/api/health", "/api/live"}


class Telemetry:
    def __init__(self, environment, tracer_provider, meter_provider, logger_provider):
        self.environment = environment
        self.environment_attributes = {"environment": environment}
        self.tracer = tracer_provider.get_tracer(SERVICE_NAME)
        self.logger = logger_provider.get_logger(SERVICE_NAME)
        meter = meter_provider.get_meter(SERVICE_NAME)
        self.requests = meter.create_counter("splitwise_http_requests")
        self.request_duration = meter.create_histogram(
            "splitwise_http_request_duration", unit="s",
            explicit_bucket_boundaries_advisory=BUCKETS,
        )
        self.errors = meter.create_counter("splitwise_api_errors")
        self.expense_failures = meter.create_counter("splitwise_expense_creation_failures")
        self.creations = {
            operation: meter.create_counter(name)
            for operation, name in CREATE_METRICS.items()
        }
        self.durations = {
            operation: meter.create_histogram(
                name, unit="s", explicit_bucket_boundaries_advisory=BUCKETS
            )
            for operation, name in DURATION_METRICS.items()
        }
        self.providers = (meter_provider, tracer_provider, logger_provider)
        # Give each process a zero baseline before its first sparse event.
        for counter in (self.errors, self.expense_failures, *self.creations.values()):
            counter.add(0, self.environment_attributes)

    def shutdown(self):
        for provider in self.providers:
            provider.shutdown()

    def instrument_database(self, engine):
        if engine is None:
            return

        from sqlalchemy import event

        @event.listens_for(engine, "before_cursor_execute")
        def begin_query(connection, cursor, statement, parameters, execution, executemany):
            if not get_current_span().get_span_context().is_valid:
                return
            execution.splitwise_span = self.tracer.start_span(
                "database.query", kind=SpanKind.CLIENT,
                attributes={"db.system.name": engine.dialect.name},
            )

        @event.listens_for(engine, "after_cursor_execute")
        def end_query(connection, cursor, statement, parameters, execution, executemany):
            span = getattr(execution, "splitwise_span", None)
            if span is not None:
                span.end()

        @event.listens_for(engine, "handle_error")
        def fail_query(error):
            span = getattr(error.execution_context, "splitwise_span", None)
            if span is not None:
                span.set_status(StatusCode.ERROR)
                span.set_attribute("error.type", type(error.original_exception).__name__)
                span.end()

        def uninstrument():
            event.remove(engine, "before_cursor_execute", begin_query)
            event.remove(engine, "after_cursor_execute", end_query)
            event.remove(engine, "handle_error", fail_query)

        return uninstrument

    def record_request(self, operation, status_code, duration, error_type):
        attributes = {
            "environment": self.environment,
            "operation": operation,
            "status_code": str(status_code),
        }
        self.requests.add(1, attributes)
        self.request_duration.record(duration, attributes)
        if status_code >= 500:
            self.errors.add(1, self.environment_attributes)
            if operation == "add_expense":
                self.expense_failures.add(1, self.environment_attributes)
        if status_code == 201 and operation in self.creations:
            self.creations[operation].add(1, self.environment_attributes)
        if operation in self.durations:
            self.durations[operation].record(duration, {
                "environment": self.environment,
                "result": "success" if status_code < 400 else "failure",
            })
        if error_type:
            attributes["error.type"] = error_type
        failure = status_code >= 500
        self.logger.emit(
            timestamp=time_ns(),
            severity_number=SeverityNumber.ERROR if failure else SeverityNumber.INFO,
            severity_text="ERROR" if failure else "INFO",
            body="API request failed" if failure else "API request completed",
            attributes=attributes,
        )


def create_telemetry():
    if not os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
        return None

    from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk._logs import LoggerProvider
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    environment = os.getenv("SPLITWISE_ENVIRONMENT", "local")
    if environment not in {"development", "production", "local"}:
        raise ValueError("Invalid SPLITWISE_ENVIRONMENT")
    resource = Resource.create({
        "service.name": SERVICE_NAME,
        "deployment.environment.name": environment,
    })
    tracer_provider = TracerProvider(resource=resource, shutdown_on_exit=False)
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter())],
        shutdown_on_exit=False,
    )
    logger_provider = LoggerProvider(resource=resource, shutdown_on_exit=False)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    return Telemetry(environment, tracer_provider, meter_provider, logger_provider)


class TelemetryMiddleware:
    def __init__(self, app, state):
        self.app = app
        self.state = state

    async def __call__(self, scope, receive, send):
        telemetry = self.state.telemetry
        if (
            telemetry is None or scope["type"] != "http"
            or not scope["path"].startswith("/api/") or scope["path"] in PROBE_PATHS
        ):
            await self.app(scope, receive, send)
            return

        headers = {
            name.decode("ascii"): value.decode("latin1")
            for name, value in scope["headers"]
            if name == b"traceparent"
        }
        started = perf_counter()
        status_code = 500
        error_type = None
        response_started = False

        async def capture(message):
            nonlocal status_code, response_started
            if message["type"] == "http.response.start":
                status_code = message["status"]
                response_started = True
            await send(message)

        with telemetry.tracer.start_as_current_span(
            "api.request", context=PROPAGATOR.extract(headers), kind=SpanKind.SERVER,
            record_exception=False, set_status_on_exception=False,
        ) as span:
            try:
                await self.app(scope, receive, capture)
            except Exception as exc:
                error_type = type(exc).__name__
                if response_started:
                    raise RuntimeError("API response interrupted") from None
                await capture({
                    "type": "http.response.start", "status": 500,
                    "headers": [(b"content-type", b"application/json")],
                })
                await capture({
                    "type": "http.response.body",
                    "body": b'{"detail":"Internal Server Error"}',
                })
            finally:
                route = scope.get("route")
                operation = getattr(route, "name", "unmatched")
                if route and getattr(route, "path", "").startswith("/api/"):
                    span.set_attribute("http.route", route.path)
                    span.update_name(f"{scope['method']} {route.path}")
                else:
                    operation = "unmatched"
                span.set_attribute("http.response.status_code", status_code)
                span.set_attribute("splitwise.operation", operation)
                if status_code >= 500 or error_type:
                    span.set_status(StatusCode.ERROR)
                if error_type:
                    span.set_attribute("error.type", error_type)
                telemetry.record_request(
                    operation, status_code, perf_counter() - started, error_type
                )
