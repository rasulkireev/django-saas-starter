from django.urls import path
from django.views.generic import RedirectView


from apps.docs.views import docs_page_view

urlpatterns = [
    path("", RedirectView.as_view(
        url="/docs/getting-started/introduction/",
        permanent=False,
    ), name="docs_home"),
    path("<str:category>/<str:page>/", docs_page_view, name="docs_page"),
]
