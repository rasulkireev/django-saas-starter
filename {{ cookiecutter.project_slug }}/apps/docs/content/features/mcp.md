---
title: MCP server
---

# MCP server

{% if cookiecutter.use_mcp == 'y' -%}
This project includes a hosted MCP server at `/mcp/` and a ready-to-copy agent skill at `/SKILL.md`.

The first included MCP tool is `get_user_info`, which returns safe account/profile details for the authenticated API key. The same data is available through the REST endpoint `GET /api/user`.

## Authentication

Use the API key shown on the user settings page. Never hardcode it into source control.

Supported MCP auth methods:

- `Authorization: Bearer <api_key>`
- `X-API-Key: <api_key>`
- `?api_key=<api_key>` on the MCP URL
- `api_key` tool argument for clients that cannot send headers

## Give this prompt to a coding agent

```text
Add {{ cookiecutter.project_name }} MCP support to this repo.

Use MCP URL: {{ cookiecutter.project_slug }} production URL + /mcp/
Use the user's {{ cookiecutter.project_name }} API key from an environment variable. Do not hardcode, log, or commit the key.
First verify the connection by calling the get_user_info MCP tool or GET /api/user with the API key, then add the smallest useful integration for this codebase.
Document how future agents should configure the MCP server locally.
```

## Deployment note

MCP uses ASGI. The generated server command runs `gunicorn {{ cookiecutter.project_slug }}.asgi:application` with `uvicorn_worker.UvicornWorker` when MCP is enabled.
{% else -%}
MCP was not enabled for this generated project. Regenerate with `use_mcp=y` to include the hosted MCP server, `/mcp/`, and `/SKILL.md`.
{% endif %}
