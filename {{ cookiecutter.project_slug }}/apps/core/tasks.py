{% if cookiecutter.use_posthog == 'y' -%}
import json
from urllib.parse import unquote

import posthog
{% endif %}

import requests
from django.conf import settings

from apps.core.models import Profile
from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)

{% if cookiecutter.use_buttondown == 'y' -%}
def add_email_to_buttondown(email, tag):
    if not settings.BUTTONDOWN_API_KEY:
        return "Buttondown API key not found."

    data = {
        "email_address": str(email),
        "metadata": {"source": tag},
        "tags": [tag],
        "referrer_url": "https://{{ cookiecutter.project_slug }}.com",
        "type": "regular",
    }

    r = requests.post(
        "https://api.buttondown.email/v1/subscribers",
        headers={"Authorization": f"Token {settings.BUTTONDOWN_API_KEY}"},
        json=data,
    )

    return r.json()
{% endif %}

{% if cookiecutter.use_posthog == 'y' -%}
def try_create_posthog_alias(profile_id: int, cookies: dict, source_function: str = None) -> str:
    if not settings.POSTHOG_API_KEY:
        return "PostHog API key not found."

    base_log_data = {
        "profile_id": profile_id,
        "cookies": cookies,
        "source_function": source_function,
    }

    profile = Profile.objects.get(id=profile_id)
    email = profile.user.email

    base_log_data["email"] = email
    base_log_data["profile_id"] = profile_id

    posthog_cookie = cookies.get(f"ph_{settings.POSTHOG_API_KEY}_posthog")
    if not posthog_cookie:
        logger.warning("[Try Create Posthog Alias] No PostHog cookie found.", **base_log_data)
        return f"No PostHog cookie found for profile {profile_id}."
    base_log_data["posthog_cookie"] = posthog_cookie

    logger.info("[Try Create Posthog Alias] Setting PostHog alias", **base_log_data)

    cookie_dict = json.loads(unquote(posthog_cookie))
    frontend_distinct_id = cookie_dict.get("distinct_id")

    if frontend_distinct_id:
        posthog.alias(frontend_distinct_id, email)
        posthog.alias(frontend_distinct_id, str(profile_id))

    logger.info("[Try Create Posthog Alias] Set PostHog alias", **base_log_data)


def track_event(
    profile_id: int, event_name: str, properties: dict, source_function: str = None
) -> str:
    if not settings.POSTHOG_API_KEY:
        return "PostHog API key not found."

    base_log_data = {
        "profile_id": profile_id,
        "event_name": event_name,
        "properties": properties,
        "source_function": source_function,
    }

    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        logger.error("[TrackEvent] Profile not found.", **base_log_data)
        return f"Profile with id {profile_id} not found."

    posthog.capture(
        profile.user.email,
        event=event_name,
        properties={
            "profile_id": profile.id,
            "email": profile.user.email,
            "current_state": profile.state,
            **properties,
        },
    )

    logger.info("[TrackEvent] Tracked event", **base_log_data)

    return f"Tracked event {event_name} for profile {profile_id}"
{% endif %}


def track_state_change(
    profile_id: int,
    from_state: str,
    to_state: str,
    metadata: dict = None,
    source_function: str = None
) -> None:
    from apps.core.models import Profile, ProfileStateTransition

    base_log_data = {
        "profile_id": profile_id,
        "from_state": from_state,
        "to_state": to_state,
        "metadata": metadata,
        "source_function": source_function,
    }

    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        logger.error("[TrackStateChange] Profile not found.", **base_log_data)
        return f"Profile with id {profile_id} not found."

    if from_state != to_state:
        logger.info("[TrackStateChange] Tracking state change", **base_log_data)
        ProfileStateTransition.objects.create(
            profile=profile,
            from_state=from_state,
            to_state=to_state,
            backup_profile_id=profile_id,
            metadata=metadata,
        )
        profile.state = to_state
        profile.save(update_fields=["state"])

    return f"Tracked state change from {from_state} to {to_state} for profile {profile_id}"
