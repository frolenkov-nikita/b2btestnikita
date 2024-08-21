from django.urls import path, include

from rest_framework import routers
from drf_spectacular import views as spectacular_views

from . import views


router = routers.SimpleRouter()


router.register(r"wallet", views.WalletViewset, basename="wallet")
router.register(r"transaction", views.TransactionViewset, basename="transaction")


urlpatterns = [
    # API
    path("v1/", include(router.urls)),
    # schema
    path("v1/schema/", spectacular_views.SpectacularAPIView.as_view(), name="schema"),
    path(
        "v1/schema/ui/",
        spectacular_views.SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger-ui",
    ),
    path(
        "v1/schema/redoc/",
        spectacular_views.SpectacularRedocView.as_view(url_name="api:schema"),
        name="redoc",
    ),
]
