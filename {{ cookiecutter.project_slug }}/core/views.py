from urllib.parse import urlencode

{% if cookiecutter.use_stripe == 'y' -%}
import stripe
{% endif %}
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView

{% if cookiecutter.use_stripe == 'y' -%}
from djstripe import models as djstripe_models, settings as djstripe_settings
from core.utils import check_if_profile_has_pro_subscription
{% endif %}

from core.forms import ProfileUpdateForm
from core.models import Profile

from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger


{% if cookiecutter.use_stripe == 'y' -%}
stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY
{% endif %}

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)

class HomeView(TemplateView):
    template_name = "pages/home.html"

    {% if cookiecutter.use_stripe == 'y' -%}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        payment_status = self.request.GET.get("payment")
        if payment_status == "success":
            messages.success(self.request, "Thanks for subscribing, I hope you enjoy the app!")
            context["show_confetti"] = True
        elif payment_status == "failed":
            messages.error(self.request, "Something went wrong with the payment.")
        {% endif %}

        return context

class UserSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "account_login"
    model = Profile
    form_class = ProfileUpdateForm
    success_message = "User Profile Updated"
    success_url = reverse_lazy("settings")
    template_name = "pages/user-settings.html"

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        email_address = EmailAddress.objects.get_for_user(user, user.email)
        context["email_verified"] = email_address.verified
        context["resend_confirmation_url"] = reverse("resend_confirmation")
        context["has_subscription"] = user.profile.subscription is not None

        return context




@login_required
def resend_confirmation_email(request):
    user = request.user
    send_email_confirmation(request, user, EmailAddress.objects.get_for_user(user, user.email))

    return redirect("settings")


{% if cookiecutter.use_stripe == 'y' -%}
class PricingView(TemplateView):
    template_name = "pages/pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                profile = self.request.user.profile
                context["has_pro_subscription"] = check_if_profile_has_pro_subscription(profile.id)
            except Profile.DoesNotExist:
                context["has_pro_subscription"] = False
        else:
            context["has_pro_subscription"] = False

        return context


def create_checkout_session(request, pk, plan):
    user = request.user

    product = djstripe_models.Product.objects.get(name=plan)
    price = product.prices.filter(active=True).first()
    customer, _ = djstripe_models.Customer.get_or_create(subscriber=user)

    profile = user.profile
    profile.customer = customer
    profile.save(update_fields=["customer"])

    base_success_url = request.build_absolute_uri(reverse("home"))
    base_cancel_url = request.build_absolute_uri(reverse("home"))

    success_params = {"payment": "success"}
    success_url = f"{base_success_url}?{urlencode(success_params)}"

    cancel_params = {"payment": "failed"}
    cancel_url = f"{base_cancel_url}?{urlencode(cancel_params)}"

    checkout_session = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=["card"],
        allow_promotion_codes=True,
        automatic_tax={"enabled": True},
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            }
        ],
        mode="subscription" if plan != "one-time" else "payment",
        success_url=success_url,
        cancel_url=cancel_url,
        customer_update={
            "address": "auto",
        },
        metadata={"user_id": user.id, "pk": pk, "price_id": price.id},
    )

    return redirect(checkout_session.url, code=303)


@login_required
def create_customer_portal_session(request):
    user = request.user
    customer = djstripe_models.Customer.objects.get(subscriber=user)

    session = stripe.billing_portal.Session.create(
        customer=customer.id,
        return_url=request.build_absolute_uri(reverse("home")),
    )

    return redirect(session.url, code=303)
{% endif %}
