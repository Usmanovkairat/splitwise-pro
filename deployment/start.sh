#!/bin/sh
set -eu
python -m alembic -c backend/alembic.ini upgrade head
exec uvicorn backend.app.production:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 1
