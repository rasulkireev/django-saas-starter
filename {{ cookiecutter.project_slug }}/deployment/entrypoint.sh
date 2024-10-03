#!/bin/sh

# Default to server command if no arguments provided
if [ $# -eq 0 ]; then
    echo "No arguments provided. Defaulting to running the server."
    server=true
else
    server=false
fi

# All commands before the conditional ones
export PROJECT_NAME={{ cookiecutter.project_slug }}

{% if cookiecutter.use_opentelemetry == 'y' -%}
export OTEL_EXPORTER_OTLP_ENDPOINT=https://signoz-otel-collector-proxy.cr.lvtd.dev
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
{% endif %}

export DJANGO_SETTINGS_MODULE="{{ cookiecutter.project_slug }}.settings"

while getopts ":sw" option; do
    case "${option}" in
        s)  # Run server
            server=true
            ;;
        w)  # Run worker
            server=false
            ;;
        *)  # Invalid option
            echo "Invalid option: -$OPTARG" >&2
            ;;
    esac
done
shift $((OPTIND - 1))

# If no valid option provided, default to server
if [ "$server" = true ]; then
    python manage.py collectstatic --noinput
    python manage.py migrate
    {% if cookiecutter.use_opentelemetry == 'y' -%}
    export OTEL_SERVICE_NAME=${PROJECT_NAME}_${ENVIRONMENT:-dev}
    export OTEL_RESOURCE_ATTRIBUTES=service.name=${PROJECT_NAME}_${ENVIRONMENT:-dev}
    opentelemetry-instrument{% endif -%} gunicorn ${PROJECT_NAME}.wsgi:application --bind 0.0.0.0:80 --workers 3 --threads 2 --reload
    {% endif %}
else
    {% if cookiecutter.use_opentelemetry == 'y' -%}
    export OTEL_SERVICE_NAME="${PROJECT_NAME}_${ENVIRONMENT:-dev}_workers"
    export OTEL_RESOURCE_ATTRIBUTES=service.name=${PROJECT_NAME}_${ENVIRONMENT:-dev}_workers
    opentelemetry-instrument{% endif -%} python manage.py qcluster
fi
