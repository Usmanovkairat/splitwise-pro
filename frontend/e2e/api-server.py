"""Isolated migrated SQLite server fixture for browser integration tests."""
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

root = Path(__file__).resolve().parents[2]
with TemporaryDirectory(prefix='splitwise-e2e-') as directory:
    env = {**os.environ, 'DATABASE_URL': 'sqlite:///' + directory + '/ledger.db', 'SPLITWISE_STORAGE': 'sqlite'}
    subprocess.run([sys.executable, '-m', 'alembic', '-c', 'backend/alembic.ini', 'upgrade', 'head'], cwd=root, env=env, check=True)
    process = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'backend.app.main:app', '--host', '127.0.0.1', '--port', '8000'], cwd=root, env=env)
    try:
        process.wait()
    finally:
        process.terminate()
        process.wait(timeout=5)
