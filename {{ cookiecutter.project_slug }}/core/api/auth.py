from django.http import HttpRequest
from ninja.security import HttpBearer

from core.models import Profile

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)


class MultipleAuthSchema(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str | None = None) -> Profile | None:
        if token:
            logger.info(
                "[Django Ninja Auth] API Request with token",
                request=request.__dict__,
                token=token,
            )
            try:
                return Profile.objects.get(key=token)
            except Profile.DoesNotExist:
                return None

        if hasattr(request, "user") and request.user.is_authenticated:
            logger.info(
                "[Django Ninja Auth] API Request with user",
                request=request.__dict__,
                user=request.user.__dict__,
            )
            try:
                return request.user.profile
            except Profile.DoesNotExist:
                return None

        return None

    def __call__(self, request):
        logger.info(
            "[Django Ninja Auth] API Request",
            request=request.__dict__,
        )

        authorization = request.headers.get("Authorization", "")
        if authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            return self.authenticate(request, token)

        if hasattr(request, "user") and request.user.is_authenticated:
            return self.authenticate(request)

        return super().__call__(request)
