import decimal

import pytest
from pytest_drf import (
    ViewSetTest,
    Returns200,
    Returns201,
    UsesListEndpoint,
    UsesGetMethod,
    UsesPostMethod,
    UsesPatchMethod,
    UsesDetailEndpoint,
)
from pytest_drf.util import url_for
from pytest_lambda import lambda_fixture

from api.models import Wallet


@pytest.mark.django_db
class TestWalletViewset(ViewSetTest):
    detail_url = lambda_fixture(lambda wallet: url_for("api:wallet-detail", wallet.pk))
    list_url = lambda_fixture(lambda wallet: url_for("api:wallet-list"))
    balance = lambda_fixture(lambda: "353894717.23124305983")
    wallet = lambda_fixture(
        lambda make_wallet, balance: make_wallet(
            label="My wallet",
            balance=balance,
        ),
        autouse=True,
    )

    class TestRetrieve(
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        def test(self, wallet, json):
            # confirm the JSON API spec (can be easily/accidentally turned off)
            assert json == {
                "data": {
                    "type": "Wallet",
                    "id": str(wallet.pk),
                    "attributes": {
                        "label": "My wallet",
                        "balance": f"{wallet.balance:.18f}",
                    },
                }
            }

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        data = lambda_fixture(
            lambda balance: {
                "data": {
                    "type": "Wallet",
                    "attributes": {"label": "My new wallet", "balance": balance},
                }
            }
        )

        def test(self, json):
            wallet = Wallet.objects.get(pk=json["data"]["id"])

            # cannot create a wallet with balance != 0
            assert wallet.balance == 0
            assert wallet.label == "My new wallet"

    class TestUpdate(
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        data = lambda_fixture(
            lambda wallet: {
                "data": {
                    "type": "Wallet",
                    "id": str(wallet.pk),
                    "attributes": {"label": "My changed wallet", "balance": "0"},
                }
            }
        )

        def test(self, balance, json):
            wallet = Wallet.objects.get(pk=json["data"]["id"])

            # cannot change wallet's balance this way
            assert wallet.balance == decimal.Decimal(balance)
            assert wallet.label == "My changed wallet"

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        wallets = lambda_fixture(
            lambda make_wallet: [make_wallet() for _ in range(5)],
            autouse=True,
        )

        def test(self, json):
            assert (
                len(json["data"]) == 5 + 1
            )  # 5 from wallets, 1 from wallet global fixture
            assert json["meta"]["pagination"]

    class TestFilter(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        wallets = lambda_fixture(
            lambda make_wallet: [make_wallet(balance=b) for b in range(10)],
            autouse=True,
        )
        list_url = lambda_fixture(
            lambda wallet: url_for("api:wallet-list") + "?filter[balance__gt]=4"
        )

        def test(self, json):
            # test that JSON API filtering syntax works
            assert len(json["data"]) == Wallet.objects.filter(balance__gt=4).count()
            assert json["meta"]["pagination"]

    class TestOrdering(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        wallets = lambda_fixture(
            lambda make_wallet: [make_wallet(balance=b) for b in range(5)],
            autouse=True,
        )
        list_url = lambda_fixture(
            lambda wallet: url_for("api:wallet-list") + "?sort=-balance"
        )

        def test(self, json):
            # test that JSON API ordering syntax works

            assert list(
                Wallet.objects.order_by("-balance").values_list("pk", flat=True)
            ) == [int(d["id"]) for d in json["data"]]
