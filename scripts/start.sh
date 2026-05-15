#!/bin/sh
set -eu

python - <<'PY'
import os
import time

import psycopg2

database_url = os.environ.get("DATABASE_URL", "")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

last_error = None
for attempt in range(1, 31):
    try:
        connection = psycopg2.connect(database_url)
        connection.close()
        print("Database is ready.")
        break
    except Exception as error:
        last_error = error
        print(f"Waiting for database ({attempt}/30): {error}")
        time.sleep(2)
else:
    raise SystemExit(f"Database did not become ready: {last_error}")
PY

if [ "${RUN_MIGRATIONS_ON_START:-true}" = "true" ]; then
  alembic upgrade head
fi

exec gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT:-8000}
