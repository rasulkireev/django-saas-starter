import time
from collections import Counter
from typing import TYPE_CHECKING, Any, Callable

import requests
from django.conf import settings
from django.forms.utils import ErrorList

from apps.core.choices import EmailType

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)

if TYPE_CHECKING:
    from apps.core.models import Profile

EMAIL_DELIVERY_METRICS = Counter()


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return f"""
            <div class="p-4 my-4 bg-red-50 dark:bg-red-950/40 rounded-md border border-red-200 dark:border-red-500/60 border-solid">
              <div class="flex">
                <div class="flex-shrink-0">
                  <!-- Heroicon name: solid/x-circle -->
                  <svg class="w-5 h-5 text-red-500 dark:text-red-300" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3 text-sm text-red-800 dark:text-red-200">
                      {''.join([f'<p>{e}</p>' for e in self])}
                </div>
              </div>
            </div>
         """ # noqa: E501

{% if cookiecutter.use_healthchecks == 'y' %}
def ping_healthchecks(ping_id):
    try:
        requests.get(f"https://healthchecks.cr.lvtd.dev/ping/{ping_id}", timeout=10)
    except requests.RequestException as e:
        logger.error("Ping failed", error=e, exc_info=True)
{% endif %}


def get_email_delivery_provider() -> str:
    backend = getattr(settings, "EMAIL_BACKEND", "")
    if "mailgun" in backend.lower():
        return "mailgun"
    if "smtp" in backend.lower():
        return "smtp"
    if "console" in backend.lower():
        return "console"
    return backend or "unknown"


def get_email_delivery_retry_backoff_seconds() -> tuple[float, ...]:
    configured = getattr(settings, "EMAIL_DELIVERY_RETRY_BACKOFF_SECONDS", (0.0, 1.0, 3.0))
    return tuple(float(value) for value in configured)


def is_transient_email_error(error: Exception) -> bool:
    transient_types = (
        TimeoutError,
        ConnectionError,
        requests.Timeout,
        requests.ConnectionError,
    )
    return isinstance(error, transient_types)



def bump_email_delivery_metric(*, email_type: EmailType, provider: str, outcome: str) -> None:
    metric_key = f"{email_type}:{provider}:{outcome}"
    EMAIL_DELIVERY_METRICS[metric_key] += 1
    logger.info(
        "email_delivery_metric",
        email_type=email_type,
        provider=provider,
        outcome=outcome,
        metric_name="email_delivery_total",
        metric_value=EMAIL_DELIVERY_METRICS[metric_key],
    )



def track_email_sent(email_address: str, email_type: EmailType, profile: "Profile" = None):
    """
    Track sent emails by creating EmailSent records.
    """
    from apps.core.models import EmailSent

    try:
        email_sent = EmailSent.objects.create(
            email_address=email_address, email_type=email_type, profile=profile
        )
        logger.info(
            "[Track Email Sent] Email tracked successfully",
            email_address=email_address,
            email_type=email_type,
            profile_id=profile.id if profile else None,
            email_sent_id=email_sent.id,
        )
        return email_sent
    except Exception as e:
        logger.error(
            "[Track Email Sent] Failed to track email",
            email_address=email_address,
            email_type=email_type,
            error=str(e),
            exc_info=True,
        )
        return None



def send_transactional_email(
    send_callable: Callable[[], Any],
    *,
    email_address: str,
    email_type: EmailType,
    profile: "Profile" = None,
    context: dict[str, Any] | None = None,
    retry_backoff_seconds: tuple[float, ...] | None = None,
) -> bool:
    provider = get_email_delivery_provider()
    context = context or {}
    backoff_seconds = retry_backoff_seconds or get_email_delivery_retry_backoff_seconds()
    max_attempts = max(1, len(backoff_seconds))

    for attempt in range(1, max_attempts + 1):
        try:
            send_callable()
            track_email_sent(
                email_address=email_address,
                email_type=email_type,
                profile=profile,
            )
            bump_email_delivery_metric(
                email_type=email_type,
                provider=provider,
                outcome="success",
            )
            logger.info(
                "email_delivery",
                email_type=email_type,
                email_address=email_address,
                provider=provider,
                outcome="success",
                attempt=attempt,
                max_attempts=max_attempts,
                profile_id=profile.id if profile else None,
                context=context,
            )
            return True
        except Exception as error:
            transient = is_transient_email_error(error)
            should_retry = transient and attempt < max_attempts
            outcome = "retrying" if should_retry else "failed"

            bump_email_delivery_metric(
                email_type=email_type,
                provider=provider,
                outcome=outcome,
            )
            log_method = logger.warning if transient else logger.error
            log_method(
                "email_delivery",
                email_type=email_type,
                email_address=email_address,
                provider=provider,
                outcome=outcome,
                attempt=attempt,
                max_attempts=max_attempts,
                error_class=error.__class__.__name__,
                error=str(error),
                transient=transient,
                profile_id=profile.id if profile else None,
                context=context,
                exc_info=not should_retry,
            )

            if should_retry:
                sleep_seconds = backoff_seconds[attempt]
                if sleep_seconds > 0:
                    time.sleep(sleep_seconds)
                continue

            return False

    return False
