"""Offline ledger transfer. Stop BOTH applications and migrate the target schema first.

python -m backend.scripts.migrate_sqlite_to_postgres --source backend/splitwise.db \
    --backup /safe/location/ledger-backup.db

DATABASE_URL must identify an empty PostgreSQL database already at Alembic head.
The backup is retained even on failure. No source or target rows are deleted.
Rollback: stop the PostgreSQL app and point DATABASE_URL back to the original
SQLite file (or its backup). Writes made after cutover require reconciliation;
never overwrite either database to perform rollback.
"""
import argparse
import json
import os
from pathlib import Path
import sqlite3

from sqlalchemy import select, text

from backend.app.database import make_engine
from backend.app.domain import balances
from backend.app.models import Base

TABLES = list(Base.metadata.sorted_tables)


def read_rows(connection):
    return {
        table.name: [dict(row) for row in connection.execute(select(table)).mappings()]
        for table in TABLES
    }


def validate_and_reconcile(rows):
    groups = {r['id'] for r in rows['groups']}
    members = {r['id']: r for r in rows['members']}
    expenses = {r['id']: {**r, 'shares': []} for r in rows['expenses']}
    for member in members.values():
        if member['group_id'] not in groups:
            raise ValueError('Member references an absent group')
    for share in rows['expense_shares']:
        expense = expenses.get(share['expense_id'])
        member = members.get(share['member_id'])
        if not expense or not member or member['group_id'] != expense['group_id']:
            raise ValueError('Invalid expense share reference')
        expense['shares'].append(share)
    for expense in expenses.values():
        payer = members.get(expense['payer_id'])
        if not payer or payer['group_id'] != expense['group_id']:
            raise ValueError('Invalid payer reference')
        if sum(s['amount_minor'] for s in expense['shares']) != expense['amount_minor']:
            raise ValueError('Expense shares do not reconcile')
    for settlement in rows['settlements']:
        for key in ('from_member_id', 'to_member_id'):
            member = members.get(settlement[key])
            if not member or member['group_id'] != settlement['group_id']:
                raise ValueError('Invalid settlement reference')
    result = {}
    for group in sorted(groups):
        result[group] = balances(
            [r for r in members.values() if r['group_id'] == group],
            [r for r in expenses.values() if r['group_id'] == group],
            [r for r in rows['settlements'] if r['group_id'] == group],
        )
        if sum(r['net_minor'] for r in result[group]['members']) != 0:
            raise ValueError('Group balances do not sum to zero')
    return result


def transfer(source_engine, target_engine):
    """Copy and verify inside one target transaction; any failure rolls back all rows."""
    with source_engine.connect() as source:
        rows = read_rows(source)
        revision = source.execute(text('SELECT version_num FROM alembic_version')).scalar_one()
    before = validate_and_reconcile(rows)
    with target_engine.begin() as target:
        if target.dialect.name == 'postgresql':
            target.execute(text('LOCK TABLE groups, members, expenses, expense_shares, settlements IN ACCESS EXCLUSIVE MODE'))
        target_revision = target.execute(text('SELECT version_num FROM alembic_version')).scalar_one()
        if revision != target_revision:
            raise ValueError('Source and target Alembic revisions must match')
        if any(target.execute(select(table).limit(1)).first() for table in TABLES):
            raise ValueError('Target ledger must be empty; no data was replaced')
        for table in TABLES:
            if rows[table.name]:
                target.execute(table.insert(), rows[table.name])
        copied = read_rows(target)
        # Full row comparison also verifies IDs, relationships, dates and split values.
        canonical = lambda values: sorted(json.dumps(r, sort_keys=True) for r in values)
        if any(canonical(rows[t.name]) != canonical(copied[t.name]) for t in TABLES):
            raise ValueError('Copied rows differ from the backup')
        if validate_and_reconcile(copied) != before:
            raise ValueError('Balance reconciliation failed')
    return {name: len(values) for name, values in rows.items()}


def migrate(source_path, backup_path, target_url):
    source_path, backup_path = Path(source_path).resolve(), Path(backup_path).resolve()
    if not source_path.is_file():
        raise ValueError('Source SQLite file does not exist')
    if backup_path == source_path or backup_path.exists():
        raise ValueError('Backup must be a new path separate from the source')
    target = make_engine(target_url)
    try:
        if target.dialect.name != 'postgresql':
            raise ValueError('Target must be PostgreSQL')
        # Exclusive creation avoids overwriting an existing backup; mode 0600 protects data.
        fd = os.open(backup_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
        with sqlite3.connect(source_path.as_uri() + '?mode=ro', uri=True) as source:
            with sqlite3.connect(backup_path) as backup:
                source.backup(backup)
                if backup.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                    raise ValueError('SQLite backup integrity check failed')
                if backup.execute('PRAGMA foreign_key_check').fetchall():
                    raise ValueError('SQLite backup contains invalid foreign keys')
        snapshot = make_engine('sqlite:///' + str(backup_path))
        try:
            return transfer(snapshot, target)
        finally:
            snapshot.dispose()
    finally:
        target.dispose()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--backup', required=True)
    args = parser.parse_args()
    target_url = os.environ.get('DATABASE_URL')
    if not target_url:
        parser.error('Set DATABASE_URL to the empty migrated PostgreSQL target')
    try:
        counts = migrate(args.source, args.backup, target_url)
    except Exception:
        # Driver exceptions can contain passwords or financial records: never print them.
        parser.exit(1, 'Migration failed; target transaction rolled back. Retain the backup and inspect securely.\n')
    print(json.dumps({'verified_row_counts': counts, 'balances_reconciled': True}))


if __name__ == '__main__':
    main()
