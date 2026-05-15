#!/bin/sh
set -eu

export DATABASE_URL="${DATABASE_URL:-postgres://getkhafeefa:getkhafeefa@khafeefa_database:5432/getkhafeefa?sslmode=disable}"
export DATABASE_HOST="${DATABASE_HOST:-khafeefa_database}"

DATABASE_URL="$(python - <<'PY'
import os
from urllib.parse import urlsplit, urlunsplit

url = os.environ["DATABASE_URL"]
replacement_host = os.environ["DATABASE_HOST"]
parts = urlsplit(url)

if parts.hostname in {"localhost", "127.0.0.1", "::1"}:
    username = parts.username or ""
    password = parts.password or ""
    auth = username
    if password:
        auth = f"{auth}:{password}"
    if auth:
        auth = f"{auth}@"

    port = f":{parts.port}" if parts.port else ""
    parts = parts._replace(netloc=f"{auth}{replacement_host}{port}")
    url = urlunsplit(parts)

print(url)
PY
)"
export DATABASE_URL
echo "Using database host: ${DATABASE_HOST}"

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
