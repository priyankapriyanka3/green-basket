#!/bin/sh
# docker-entrypoint.sh - Run migrations and seed data before starting the backend
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Seeding database..."
python seed_data.py 2>/dev/null || true

echo "Starting backend server..."
exec "$@"
