import requests

from django.forms.utils import ErrorList

from apps.core.models import EmailSent, Profile
from apps.core.choices import EmailType

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)


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


def track_email_sent(email_address: str, email_type: EmailType, profile: Profile = None):
    """
    Track sent emails by creating EmailSent records.
    """
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
