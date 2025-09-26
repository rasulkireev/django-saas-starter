from django.urls import path

from core import views
from core.api.views import api

urlpatterns = [
    # pages
    path("", views.HomeView.as_view(), name="home"),
    path("settings", views.UserSettingsView.as_view(), name="settings"),
    {% if cookiecutter.generate_blog == 'y' -%}
    # blog
    path("blog", views.BlogView.as_view(), name="blog_posts"),
    path("blog/<slug:slug>", views.BlogPostView.as_view(), name="blog_post"),
    {% endif %}
    # app
    path("api/", api.urls),
    # utils
    path("resend-confirmation/", views.resend_confirmation_email, name="resend_confirmation"),
    {% if cookiecutter.use_stripe == 'y' -%}
    # payments
    path("pricing", views.PricingView.as_view(), name="pricing"),
    path(
        "create-checkout-session/<int:pk>/<str:plan>/",
        views.create_checkout_session,
        name="user_upgrade_checkout_session",
    ),
    path(
      "create-customer-portal/",
      views.create_customer_portal_session,
      name="create_customer_portal_session"
    ),
    {% endif %}
]
