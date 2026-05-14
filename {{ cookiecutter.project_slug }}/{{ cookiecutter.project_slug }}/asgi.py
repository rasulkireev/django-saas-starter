"""
ASGI config for {{ cookiecutter.project_slug }} project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from django.core.asgi import get_asgi_application
{% if cookiecutter.use_mcp == 'y' -%}
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.routing import Mount, Route
{% endif %}

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_slug }}.settings")

{% if cookiecutter.use_mcp == 'y' -%}
django_application = get_asgi_application()

from apps.mcp_server.server import mcp  # noqa: E402

mcp_application = mcp.http_app(path="/")


def redirect_mcp(request: Request) -> RedirectResponse:
    return RedirectResponse(str(request.url.replace(path="/mcp/")), status_code=307)


application = Starlette(
    routes=[
        Route("/mcp", endpoint=redirect_mcp, methods=["GET", "POST", "DELETE"]),
        Mount("/mcp", app=mcp_application),
        Mount("/", app=django_application),
    ],
    lifespan=mcp_application.lifespan,
)
{% else -%}
application = get_asgi_application()
{% endif %}
