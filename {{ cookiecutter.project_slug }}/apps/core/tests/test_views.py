import pytest
from django.test import override_settings
from django.urls import reverse

from apps.core.views import build_absolute_public_url


@pytest.mark.django_db
class TestHomeView:
    def test_home_view_status_code(self, auth_client):
        url = reverse("home")
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_home_view_uses_correct_template(self, auth_client):
        url = reverse("home")
        response = auth_client.get(url)
        assert "pages/home.html" in [t.name for t in response.templates]

    {% if cookiecutter.use_mcp == 'y' -%}
    def test_home_view_includes_copyable_agent_prompt(self, auth_client, profile):
        url = reverse("home")
        response = auth_client.get(url)
        content = response.content.decode()

        assert response.status_code == 200
        assert "Copy/paste prompt" in content
        assert "data-controller=\"copy\"" in content
        assert "/mcp/" in content
        assert "/SKILL.md" in content
        assert profile.key in content
    {% endif %}


@override_settings(SITE_URL="http://example.com")
def test_build_absolute_public_url_upgrades_non_local_http():
    assert build_absolute_public_url("/api/user") == "https://example.com/api/user"


@override_settings(SITE_URL="http://notlocalhost.example")
def test_build_absolute_public_url_does_not_treat_hostname_substrings_as_local():
    assert build_absolute_public_url("/api/user") == "https://notlocalhost.example/api/user"


@override_settings(SITE_URL="http://localhost:8000")
def test_build_absolute_public_url_preserves_localhost_http():
    assert build_absolute_public_url("/api/user") == "http://localhost:8000/api/user"
