"""Isolated migrated SQLite server fixture for browser integration tests."""
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import uvicorn

root = Path(__file__).resolve().parents[2]
with TemporaryDirectory(prefix='splitwise-e2e-') as directory:
    env = {**os.environ, 'DATABASE_URL': 'sqlite:///' + directory + '/ledger.db', 'SPLITWISE_STORAGE': 'sqlite'}
    subprocess.run([sys.executable, '-m', 'alembic', '-c', 'backend/alembic.ini', 'upgrade', 'head'], cwd=root, env=env, check=True)
    # Keep the server in this fixture process so Playwright shutdown cannot
    # leave a child API process holding the port or temporary database open.
    os.environ.update(env)
    sys.path.insert(0, str(root))
    uvicorn.run('backend.app.main:app', host='127.0.0.1', port=8000)
