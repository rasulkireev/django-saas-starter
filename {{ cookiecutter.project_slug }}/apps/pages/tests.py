import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_login_page_shows_passkey_option(client):
    response = client.get(reverse("account_login"))
    assert response.status_code == 200

    content = response.content.decode()
    assert "Sign in with a passkey" in content
    assert 'id="mfa_login"' in content


def test_signup_page_shows_passkey_option(client):
    response = client.get(reverse("account_signup"))
    assert response.status_code == 200

    content = response.content.decode()
    assert "Sign up using a passkey" in content


def test_passkey_signup_page_uses_custom_template(client):
    response = client.get(reverse("account_signup_by_passkey"))
    assert response.status_code == 200

    content = response.content.decode()
    assert "Create your account with a passkey" in content
    assert "Continue with passkey" in content
