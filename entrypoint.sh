#!/bin/sh
set -e

# Wait for Postgres (tries for up to 60s)
if [ -z "$DATABASE_URL" ]; then
  echo "DATABASE_URL not set. Exiting."
  exit 1
fi

echo "Waiting for Postgres..."
python - <<'PY'
import os, time, sys
import psycopg2
db_url = os.environ.get("DATABASE_URL")
for i in range(60):
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print("Postgres is available")
        sys.exit(0)
    except Exception as e:
        print("Postgres still unavailable, retrying...", e)
        time.sleep(1)
print("Postgres connection failed after retries.")
sys.exit(1)
PY

# apply migrations and create static dir
python manage.py makemigrations || true
python manage.py migrate --noinput || true
python manage.py collectstatic --noinput || true

exec "$@"
