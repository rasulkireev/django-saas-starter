from apps.core.models import Profile


def serialize_user_info(profile: Profile) -> dict:
    """Return safe user/profile details for API and MCP consumers."""
    user = profile.user
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.get_full_name(),
        "date_joined": user.date_joined,
        "profile": {
            "id": profile.id,
            "state": profile.state,
            "has_active_subscription": {% if cookiecutter.use_stripe == 'y' -%}profile.has_active_subscription{% else -%}False{% endif %},
        },
    }
