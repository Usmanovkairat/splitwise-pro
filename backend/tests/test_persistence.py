import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.request
import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import inspect, select, event
from sqlalchemy.orm import Session
from backend.app.database import make_engine
from backend.app.models import Base, Group, Member, Expense, ExpenseShare, Settlement
from backend.app.sql_repository import SQLAlchemyRepository
from backend.app.domain import DomainError
from backend.app.service import Service


@pytest.fixture
def database(tmp_path):
    url = f"sqlite:///{tmp_path/'ledger.db'}"
    cfg = Config("backend/alembic.ini")
    cfg.set_main_option("sqlalchemy.url", url)
    cfg.attributes["explicit_url"] = True
    command.upgrade(cfg, "head")
    engine = make_engine(url)
    try:
        yield engine, cfg
    finally:
        engine.dispose()


def ledger(engine):
    repo = SQLAlchemyRepository(engine)
    service = Service(repo)
    g = service.create_group(dict(name="Trip", currency="USD", description=""))
    a = service.add_member(g["id"], {"name": "Alice"})
    b = service.add_member(g["id"], {"name": "Bob"})
    expense = service.expense(
        g["id"],
        dict(
            description="Dinner",
            amount_minor=1001,
            payer_id=a["id"],
            category="Food",
            date="2026-10-20",
            split_type="equal",
            split_values={a["id"]: 1, b["id"]: 1},
        ),
    )
    return repo, service, g, a, b, expense


def test_migration_matches_metadata_and_roundtrip(database):
    engine, cfg = database
    with engine.connect() as connection:
        assert (
            compare_metadata(MigrationContext.configure(connection), Base.metadata)
            == []
        )
    assert set(inspect(engine).get_table_names()) == {
        "alembic_version",
        "groups",
        "members",
        "expenses",
        "expense_shares",
        "settlements",
    }
    command.downgrade(cfg, "base")
    assert inspect(engine).get_table_names() == ["alembic_version"]
    command.upgrade(cfg, "head")
    assert "expense_shares" in inspect(engine).get_table_names()


def test_fk_enforcement_and_failed_expense_update_rolls_back(database):
    engine, _ = database
    repo, service, g, a, b, expense = ledger(engine)
    with pytest.raises(DomainError):
        repo.save("members", dict(id="bad", group_id="nonexistent", name="Ghost"))
    assert repo.get("members", "bad") is None
    broken = {
        **expense,
        "amount_minor": 999,
        "split_values": {"ghost": 1},
        "shares": [{"member_id": "ghost", "amount_minor": 999}],
    }
    with pytest.raises(DomainError):
        repo.save("expenses", broken)
    assert repo.get("expenses", expense["id"]) == expense
    assert service.balances(g["id"])["total_minor"] == 1001


def test_group_delete_transaction_rolls_back_on_injected_failure(database):
    engine, _ = database
    repo, service, g, a, b, expense = ledger(engine)

    def fail_members(connection, cursor, statement, parameters, context, executemany):
        if statement.startswith("DELETE FROM members"):
            raise RuntimeError("Injected storage failure")

    event.listen(engine, "before_cursor_execute", fail_members)
    try:
        with pytest.raises(RuntimeError):
            service.delete_group(g["id"])
    finally:
        event.remove(engine, "before_cursor_execute", fail_members)
    assert repo.get("groups", g["id"]) is not None
    assert repo.get("expenses", expense["id"]) == expense
    service.delete_group(g["id"])
    with Session(engine) as session:
        for model in (Group, Member, Expense, ExpenseShare, Settlement):
            assert session.scalars(select(model)).all() == []


def test_database_uniqueness_protects_casefold_names(database):
    engine, _ = database
    repo, service, g, a, b, expense = ledger(engine)
    with pytest.raises(DomainError):
        repo.save("members", dict(id="duplicate", group_id=g["id"], name="ALICE"))
    assert len(repo.list("members", g["id"])) == 2


def test_actual_uvicorn_process_restart_retains_ledger(tmp_path):
    root = Path(__file__).resolve().parents[2]
    url = f"sqlite:///{tmp_path/'restart.db'}"
    env = {**os.environ, "DATABASE_URL": url, "SPLITWISE_STORAGE": "sqlite"}
    subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            "backend/alembic.ini",
            "upgrade",
            "head",
        ],
        cwd=root,
        env=env,
        check=True,
        capture_output=True,
    )
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    base = f"http://127.0.0.1:{port}"

    def request(path, data=None):
        req = urllib.request.Request(
            base + path,
            data=json.dumps(data).encode() if data is not None else None,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            return json.load(response)

    def start():
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "backend.app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
            ],
            cwd=root,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(100):
            if process.poll() is not None:
                raise RuntimeError("uvicorn exited before health check")
            try:
                if request("/api/health")["storage"] == "sqlite":
                    return process
            except OSError:
                time.sleep(0.05)
        process.terminate()
        process.wait(timeout=5)
        raise RuntimeError("uvicorn did not start")

    process = start()
    try:
        g = request(
            "/api/groups",
            dict(name="Persistent", currency="EUR", description="Restart verified"),
        )
        path = f"/api/groups/{g['id']}"
        a = request(path + "/members", {"name": "Alice"})
        b = request(path + "/members", {"name": "Bob"})
        request(
            path + "/expenses",
            dict(
                description="Hotel",
                amount_minor=1000,
                payer_id=a["id"],
                category="Travel",
                date="2026-10-20",
                split_type="exact",
                split_values={a["id"]: 500, b["id"]: 500},
            ),
        )
        request(
            path + "/settlements",
            dict(
                from_member_id=b["id"],
                to_member_id=a["id"],
                amount_minor=200,
                date="2026-10-20",
                note="Partial",
            ),
        )
        before = {
            key: request(path + "/" + key)
            for key in ("members", "expenses", "settlements", "balances", "analytics")
        }
    finally:
        process.terminate()
        process.wait(timeout=5)
    process = start()
    try:
        assert request(path) == g
        assert {key: request(path + "/" + key) for key in before} == before
        assert request(path + "/analytics")["outstanding_minor"] == 300
    finally:
        process.terminate()
        process.wait(timeout=5)


def test_explicit_demo_seed_refuses_existing_workspace(database):
    from backend.scripts.seed_demo import seed_demo

    engine, _ = database
    repo = SQLAlchemyRepository(engine)
    group = seed_demo(repo)
    service = Service(repo)
    assert len(repo.list("groups")) == 1
    assert len(repo.list("members", group["id"])) == 4
    assert len(repo.list("expenses", group["id"])) == 7
    assert len(repo.list("settlements", group["id"])) == 1
    assert {e["split_type"] for e in repo.list("expenses", group["id"])} == {
        "equal",
        "exact",
        "percentage",
    }
    assert (
        sum(row["net_minor"] for row in service.balances(group["id"])["members"]) == 0
    )
    before = {
        kind: repo.list(kind)
        for kind in ("groups", "members", "expenses", "settlements")
    }
    with pytest.raises(ValueError, match="empty workspace"):
        seed_demo(repo)
    assert {kind: repo.list(kind) for kind in before} == before
