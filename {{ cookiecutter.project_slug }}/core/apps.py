{% if cookiecutter.use_posthog == 'y' -%}
import posthog
{% endif -%}
from django.conf import settings
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        import core.signals  # noqa

        {% if cookiecutter.use_posthog == 'y' -%}
        if settings.ENVIRONMENT == "prod":
            posthog.api_key = settings.POSTHOG_API_KEY
            posthog.host = "https://us.i.posthog.com"
        {% endif -%}
