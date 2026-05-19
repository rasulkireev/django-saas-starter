#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK_DIR="${SMOKE_WORK_DIR:-$(mktemp -d)}"
KEEP_SMOKE_PROJECTS="${KEEP_SMOKE_PROJECTS:-}"
PYTHON_BIN="${PYTHON:-python}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
fi

if [[ -z "$KEEP_SMOKE_PROJECTS" ]]; then
  trap 'rm -rf "$WORK_DIR"' EXIT
else
  echo "Keeping generated smoke projects in $WORK_DIR"
fi

if [[ $# -eq 0 ]]; then
  VARIANTS=("default" "all-disabled")
else
  VARIANTS=("$@")
fi

require_command() {
  local command_name="$1"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Required command not found: $command_name" >&2
    exit 1
  fi
}

validate_variant() {
  local variant="$1"
  local project_slug
  local project_name
  local -a extra_context

  case "$variant" in
    default)
      project_slug="smoke_default"
      project_name="Smoke Default"
      extra_context=()
      ;;
    all-disabled)
      project_slug="smoke_disabled"
      project_name="Smoke Disabled"
      extra_context=(
        use_posthog=n
        use_buttondown=n
        use_s3=n
        use_stripe=n
        use_sentry=n
        generate_blog=n
        generate_docs=n
        use_mjml=n
        use_ai=n
        use_logfire=n
        use_healthchecks=n
        use_chatwoot=n
        use_mcp=n
        use_ci=n
      )
      ;;
    *)
      echo "Unknown smoke-test variant: $variant" >&2
      exit 1
      ;;
  esac

  local output_dir="$WORK_DIR/$variant"
  local project_dir="$output_dir/$project_slug"
  local -a cookiecutter_args=(
    --no-input
    "$ROOT_DIR"
    --output-dir "$output_dir"
    project_name="$project_name"
    project_slug="$project_slug"
  )

  if [[ ${#extra_context[@]} -gt 0 ]]; then
    cookiecutter_args+=("${extra_context[@]}")
  fi

  mkdir -p "$output_dir"

  echo "::group::Generate $variant project"
  cookiecutter "${cookiecutter_args[@]}"
  echo "::endgroup::"

  cd "$project_dir"

  echo "::group::Validate package.json and pyproject.toml"
  node -e "JSON.parse(require('fs').readFileSync('package.json', 'utf8'))"
  "$PYTHON_BIN" - <<'PY'
import pathlib
import tomllib

tomllib.loads(pathlib.Path("pyproject.toml").read_text())
PY
  echo "::endgroup::"

  echo "::group::Compile Python sources"
  "$PYTHON_BIN" -m compileall -q .
  echo "::endgroup::"

  echo "::group::Build frontend assets"
  npm install
  npm run build
  echo "::endgroup::"

  echo "::group::Install Python dependencies"
  uv sync --all-groups
  echo "::endgroup::"

  export ENVIRONMENT=dev
  export DEBUG=True
  export SECRET_KEY=template-smoke-test-secret
  export SITE_URL=http://localhost:8000
  export POSTGRES_DB="$project_slug"
  export POSTGRES_USER="$project_slug"
  export POSTGRES_PASSWORD="$project_slug"
  export POSTGRES_HOST=127.0.0.1
  export POSTGRES_PORT="${POSTGRES_PORT:-5432}"
  export REDIS_HOST="${REDIS_HOST:-127.0.0.1}"
  export REDIS_PORT="${REDIS_PORT:-6379}"
  export REDIS_PASSWORD="${REDIS_PASSWORD:-}"
  export REDIS_DB=0

  echo "::group::Run Django checks"
  uv run python manage.py check
  echo "::endgroup::"

  echo "::group::Check migrations are current"
  uv run python manage.py makemigrations --check --dry-run
  echo "::endgroup::"

  echo "::group::Run pytest"
  uv run pytest
  echo "::endgroup::"

  echo "::group::Build Docker images"
  docker build -f Dockerfile-python -t "django-saas-starter:${variant}-python" .
  docker build -f deployment/Dockerfile.server -t "django-saas-starter:${variant}-server" .
  docker build -f deployment/Dockerfile.workers -t "django-saas-starter:${variant}-workers" .
  echo "::endgroup::"
}

require_command cookiecutter
require_command docker
require_command node
require_command npm
require_command "$PYTHON_BIN"
require_command uv

for variant in "${VARIANTS[@]}"; do
  validate_variant "$variant"
done
