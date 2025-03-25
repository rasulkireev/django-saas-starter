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
    gunicorn ${PROJECT_NAME}.wsgi:application --bind 0.0.0.0:80 --workers 3 --threads 2 --reload
else
    python manage.py qcluster
fi
