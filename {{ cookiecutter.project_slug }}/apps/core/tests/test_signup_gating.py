from django.conf import settings
from django.template.loader import render_to_string
from django.test import RequestFactory, override_settings
from django.urls import path
from django.utils.module_loading import import_string
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(), name="landing"),
    path("accounts/login/", TemplateView.as_view(), name="account_login"),
    path("accounts/signup/", TemplateView.as_view(), name="account_signup"),
    path("app/", TemplateView.as_view(), name="home"),
    path("blog/", TemplateView.as_view(), name="blog_posts"),
    path("docs/", TemplateView.as_view(), name="docs_home"),
    path("pricing/", TemplateView.as_view(), name="pricing"),
    path("privacy/", TemplateView.as_view(), name="privacy_policy"),
    path("terms/", TemplateView.as_view(), name="terms_of_service"),
]


def _account_adapter():
    return import_string(settings.ACCOUNT_ADAPTER)()


def _social_account_adapter():
    return import_string(settings.SOCIALACCOUNT_ADAPTER)()


@override_settings(ALLOW_SIGNUPS=True)
def test_account_signup_adapter_defaults_open_for_signups():
    request = RequestFactory().get("/accounts/signup/")

    assert _account_adapter().is_open_for_signup(request) is True


@override_settings(ALLOW_SIGNUPS=False)
def test_account_signup_adapter_can_pause_new_signups():
    request = RequestFactory().get("/accounts/signup/")

    assert _account_adapter().is_open_for_signup(request) is False


def test_account_signup_adapter_defaults_open_when_setting_is_absent(monkeypatch):
    request = RequestFactory().get("/accounts/signup/")
    monkeypatch.delattr(settings, "ALLOW_SIGNUPS", raising=False)

    assert _account_adapter().is_open_for_signup(request) is True


@override_settings(ALLOW_SIGNUPS=True)
def test_social_signup_adapter_defaults_open_for_signups():
    request = RequestFactory().get("/accounts/github/login/callback/")

    assert _social_account_adapter().is_open_for_signup(request, sociallogin=None) is True


@override_settings(ALLOW_SIGNUPS=False)
def test_social_signup_adapter_uses_same_signup_gate():
    request = RequestFactory().get("/accounts/github/login/callback/")

    assert _social_account_adapter().is_open_for_signup(request, sociallogin=None) is False


def test_social_signup_adapter_defaults_open_when_setting_is_absent(monkeypatch):
    request = RequestFactory().get("/accounts/github/login/callback/")
    monkeypatch.delattr(settings, "ALLOW_SIGNUPS", raising=False)

    assert _social_account_adapter().is_open_for_signup(request, sociallogin=None) is True


@override_settings(ROOT_URLCONF=__name__)
def test_signup_closed_template_tells_existing_users_to_log_in():
    content = render_to_string("account/signup_closed.html")

    assert "Signups paused" in content
    assert "Existing users can continue using the product as usual" in content
    assert 'href="/accounts/login/"' in content
    assert 'name="email"' not in content
    assert 'name="password1"' not in content
