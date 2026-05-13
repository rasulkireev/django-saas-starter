import time

import pytest
from allauth.account.models import EmailAddress
from allauth.mfa.models import Authenticator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_login_page_shows_passkey_option(client):
    response = client.get(reverse("account_login"))
    assert response.status_code == 200

    content = response.content.decode()
    assert "Sign in with a passkey" in content
    assert 'id="mfa_login"' in content
    assert "window.webauthnJSON.get(requestOptions)" in content
    assert "X-Requested-With" in content
    assert "allauth.webauthn.forms.loginForm" not in content


def test_signup_page_hides_passkey_signup_option(client):
    response = client.get(reverse("account_signup"))
    assert response.status_code == 200

    content = response.content.decode()
    assert "Username" not in content
    assert "Confirm Password" not in content
    assert "Cofirm Password" not in content
    assert "Sign up using a passkey" not in content


def test_login_page_uses_email_instead_of_username(client):
    response = client.get(reverse("account_login"))
    assert response.status_code == 200

    content = response.content.decode()
    assert 'placeholder="Email"' in content
    assert 'type="email"' in content
    assert 'placeholder="Username"' not in content


def test_signup_redirects_to_dashboard_without_blocking_email_code_page(
    client, monkeypatch, settings
):
    sent_confirmations = []

    def fake_send_confirmation_mail(self, request, emailconfirmation, signup):
        sent_confirmations.append((emailconfirmation.email_address.email, signup))

    monkeypatch.setattr(
        "{{ cookiecutter.project_slug }}.adapters.CustomAccountAdapter.send_confirmation_mail",
        fake_send_confirmation_mail,
    )
    {% if cookiecutter.use_posthog == 'y' -%}
    settings.POSTHOG_API_KEY = ""
    {% endif %}

    response = client.post(
        reverse("account_signup"),
        data={
            "email": "newuser@example.com",
            "password1": "strong-test-pass-123",
        },
    )

    assert response.status_code == 302
    assert response["Location"] == reverse("home")
    user = get_user_model().objects.get(email="newuser@example.com")
    assert user.username
    assert sent_confirmations == [("newuser@example.com", True)]


def test_dashboard_does_not_show_email_confirmation_reminder(client):
    user = get_user_model().objects.create_user(
        username="unverified",
        email="unverified@example.com",
        password="strong-test-pass-123",
    )
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True, "verified": False},
    )
    client.force_login(user)

    response = client.get(reverse("home"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Your email is not yet confirmed" not in content
    assert "Welcome to {{ cookiecutter.project_name }}" in content


def test_settings_shows_email_confirmation_and_passkey_setup(client):
    user = get_user_model().objects.create_user(
        username="settingsuser",
        email="settingsuser@example.com",
        password="strong-test-pass-123",
    )
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True, "verified": False},
    )
    client.force_login(user)

    response = client.get(reverse("settings"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Your email is not yet confirmed" in content
    assert "Add passkey" in content
    assert reverse("mfa_add_webauthn") in content


def test_settings_handles_users_without_allauth_email_address(client):
    user = get_user_model().objects.create_user(
        username="noemailaddress",
        email="noemailaddress@example.com",
        password="strong-test-pass-123",
    )
    client.force_login(user)

    response = client.get(reverse("settings"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Your email is not yet confirmed" in content
    assert "Add passkey" in content


def test_settings_shows_passkey_manage_link_when_passkey_exists(client):
    user = get_user_model().objects.create_user(
        username="passkeyuser",
        email="passkeyuser@example.com",
        password="strong-test-pass-123",
    )
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True, "verified": True},
    )
    Authenticator.objects.create(
        user=user,
        type=Authenticator.Type.WEBAUTHN,
        data={"name": "Test passkey"},
    )
    client.force_login(user)

    response = client.get(reverse("settings"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "You have 1 passkey set up." in content
    assert "Manage passkeys" in content
    assert reverse("mfa_list_webauthn") in content


def test_mfa_index_uses_app_styling(client):
    user = get_user_model().objects.create_user(
        username="mfauser",
        email="mfauser@example.com",
        password="strong-test-pass-123",
    )
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True, "verified": True},
    )
    client.force_login(user)

    response = client.get(reverse("mfa_index"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Passkeys" in content
    assert "Add passkey" in content
    assert "Menu:" not in content


def test_webauthn_add_page_loads_styled_form_and_scripts(client):
    user = get_user_model().objects.create_user(
        username="addpasskeyuser",
        email="addpasskeyuser@example.com",
        password="strong-test-pass-123",
    )
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True, "verified": True},
    )
    assert client.login(username="addpasskeyuser", password="strong-test-pass-123")
    session = client.session
    session["account_authentication_methods"] = [
        {"method": "password", "at": time.time(), "username": "addpasskeyuser"}
    ]
    session.save()

    response = client.get(reverse("mfa_add_webauthn"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Add passkey" in content
    assert 'id="mfa_webauthn_add"' in content
    assert "allauth.webauthn.forms.addForm" in content
    assert "mfa/js/webauthn.js" in content
    assert "Menu:" not in content


def test_reauthenticate_page_uses_app_styling(client):
    user = get_user_model().objects.create_user(
        username="reauthuser",
        email="reauthuser@example.com",
        password="strong-test-pass-123",
    )
    client.force_login(user)

    response = client.get(reverse("account_reauthenticate"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Confirm access" in content
    assert "Menu:" not in content


def test_account_email_page_uses_app_styling(client):
    user = get_user_model().objects.create_user(
        username="emailpageuser",
        email="emailpageuser@example.com",
        password="strong-test-pass-123",
    )
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True, "verified": False},
    )
    client.force_login(user)

    response = client.get(reverse("account_email"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Email addresses" in content
    assert "Re-send verification" in content
    assert "Menu:" not in content


def test_settings_resend_confirmation_uses_hmac_link(client, monkeypatch):
    sent_confirmations = []

    def fake_send_confirmation_mail(self, request, emailconfirmation, signup):
        sent_confirmations.append((emailconfirmation, signup))

    monkeypatch.setattr(
        "{{ cookiecutter.project_slug }}.adapters.CustomAccountAdapter.send_confirmation_mail",
        fake_send_confirmation_mail,
    )
    user = get_user_model().objects.create_user(
        username="resenduser",
        email="resenduser@example.com",
        password="strong-test-pass-123",
    )
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True, "verified": False},
    )
    client.force_login(user)

    response = client.post(reverse("resend_confirmation"))

    assert response.status_code == 302
    assert response["Location"] == reverse("settings")
    assert len(list(get_messages(response.wsgi_request))) == 1
    assert len(sent_confirmations) == 1
    emailconfirmation, signup = sent_confirmations[0]
    assert signup is False
    assert emailconfirmation.key.count(":") == 2
    assert not EmailAddress.objects.get(user=user, email=user.email).verified


def test_settings_resend_confirmation_requires_post(client):
    user = get_user_model().objects.create_user(
        username="resendgetuser",
        email="resendgetuser@example.com",
        password="strong-test-pass-123",
    )
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True, "verified": False},
    )
    client.force_login(user)

    response = client.get(reverse("resend_confirmation"))

    assert response.status_code == 405


def test_settings_resend_confirmation_link_confirms_email(client, monkeypatch):
    sent_confirmations = []

    def fake_send_confirmation_mail(self, request, emailconfirmation, signup):
        sent_confirmations.append(emailconfirmation)

    monkeypatch.setattr(
        "{{ cookiecutter.project_slug }}.adapters.CustomAccountAdapter.send_confirmation_mail",
        fake_send_confirmation_mail,
    )
    user = get_user_model().objects.create_user(
        username="confirmresenduser",
        email="confirmresenduser@example.com",
        password="strong-test-pass-123",
    )
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True, "verified": False},
    )
    client.force_login(user)

    response = client.post(reverse("resend_confirmation"))

    assert response.status_code == 302
    assert len(sent_confirmations) == 1
    confirm_path = reverse("account_confirm_email", args=[sent_confirmations[0].key])
    confirm_response = client.post(confirm_path)

    assert confirm_response.status_code == 302
    assert EmailAddress.objects.get(user=user, email=user.email).verified is True


def test_mailgun_sender_defaults_are_configurable():
    assert settings.DEFAULT_FROM_EMAIL == "{{ cookiecutter.author_name }} from {{ cookiecutter.project_name }} <hello@{{ cookiecutter.project_slug }}.app>"
    assert settings.SERVER_EMAIL == "{{ cookiecutter.project_name }} Errors <error@{{ cookiecutter.project_slug }}.app>"
    assert settings.ANYMAIL["MAILGUN_SENDER_DOMAIN"] == "mg.{{ cookiecutter.project_slug }}.app"
