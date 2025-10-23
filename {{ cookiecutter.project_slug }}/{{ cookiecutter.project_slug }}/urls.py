"""{{ cookiecutter.project_slug }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from {{ cookiecutter.project_slug }}.sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("anymail/", include("anymail.urls")),
    path("uses", TemplateView.as_view(template_name="pages/uses.html"), name="uses"),
    {% if cookiecutter.use_stripe == 'y' -%}
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    {% endif %}
    {% if cookiecutter.generate_blog == 'y' -%}
    path("blog/", include("blog.urls")),
    {% endif %}
    path("api/", include("api.urls")),
    path("", include("core.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
