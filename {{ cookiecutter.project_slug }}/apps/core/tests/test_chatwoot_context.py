import hmac
from hashlib import sha256
from types import SimpleNamespace

from django.test import RequestFactory, override_settings

from apps.core.context_processors import chatwoot_config


@override_settings(CHATWOOT_BASE_URL="", CHATWOOT_WEBSITE_TOKEN="")
def test_chatwoot_context_disabled_without_config():
    request = RequestFactory().get("/")
    request.user = SimpleNamespace(is_authenticated=False)

    assert chatwoot_config(request) == {"chatwoot": {"enabled": False}}


@override_settings(CHATWOOT_BASE_URL="", CHATWOOT_WEBSITE_TOKEN="website-token")
def test_chatwoot_context_disabled_without_base_url():
    request = RequestFactory().get("/")
    request.user = SimpleNamespace(is_authenticated=False)

    assert chatwoot_config(request) == {"chatwoot": {"enabled": False}}


@override_settings(CHATWOOT_BASE_URL="https://chatwoot.example.com", CHATWOOT_WEBSITE_TOKEN="")
def test_chatwoot_context_disabled_without_website_token():
    request = RequestFactory().get("/")
    request.user = SimpleNamespace(is_authenticated=False)

    assert chatwoot_config(request) == {"chatwoot": {"enabled": False}}


@override_settings(
    CHATWOOT_BASE_URL="https://chatwoot.example.com/",
    CHATWOOT_WEBSITE_TOKEN="website-token",
    CHATWOOT_HMAC_SECRET="",
)
def test_chatwoot_context_enables_anonymous_widget():
    request = RequestFactory().get("/")
    request.user = SimpleNamespace(is_authenticated=False)

    assert chatwoot_config(request) == {
        "chatwoot": {
            "enabled": True,
            "base_url": "https://chatwoot.example.com",
            "website_token": "website-token",
            "user": None,
        }
    }


@override_settings(
    CHATWOOT_BASE_URL="https://chatwoot.example.com",
    CHATWOOT_WEBSITE_TOKEN="website-token",
    CHATWOOT_HMAC_SECRET="",
)
def test_chatwoot_context_identifies_authenticated_user_without_hmac():
    request = RequestFactory().get("/")
    request.user = SimpleNamespace(
        is_authenticated=True,
        pk=42,
        email="ada@example.com",
        get_full_name=lambda: "Ada Lovelace",
    )

    assert chatwoot_config(request)["chatwoot"]["user"] == {
        "identifier": "42",
        "email": "ada@example.com",
        "name": "Ada Lovelace",
    }


@override_settings(
    CHATWOOT_BASE_URL="https://app.chatwoot.com",
    CHATWOOT_WEBSITE_TOKEN="website-token",
    CHATWOOT_HMAC_SECRET="hmac-secret",
)
def test_chatwoot_context_identifies_authenticated_user_with_hmac():
    request = RequestFactory().get("/")
    request.user = SimpleNamespace(
        is_authenticated=True,
        pk=42,
        email="ada@example.com",
        get_full_name=lambda: "",
    )

    expected_hash = hmac.new(b"hmac-secret", b"42", sha256).hexdigest()

    assert chatwoot_config(request)["chatwoot"]["user"] == {
        "identifier": "42",
        "email": "ada@example.com",
        "name": "ada@example.com",
        "identifier_hash": expected_hash,
    }
