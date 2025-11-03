from django.urls import path

from pages import views

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing"),
    path("privacy-policy", views.PrivacyPolicyView.as_view(), name="privacy_policy"),
    path("terms-of-service", views.TermsOfServiceView.as_view(), name="terms_of_service"),
    {% if cookiecutter.use_stripe == 'y' -%}
    path("pricing", views.PricingView.as_view(), name="pricing"),
    {% endif %}
]
