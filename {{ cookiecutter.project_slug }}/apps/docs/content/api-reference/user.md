---
title: User API
description: Use the {{ cookiecutter.project_name }} user endpoint to verify API access and inspect safe profile details.
keywords: {{ cookiecutter.project_name }} API, user API, profile API
---

Use the user endpoint to verify an API key and fetch safe account/profile details for the authenticated user.

## Authentication

```http
Authorization: Bearer {% raw %}{{ api_key_full }}{% endraw %}
```

Your API base URL is:

```text
{% raw %}{{ api_base_url }}{% endraw %}
```

## Get current user

```http
GET {% raw %}{{ api_base_url }}{% endraw %}/user
```

Example:

```bash
curl -H "Authorization: Bearer {% raw %}{{ api_key_full }}{% endraw %}" "{% raw %}{{ api_base_url }}{% endraw %}/user"
```

Example response:

```json
{
  "email": "{% raw %}{{ user_email }}{% endraw %}",
  "profile": {
    "state": "signed_up"
  }
}
```

The response does **not** include your API key or privileged admin flags.

## When to use this endpoint

- Check that an integration is authenticated correctly.
- Give an AI agent a low-risk connectivity test before it does product-specific work.
- Confirm which {{ cookiecutter.project_name }} account a key belongs to.
