from django.http import HttpRequest
from ninja.security import APIKeyHeader, APIKeyQuery, HttpBearer

from apps.core.models import Profile

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)


def _get_profile_for_api_key(key: str) -> Profile | None:
    logger.info("[Django Ninja Auth] API key request")
    try:
        return Profile.objects.select_related("user").get(key=key)
    except Profile.DoesNotExist:
        logger.warning("[Django Ninja Auth] Invalid API key")
        return None


class APIKeyAuth(APIKeyQuery):
    param_name = "api_key"

    def authenticate(self, request: HttpRequest, key: str) -> Profile | None:
        return _get_profile_for_api_key(key)


class APIKeyHeaderAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request: HttpRequest, key: str) -> Profile | None:
        return _get_profile_for_api_key(key)


class BearerAPIKeyAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Profile | None:
        return _get_profile_for_api_key(token)


class SessionAuth:
    """Authentication via Django session"""

    def authenticate(self, request: HttpRequest) -> Profile | None:
        if hasattr(request, "user") and request.user.is_authenticated:
            logger.info(
                "[Django Ninja Auth] API Request with authenticated user",
                user_id=request.user.id,
            )
            try:
                return request.user.profile
            except Profile.DoesNotExist:
                logger.warning("[Django Ninja Auth] No profile for user", user_id=request.user.id)
                return None
        return None

    def __call__(self, request: HttpRequest):
        return self.authenticate(request)


class SuperuserAPIKeyAuth(APIKeyQuery):
    param_name = "api_key"

    def authenticate(self, request: HttpRequest, key: str) -> Profile | None:
        try:
            profile = Profile.objects.select_related("user").get(key=key)
            if profile.user.is_superuser:
                return profile
            logger.warning(
                "[Django Ninja Auth] Non-superuser attempted admin access",
                profile_id=profile.user.id,
            )
            return None
        except Profile.DoesNotExist:
            logger.warning("[Django Ninja Auth] Profile does not exist")
            return None


api_key_auth = [APIKeyAuth(), APIKeyHeaderAuth(), BearerAPIKeyAuth()]
session_auth = SessionAuth()
superuser_api_auth = SuperuserAPIKeyAuth()
