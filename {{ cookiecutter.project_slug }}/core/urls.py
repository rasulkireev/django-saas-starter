from django.urls import path

from core import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("settings", views.UserSettingsView.as_view(), name="settings"),
    path("resend-confirmation/", views.resend_confirmation_email, name="resend_confirmation"),
    {% if cookiecutter.use_stripe == 'y' -%}
    path(
        "create-checkout-session/<int:pk>/<str:plan>/",
        views.create_checkout_session,
        name="user_upgrade_checkout_session",
    ),
    path("create-customer-portal/", views.create_customer_portal_session, name="create_customer_portal_session"),
    {% endif -%}
]
