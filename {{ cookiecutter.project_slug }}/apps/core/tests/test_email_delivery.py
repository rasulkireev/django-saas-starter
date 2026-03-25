from types import SimpleNamespace

import pytest
from allauth.account.adapter import DefaultAccountAdapter

from apps.core.choices import EmailType
from apps.core.models import EmailSent, Feedback
from apps.core.utils import (
    EMAIL_DELIVERY_METRICS,
    get_email_delivery_provider,
    send_transactional_email,
)
from {{ cookiecutter.project_slug }}.adapters import CustomAccountAdapter


@pytest.mark.django_db
def test_send_transactional_email_tracks_success(profile):
    EMAIL_DELIVERY_METRICS.clear()
    attempts = []

    def send_callable():
        attempts.append("sent")

    success = send_transactional_email(
        send_callable,
        email_address=profile.user.email,
        email_type=EmailType.WELCOME,
        profile=profile,
        retry_backoff_seconds=(0.0,),
    )

    assert success is True
    assert attempts == ["sent"]
    assert EmailSent.objects.filter(email_address=profile.user.email).count() == 1
    provider = get_email_delivery_provider()
    assert EMAIL_DELIVERY_METRICS[f"{EmailType.WELCOME}:{provider}:success"] == 1


@pytest.mark.django_db
def test_send_transactional_email_retries_transient_failures(profile):
    EMAIL_DELIVERY_METRICS.clear()
    attempts = {"count": 0}

    def send_callable():
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise TimeoutError("temporary email outage")

    success = send_transactional_email(
        send_callable,
        email_address=profile.user.email,
        email_type=EmailType.EMAIL_CONFIRMATION,
        profile=profile,
        retry_backoff_seconds=(0.0, 0.0),
    )

    assert success is True
    assert attempts["count"] == 2
    provider = get_email_delivery_provider()
    assert EMAIL_DELIVERY_METRICS[f"{EmailType.EMAIL_CONFIRMATION}:{provider}:retrying"] == 1
    assert EMAIL_DELIVERY_METRICS[f"{EmailType.EMAIL_CONFIRMATION}:{provider}:success"] == 1


@pytest.mark.django_db
def test_send_transactional_email_returns_false_for_hard_failures(profile):
    EMAIL_DELIVERY_METRICS.clear()

    def send_callable():
        raise ValueError("permanent email template error")

    success = send_transactional_email(
        send_callable,
        email_address=profile.user.email,
        email_type=EmailType.EMAIL_CONFIRMATION,
        profile=profile,
        retry_backoff_seconds=(0.0, 0.0),
    )

    assert success is False
    assert EmailSent.objects.count() == 0
    provider = get_email_delivery_provider()
    assert EMAIL_DELIVERY_METRICS[f"{EmailType.EMAIL_CONFIRMATION}:{provider}:failed"] == 1


@pytest.mark.django_db
def test_confirmation_mail_failures_do_not_bubble_to_signup(user, monkeypatch):
    def fake_send_confirmation_mail(self, request, emailconfirmation, signup):
        raise TimeoutError("mailgun unavailable")

    monkeypatch.setattr(
        DefaultAccountAdapter,
        "send_confirmation_mail",
        fake_send_confirmation_mail,
    )

    adapter = CustomAccountAdapter()
    emailconfirmation = SimpleNamespace(
        email_address=SimpleNamespace(user=user, email=user.email)
    )

    adapter.send_confirmation_mail(None, emailconfirmation, signup=True)

    assert EmailSent.objects.count() == 0


@pytest.mark.django_db
def test_feedback_notifications_swallow_email_failures(profile, monkeypatch):
    def fake_send_mail(*args, **kwargs):
        raise TimeoutError("smtp timeout")

    monkeypatch.setattr("apps.core.models.send_mail", fake_send_mail)

    feedback = Feedback(
        profile=profile,
        feedback="This page helped.",
        page="/pricing/",
    )
    feedback.save()

    assert Feedback.objects.count() == 1
    assert EmailSent.objects.count() == 0
