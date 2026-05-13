{% if cookiecutter.use_chatwoot == 'y' -%}
import hashlib
import hmac
{% endif %}

from allauth.socialaccount.models import SocialApp
from django.conf import settings

from apps.core.choices import ProfileStates

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)


def current_state(request):
    if request.user.is_authenticated:
        return {"current_state": request.user.profile.current_state}
    return {"current_state": ProfileStates.STRANGER}

{% if cookiecutter.use_stripe == 'y' %}
def pro_subscription_status(request):
    """
    Adds a 'has_pro_subscription' variable to the context.
    This variable is True if the user has an active pro subscription, False otherwise.
    """
    if request.user.is_authenticated and hasattr(request.user, "profile"):
        return {"has_pro_subscription": request.user.profile.has_active_subscription}
    return {"has_pro_subscription": False}
{% endif %}

{% if cookiecutter.use_posthog == 'y' -%}
def posthog_api_key(request):
    return {"posthog_api_key": settings.POSTHOG_API_KEY}
{% endif %}

{% if cookiecutter.use_mjml == 'y' -%}
def mjml_url(request):
    return {"mjml_url": settings.MJML_URL}
{% endif %}

{% if cookiecutter.use_chatwoot == 'y' -%}
def _chatwoot_identifier_hash(identifier):
    if not settings.CHATWOOT_HMAC_SECRET:
        return ""

    return hmac.new(
        settings.CHATWOOT_HMAC_SECRET.encode("utf-8"),
        str(identifier).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def chatwoot_config(request):
    base_url = settings.CHATWOOT_BASE_URL.rstrip("/")
    website_token = settings.CHATWOOT_WEBSITE_TOKEN
    if not base_url or not website_token:
        return {"chatwoot": {"enabled": False}}

    config = {
        "enabled": True,
        "base_url": base_url,
        "website_token": website_token,
        "user": None,
    }

    user = request.user
    if user.is_authenticated:
        identifier = str(user.pk)
        user_config = {
            "identifier": identifier,
            "email": user.email,
            "name": user.get_full_name() or user.email,
        }

        identifier_hash = _chatwoot_identifier_hash(identifier)
        if identifier_hash:
            user_config["identifier_hash"] = identifier_hash

        config["user"] = user_config

    return {"chatwoot": config}
{% endif %}

def available_social_providers(request):
    """
    Checks which social authentication providers are available.
    Returns a list of provider names from either SOCIALACCOUNT_PROVIDERS settings
    or SocialApp database entries, as django-allauth supports both configuration methods.
    """
    available_providers = set()

    configured_providers = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})

    available_providers.update(configured_providers.keys())

    try:
        social_apps = SocialApp.objects.all()
        for social_app in social_apps:
            available_providers.add(social_app.provider)
    except Exception as e:
        logger.warning("Error retrieving SocialApp entries", error=str(e))

    available_providers_list = sorted(list(available_providers))

    return {
        "available_social_providers": available_providers_list,
        "has_social_providers": len(available_providers_list) > 0,
    }
