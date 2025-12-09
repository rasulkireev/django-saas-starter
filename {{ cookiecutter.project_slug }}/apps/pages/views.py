from allauth.account.views import SignupView
from django_q.tasks import async_task
from django.conf import settings
from django.views.generic import TemplateView

from apps.core.models import Profile

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)


class LandingPageView(TemplateView):
    template_name = "pages/landing-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        {% if cookiecutter.use_posthog == 'y' -%}
        if self.request.user.is_authenticated and settings.POSTHOG_API_KEY:
            user = self.request.user
            profile = user.profile

            async_task(
                "core.tasks.try_create_posthog_alias",
                profile_id=profile.id,
                cookies=self.request.COOKIES,
                source_function="LandingPageView - get_context_data",
                group="Create Posthog Alias",
            )
        {% endif %}

        return context


class AccountSignupView(SignupView):
    template_name = "account/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.user
        profile = user.profile

        {% if cookiecutter.use_posthog == 'y' -%}
        async_task(
            "core.tasks.try_create_posthog_alias",
            profile_id=profile.id,
            cookies=self.request.COOKIES,
            source_function="AccountSignupView - form_valid",
            group="Create Posthog Alias",
        )

        async_task(
            "core.tasks.track_event",
            profile_id=profile.id,
            event_name="user_signed_up",
            properties={
                "$set": {
                    "email": profile.user.email,
                    "username": profile.user.username,
                },
            },
            source_function="AccountSignupView - form_valid",
            group="Track Event",
        )
        {% endif %}

        return response


{% if cookiecutter.use_stripe == 'y' -%}
class PricingView(TemplateView):
    template_name = "pages/pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                profile = self.request.user.profile
                context["has_pro_subscription"] = profile.has_active_subscription
            except Profile.DoesNotExist:
                context["has_pro_subscription"] = False
        else:
            context["has_pro_subscription"] = False

        return context
{% endif %}


class PrivacyPolicyView(TemplateView):
    template_name = "pages/privacy-policy.html"


class TermsOfServiceView(TemplateView):
    template_name = "pages/terms-of-service.html"
