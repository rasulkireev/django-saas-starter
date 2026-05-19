from types import SimpleNamespace

import anyio
import pytest
from fastmcp import Client

from apps.mcp_server.server import mcp


def _profile():
    user = SimpleNamespace(
        id=7,
        email="ada@example.com",
        username="ada",
        first_name="Ada",
        last_name="Lovelace",
        date_joined="2026-05-14T00:00:00Z",
        is_staff=False,
        is_superuser=False,
        get_full_name=lambda: "Ada Lovelace",
    )
    return SimpleNamespace(
        id=11,
        user=user,
        state="signed_up",
        {% if cookiecutter.use_stripe == 'y' -%}
        has_active_subscription=False,
        {% endif %}
    )


def test_get_user_info_mcp_tool_returns_safe_user_data(monkeypatch):
    async def run():
        monkeypatch.setattr(
            "apps.mcp_server.server._authenticate_profile",
            lambda api_key=None: _profile(),
        )

        async with Client(mcp) as client:
            result = await client.call_tool("get_user_info", {"api_key": "secret-key"})

        payload = result.data
        assert payload["email"] == "ada@example.com"
        assert payload["profile"]["id"] == 11
        assert "key" not in payload

    anyio.run(run)


def test_get_user_info_mcp_tool_rejects_invalid_api_key(monkeypatch):
    def reject(api_key=None):
        raise PermissionError("Invalid {{ cookiecutter.project_name }} API key")

    async def run():
        monkeypatch.setattr("apps.mcp_server.server._authenticate_profile", reject)

        async with Client(mcp) as client:
            with pytest.raises(Exception, match="Invalid {{ cookiecutter.project_name }} API key"):
                await client.call_tool("get_user_info", {"api_key": "not-real"})

    anyio.run(run)
