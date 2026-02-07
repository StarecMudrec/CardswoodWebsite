#!/bin/sh
set -e

echo "Waiting for database..."
until python -c "
import os, sys
uri = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:postgres@db:5432/cards').replace('postgresql+psycopg2://', 'postgresql://')
import psycopg2
try:
    psycopg2.connect(uri).close()
    sys.exit(0)
except Exception:
    sys.exit(1)
"; do
    sleep 2
done
echo "Database ready."

echo "Running migrations..."
alembic -c migrations/alembic.ini upgrade head
echo "Migrations done."

echo "Starting hypercorn..."
exec hypercorn --bind 0.0.0.0:8000 --read-timeout 120 asgi:app
