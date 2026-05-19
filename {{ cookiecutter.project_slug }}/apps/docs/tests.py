import pytest
from django.urls import reverse

from apps.docs.views import get_docs_navigation


@pytest.mark.django_db
def test_docs_require_login(client):
    response = client.get(reverse("docs_home"))
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


@pytest.mark.django_db
def test_docs_render_in_authenticated_app_shell(auth_client, profile):
    response = auth_client.get(reverse("docs_page", kwargs={"category": "api-reference", "page": "introduction"}))

    assert response.status_code == 200
    content = response.content.decode()
    assert "API Reference" in content
    assert "noindex, nofollow" in content
    assert "docs-code-blocks" in content
    assert "data-controller=\"toc docs-code\"" in content
    assert profile.key in content
    assert "Work in Progress" not in content


def test_docs_navigation_uses_frontmatter_titles():
    navigation = get_docs_navigation()
    api_reference = next(section for section in navigation if section["category_slug"] == "api-reference")

    assert api_reference["category"] == "API Reference"
    assert [page["title"] for page in api_reference["pages"]][:2] == ["Introduction", "User API"]
