"""Transfer safety regression; set TEST_POSTGRES_URL for real PostgreSQL verification."""
import os
import uuid

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import event, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext

from backend.app.database import make_engine
from backend.app.models import Base
from backend.app.service import Service
from backend.app.sql_repository import SQLAlchemyRepository
from backend.scripts.migrate_sqlite_to_postgres import transfer, read_rows, validate_and_reconcile, migrate


def setup_database(url):
    cfg = Config('backend/alembic.ini')
    cfg.set_main_option('sqlalchemy.url', url.replace('%', '%%'))
    cfg.attributes['explicit_url'] = True
    command.upgrade(cfg, 'head')
    return make_engine(url)


def seed(engine):
    service = Service(SQLAlchemyRepository(engine))
    group = service.create_group(dict(name='Transfer', currency='KZT', description=''))
    a = service.add_member(group['id'], {'name': 'A'})
    b = service.add_member(group['id'], {'name': 'B'})
    service.expense(group['id'], dict(description='Food', amount_minor=1001,
        payer_id=a['id'], category='Food', date='2026-11-02', split_type='equal',
        split_values={a['id']: 1, b['id']: 1}))
    service.settlement(group['id'], dict(from_member_id=b['id'], to_member_id=a['id'],
        amount_minor=100, date='2026-11-02', note='Partial'))


@pytest.fixture
def databases(tmp_path):
    source = setup_database(f'sqlite:///{tmp_path / "source.db"}')
    target = setup_database(f'sqlite:///{tmp_path / "target.db"}')
    seed(source)
    yield source, target
    source.dispose()
    target.dispose()


def test_transfer_preserves_every_row_and_partial_repayment(databases):
    source, target = databases
    assert transfer(source, target) == dict(groups=1, members=2, expenses=1, expense_shares=2, settlements=1)
    with source.connect() as a, target.connect() as b:
        left, right = read_rows(a), read_rows(b)
        assert left == right
        assert validate_and_reconcile(left) == validate_and_reconcile(right)


def test_transfer_refuses_nonempty_target_without_changes(databases):
    source, target = databases
    seed(target)
    with target.connect() as connection:
        before = read_rows(connection)
    with pytest.raises(ValueError, match='empty'):
        transfer(source, target)
    with target.connect() as connection:
        assert read_rows(connection) == before


def test_transfer_failure_rolls_back_all_prior_inserts(databases):
    source, target = databases
    def fail(connection, cursor, statement, parameters, context, executemany):
        if statement.startswith('INSERT INTO expense_shares'):
            raise RuntimeError('Injected copy failure')
    event.listen(target, 'before_cursor_execute', fail)
    try:
        with pytest.raises(RuntimeError, match='Injected'):
            transfer(source, target)
    finally:
        event.remove(target, 'before_cursor_execute', fail)
    with target.connect() as connection:
        assert all(not rows for rows in read_rows(connection).values())


def test_cross_group_reference_rejected_before_copy(databases):
    source, target = databases
    with source.connect() as connection:
        rows = read_rows(connection)
    rows['members'][0]['group_id'] = 'missing'
    with pytest.raises(ValueError, match='absent group'):
        validate_and_reconcile(rows)


def test_cli_refuses_existing_backup_without_overwriting(tmp_path):
    source = tmp_path / 'source.db'
    source.touch()
    backup = tmp_path / 'backup.db'
    backup.write_bytes(b'keep me')
    with pytest.raises(ValueError, match='new path'):
        migrate(source, backup, 'postgresql+psycopg://localhost/example')
    assert backup.read_bytes() == b'keep me'


@pytest.fixture
def postgres_database():
    if not os.getenv('TEST_POSTGRES_URL'):
        pytest.skip('TEST_POSTGRES_URL not configured')
    admin = make_engine(os.environ['TEST_POSTGRES_URL'])
    schema = 'migration_test_' + uuid.uuid4().hex
    with admin.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    url = make_url(os.environ['TEST_POSTGRES_URL']).update_query_dict({'options': f'-csearch_path={schema}'})
    target = None
    try:
        target = setup_database(url.render_as_string(hide_password=False))
        yield target
    finally:
        if target is not None:
            target.dispose()
        with admin.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()


def test_transfer_to_real_postgres(tmp_path, postgres_database):
    source = setup_database(f'sqlite:///{tmp_path / "postgres-source.db"}')
    seed(source)
    try:
        assert transfer(source, postgres_database)['expense_shares'] == 2
        with source.connect() as a, postgres_database.connect() as b:
            assert validate_and_reconcile(read_rows(a)) == validate_and_reconcile(read_rows(b))
            assert compare_metadata(MigrationContext.configure(b), Base.metadata) == []
        # IDs, references and rounded amounts survive a fresh repository instance.
        assert SQLAlchemyRepository(source).list('expenses') == SQLAlchemyRepository(postgres_database).list('expenses')
    finally:
        source.dispose()


def test_postgres_enforces_foreign_keys_and_rolls_back(postgres_database):
    table = Base.metadata.tables['members']
    with pytest.raises(IntegrityError):
        with postgres_database.begin() as connection:
            connection.execute(table.insert(), dict(id='orphan', group_id='missing', name='Ghost', normalized_name='ghost'))
    with postgres_database.connect() as connection:
        assert connection.execute(select(table)).all() == []


def test_real_postgres_migration_creates_verified_backup(tmp_path, postgres_database):
    source_path = tmp_path / 'original.db'
    source = setup_database(f'sqlite:///{source_path}')
    seed(source)
    with source.connect() as connection:
        before = read_rows(connection)
    source.dispose()
    backup = tmp_path / 'backup.db'
    counts = migrate(source_path, backup, postgres_database.url.render_as_string(hide_password=False))
    assert counts['settlements'] == 1
    assert backup.stat().st_mode & 0o777 == 0o600
    for path in (source_path, backup):
        engine = make_engine(f'sqlite:///{path}')
        with engine.connect() as connection:
            assert read_rows(connection) == before
        engine.dispose()


def test_revision_mismatch_leaves_target_empty(databases):
    source, target = databases
    with target.begin() as connection:
        connection.execute(text("UPDATE alembic_version SET version_num = 'different'"))
    with pytest.raises(ValueError, match='revisions'):
        transfer(source, target)
    with target.connect() as connection:
        assert all(not rows for rows in read_rows(connection).values())
