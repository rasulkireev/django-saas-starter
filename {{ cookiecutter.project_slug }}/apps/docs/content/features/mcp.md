---
title: MCP access
---

{% if cookiecutter.use_mcp == 'y' -%}
This project includes a hosted MCP server at `/mcp/`, a ready-to-copy agent skill at `/SKILL.md`, and a dashboard prompt that includes the exact URLs and API key for the current user.

The first included MCP tool is `get_user_info`, which returns safe account/profile details for the authenticated API key. The same data is available through the REST endpoint `GET /api/user`.

## URLs

```text
MCP URL: {% raw %}{{ mcp_url }}{% endraw %}
Skill URL: {% raw %}{{ skill_url }}{% endraw %}
User API: {% raw %}{{ api_base_url }}{% endraw %}/user
```

## Authentication

Use the API key shown on the user settings page. Never hardcode it into source control.

Supported MCP auth methods:

- `Authorization: Bearer <api_key>`
- `X-API-Key: <api_key>`
- `?api_key=<api_key>` on the MCP URL
- `api_key` tool argument for clients that cannot send headers

## Give this prompt to a coding agent

```text
{% raw %}{{ agent_setup_prompt }}{% endraw %}
```

## Deployment note

MCP uses ASGI. The generated server command runs `gunicorn {{ cookiecutter.project_slug }}.asgi:application` with `uvicorn_worker.UvicornWorker` when MCP is enabled.
{% else -%}
MCP was not enabled for this generated project. Regenerate with `use_mcp=y` to include the hosted MCP server, `/mcp/`, `/SKILL.md`, and the dashboard copy/paste agent prompt.
{% endif %}
