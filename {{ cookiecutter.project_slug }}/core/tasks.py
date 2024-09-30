import requests
from django.conf import settings

from osig.utils import get_osig_logger

logger = get_osig_logger(__name__)

{% if cookiecutter.use_buttondown == 'y' -%}
def add_email_to_buttondown(email, tag):
    data = {
        "email_address": str(email),
        "metadata": {"source": tag},
        "tags": [tag],
        "referrer_url": "https://osig.app",
        "subscriber_type": "regular",
    }

    r = requests.post(
        "https://api.buttondown.email/v1/subscribers",
        headers={"Authorization": f"Token {settings.BUTTONDOWN_API_KEY}"},
        json=data,
    )

    return r.json()
{% endif -%}
