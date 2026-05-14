---
title: Introduction
description: Learn how {{ cookiecutter.project_name }} API authentication works and where to find generated API docs.
keywords: {{ cookiecutter.project_name }} API, API authentication, OpenAPI docs
---

{{ cookiecutter.project_name }} exposes authenticated REST endpoints for account checks and product-specific integrations.

## Base URL

```text
{% raw %}{{ api_base_url }}{% endraw %}
```

## Authentication

Use your API key as a bearer token:

```http
Authorization: Bearer {% raw %}{{ api_key_full }}{% endraw %}
```

Example request:

```bash
curl -H "Authorization: Bearer {% raw %}{{ api_key_full }}{% endraw %}" "{% raw %}{{ api_base_url }}{% endraw %}/user"
```

Authenticated docs show your full key so you can copy it into trusted tools. Treat it like a password: do not put it in frontend code, public repos, shared screenshots, or logs.

## Interactive API docs

{{ cookiecutter.project_name }} also exposes generated API docs from the backend schema:

[Open generated API docs]({% raw %}{{ api_docs_url }}{% endraw %})

Use those generated docs when you want request/response schemas or to inspect lower-level endpoint details. Use this docs section for workflow-oriented guidance.

## Sections

- **User API** — verify a key and inspect safe profile details.
- Add product-specific API pages here as you add user-facing endpoints.
