"""Isolated migrated database fixture for real browser integration tests.

QA_DATABASE_URL may point to a dedicated PostgreSQL test database. The fixture
creates a unique schema and removes only that schema on exit. SQLite is default.
Never set QA_DATABASE_URL to a production database.
"""
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from uuid import uuid4

import uvicorn
from sqlalchemy import create_engine, text

root = Path(__file__).resolve().parents[2]


def serve(url):
    env = {**os.environ, 'DATABASE_URL': url, 'SPLITWISE_STORAGE': 'sqlite'}
    subprocess.run([sys.executable, '-m', 'alembic', '-c', 'backend/alembic.ini', 'upgrade', 'head'], cwd=root, env=env, check=True)
    os.environ.update(env)
    sys.path.insert(0, str(root))
    uvicorn.run('backend.app.main:app', host='127.0.0.1', port=8000)


url = os.getenv('QA_DATABASE_URL')
if url:
    if not url.startswith(('postgresql://', 'postgresql+psycopg://')):
        raise SystemExit('QA_DATABASE_URL must use PostgreSQL; omit it for temporary SQLite.')
    from sqlalchemy.engine import make_url
    base_url = make_url(url)
    if base_url.drivername == 'postgresql':
        base_url = base_url.set(drivername='postgresql+psycopg')
    schema = 'e2e_' + uuid4().hex
    engine = create_engine(base_url)
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA {schema}'))
    scoped = base_url.update_query_dict({'options': f'-csearch_path={schema}'}).render_as_string(hide_password=False)
    try:
        serve(scoped)
    finally:
        with engine.begin() as connection:
            connection.execute(text(f'DROP SCHEMA {schema} CASCADE'))
        engine.dispose()
else:
    with TemporaryDirectory(prefix='splitwise-e2e-') as directory:
        serve('sqlite:///' + directory + '/ledger.db')
