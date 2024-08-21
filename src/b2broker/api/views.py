from rest_framework import viewsets, mixins
from rest_framework_json_api import filters
from rest_framework_json_api import django_filters
from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from . import serializers
from .models import Transaction, Wallet


class FilterMixin:
    # Filters: as per docs DjangoFilter: "This filter is not part of the JSON:API standard per-se, other than the
    # requirement to use the filter keyword: It is an optional implementation of a style of filtering in which
    # each filter is an ORM expression as implemented by DjangoFilterBackend and seems to be in alignment with
    # an interpretation of the JSON:API recommendations, including relationship chaining."
    # <--- Looks like a good solution.
    filter_backends = (
        filters.QueryParameterValidationFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    )


class PaginationMixin:
    pagination_class = JsonApiPageNumberPagination


class APIV1Mixin(PaginationMixin, FilterMixin):
    # Permissions, authorization, authentication are not implemented, but are mandatory for the real service
    # This is the good place to define permission_classes & authentication_classes
    default_version = "v1"


# Delete operation is not provided as there is nothing about it in requirements.
class WalletViewset(
    APIV1Mixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.WalletSerializer
    queryset = Wallet.objects.all().order_by("pk")
    filterset_fields = {
        # the ones that make the most sense from my point of view
        # however we need to consider the DB performance here
        "id": ("exact", "in"),
        "label": ("icontains", "iexact", "contains"),
        "balance": ("exact", "lt", "gt", "gte", "lte"),
    }


class TransactionViewset(
    APIV1Mixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.TransactionSerializer
    queryset = Transaction.objects.all()
    filterset_fields = {
        # the ones that make the most sense from my point of view
        # however we need to consider the DB performance here
        "wallet": ("exact", "in"),
        "txid": ("exact", "in"),
        "amount": ("exact", "lt", "gt", "gte", "lte"),
    }

    def perform_create(self, serializer):
        transaction = serializer.save()
        # In theory, it should be possible for the "invalid" transaction to pass the validation process,
        # but then we should have an error on a DB/models level, which is not handled here intentionally.
        # 5xx responses would be handled by the monitoring/error reporting services, and we would notice that something
        # nasty is going on and the proper team would be notified.
        transaction.apply()
