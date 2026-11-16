"""Run: uvicorn backend.app.main:app --host 127.0.0.1 --port 8000."""

import os
from contextlib import asynccontextmanager, contextmanager
from datetime import date
from threading import RLock
from fastapi import FastAPI, Query, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from opentelemetry.trace import StatusCode
from .domain import DomainError
from .repository import MemoryRepository
from .service import Service
from .telemetry import TelemetryMiddleware, create_telemetry
from .schemas import GroupInput, GroupUpdate, MemberInput, ExpenseInput, SettlementInput


def create_app(repository=None, storage=None):
    @asynccontextmanager
    async def lifespan(app):
        telemetry = create_telemetry()
        app.state.telemetry = telemetry
        remove_database_hooks = None
        try:
            if telemetry is not None:
                engine = getattr(app.state.repository, "engine", None)
                remove_database_hooks = telemetry.instrument_database(engine)
            yield
        finally:
            app.state.telemetry = None
            if remove_database_hooks is not None:
                remove_database_hooks()
            if telemetry is not None:
                telemetry.shutdown()

    app = FastAPI(title="SplitWise Pro API", version="1.0.0", lifespan=lifespan)
    app.state.telemetry = None
    storage = storage or os.getenv("SPLITWISE_STORAGE", "sqlite")
    if repository is None:
        if storage == "memory":
            repository = MemoryRepository()
        elif storage == "sqlite":
            from .database import make_engine
            from .sql_repository import SQLAlchemyRepository

            repository = SQLAlchemyRepository(make_engine())
        else:
            raise ValueError("SPLITWISE_STORAGE must be memory or sqlite")
    app.state.repository = repository
    app.state.storage = storage
    service = Service(app.state.repository)
    lock = RLock()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type"],
    )

    app.add_middleware(TelemetryMiddleware, state=app.state)

    @contextmanager
    def business_span(operation):
        telemetry = app.state.telemetry
        if telemetry is None:
            yield
            return
        with telemetry.tracer.start_as_current_span(
            operation, record_exception=False, set_status_on_exception=False,
        ) as span:
            try:
                yield
            except DomainError:
                raise
            except Exception as exc:
                span.set_attribute("error.type", type(exc).__name__)
                span.set_status(StatusCode.ERROR)
                raise

    @app.exception_handler(DomainError)
    async def domain_error(request, exc):
        return JSONResponse(status_code=exc.status, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        details = "; ".join(
            ".".join(str(x) for x in e["loc"]) + ": " + e["msg"] for e in exc.errors()
        )
        return JSONResponse(status_code=422, content={"detail": details})

    @app.get("/api/live", include_in_schema=False)
    def liveness():
        return {"status": "ok"}

    @app.get("/api/health")
    def health():
        engine = getattr(app.state.repository, "engine", None)
        if engine is not None:
            from sqlalchemy import select
            from .models import Group
            try:
                with engine.connect() as connection:
                    connection.execute(select(Group.id).limit(1))
            except Exception:
                return JSONResponse(status_code=503, content={"status": "unavailable"})
        return dict(status="ok", storage=app.state.storage,
                    database=engine.dialect.name if engine is not None else "memory")

    @app.get("/api/groups")
    def groups():
        with lock:
            return app.state.repository.list("groups")

    @app.post("/api/groups", status_code=201)
    def create_group(data: GroupInput):
        with business_span("create_group"), lock:
            return service.create_group(data.model_dump())

    @app.get("/api/groups/{group_id}")
    def group(group_id: str):
        with lock:
            return service.group(group_id)

    @app.put("/api/groups/{group_id}")
    def update_group(group_id: str, data: GroupUpdate):
        with lock:
            return service.update_group(group_id, data.model_dump())

    @app.delete("/api/groups/{group_id}", status_code=204)
    def delete_group(group_id: str):
        with lock:
            service.delete_group(group_id)
        return Response(status_code=204)

    @app.get("/api/groups/{group_id}/members")
    def members(group_id: str):
        with lock:
            return service.list("members", group_id)

    @app.post("/api/groups/{group_id}/members", status_code=201)
    def add_member(group_id: str, data: MemberInput):
        with lock:
            return service.add_member(group_id, data.model_dump())

    @app.delete("/api/groups/{group_id}/members/{member_id}", status_code=204)
    def remove_member(group_id: str, member_id: str):
        with lock:
            service.remove_member(group_id, member_id)
        return Response(status_code=204)

    @app.get("/api/groups/{group_id}/expenses")
    def expenses(
        group_id: str,
        q: str | None = None,
        category: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ):
        with lock:
            if date_from and date_to and date_from > date_to:
                raise DomainError("Start date must not follow end date")
            rows = service.list("expenses", group_id)
            return sorted(
                [
                    e
                    for e in rows
                    if (not q or q.casefold() in e["description"].casefold())
                    and (not category or e["category"] == category)
                    and (not date_from or e["date"] >= date_from.isoformat())
                    and (not date_to or e["date"] <= date_to.isoformat())
                ],
                key=lambda e: (e["date"], e["id"]),
                reverse=True,
            )

    @app.post("/api/groups/{group_id}/expenses", status_code=201)
    def add_expense(group_id: str, data: ExpenseInput):
        with business_span("add_expense"), lock:
            return service.expense(group_id, data.model_dump(mode="json"))

    @app.put("/api/groups/{group_id}/expenses/{expense_id}")
    def update_expense(group_id: str, expense_id: str, data: ExpenseInput):
        with lock:
            return service.expense(group_id, data.model_dump(mode="json"), expense_id)

    @app.delete("/api/groups/{group_id}/expenses/{expense_id}", status_code=204)
    def delete_expense(group_id: str, expense_id: str):
        with lock:
            service.delete_expense(group_id, expense_id)
        return Response(status_code=204)

    @app.get("/api/groups/{group_id}/balances")
    def balances(group_id: str):
        with business_span("balances"), lock:
            return service.balances(group_id)

    @app.get("/api/groups/{group_id}/settlements")
    def settlements(group_id: str):
        with lock:
            return sorted(
                service.list("settlements", group_id),
                key=lambda s: (s["date"], s["id"]),
                reverse=True,
            )

    @app.post("/api/groups/{group_id}/settlements", status_code=201)
    def add_settlement(group_id: str, data: SettlementInput):
        with business_span("add_settlement"), lock:
            return service.settlement(group_id, data.model_dump(mode="json"))

    @app.get("/api/groups/{group_id}/analytics")
    def analytics(group_id: str):
        with lock:
            return service.analytics(group_id)

    return app


app = create_app()
