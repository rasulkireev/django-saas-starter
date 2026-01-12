from django.http import HttpRequest

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)


def _get_api_key_from_headers(request: HttpRequest) -> str | None:
    key = request.headers.get("X-API-Key")
    if key:
        return key

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    parts = auth_header.split(None, 1)
    if len(parts) != 2:
        return None

    scheme, value = parts[0].lower(), parts[1].strip()
    if not value:
        return None

    if scheme in {"api-key", "apikey", "bearer", "token"}:
        return value

    return None