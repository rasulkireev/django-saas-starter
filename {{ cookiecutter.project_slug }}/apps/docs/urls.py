from django.urls import path
from django.views.generic import RedirectView


from apps.docs.views import docs_page_view

urlpatterns = [
    path("", RedirectView.as_view(
      pattern_name='docs_page',
      permanent=False,
      kwargs={'category': 'getting-started', 'page': 'introduction'}
    ), name="docs_home"),
    path("<str:category>/<str:page>/", docs_page_view, name="docs_page"),
]
