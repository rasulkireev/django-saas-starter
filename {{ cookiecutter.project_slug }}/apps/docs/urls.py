from django.urls import path

from apps.docs.views import docs_home_view, docs_page_view

urlpatterns = [
    path("", docs_home_view, name="docs_home"),
    path("<str:category>/<str:page>/", docs_page_view, name="docs_page"),
]
