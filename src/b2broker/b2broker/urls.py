from django.urls import path, include

from api import urls as api_urls


urlpatterns = [
    # API
    path("api/", include(("api.urls", "api"), namespace="api")),
]
