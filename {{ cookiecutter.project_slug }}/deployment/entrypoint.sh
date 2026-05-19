#!/bin/sh
set -eu

# Default to server command if no arguments provided
if [ $# -eq 0 ]; then
    echo "No arguments provided. Defaulting to running the server."
    server=true
else
    server=false
fi

export PROJECT_NAME={{ cookiecutter.project_slug }}
export DJANGO_SETTINGS_MODULE="{{ cookiecutter.project_slug }}.settings"

while getopts ":sw" option; do
    case "${option}" in
        s) server=true ;;
        w) server=false ;;
        *) echo "Invalid option: -$OPTARG" >&2 ;;
    esac
done
shift $((OPTIND - 1))

wait_for_database() {
    echo "Waiting for database..."
    uv run --no-sync python - <<'PY'
import os
import sys
import time

import django
from django.db import connections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_slug }}.settings")
django.setup()

last_error = None
for attempt in range(1, 61):
    try:
        connections["default"].ensure_connection()
        print("Database is ready.")
        sys.exit(0)
    except Exception as exc:
        last_error = exc
        print(f"Database unavailable, retrying ({attempt}/60): {exc}", flush=True)
        time.sleep(2)

print(f"Database did not become ready: {last_error}", file=sys.stderr)
sys.exit(1)
PY
}

wait_for_database

if [ "$server" = true ]; then
    echo "Starting {{ cookiecutter.project_name }} server..."
    uv run --no-sync python manage.py collectstatic --noinput
    uv run --no-sync python manage.py migrate --noinput
    {% if cookiecutter.use_mcp == 'y' -%}
    exec uv run --no-sync gunicorn ${PROJECT_NAME}.asgi:application --bind 0.0.0.0:80 --workers 3 --worker-class uvicorn_worker.UvicornWorker
    {% else -%}
    exec uv run --no-sync gunicorn ${PROJECT_NAME}.wsgi:application --bind 0.0.0.0:80 --workers 3 --threads 2
    {% endif %}
else
    echo "Starting {{ cookiecutter.project_name }} workers..."
    exec uv run --no-sync python manage.py qcluster
fi
