from django.urls import path

from apps.api.views import api

urlpatterns = [
    path("", api.urls),
]
