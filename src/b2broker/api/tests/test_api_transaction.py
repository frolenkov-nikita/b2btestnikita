import decimal

import pytest
from pytest_drf import (
    ViewSetTest,
    Returns200,
    Returns201,
    Returns400,
    Returns405,
    UsesListEndpoint,
    UsesGetMethod,
    UsesPostMethod,
    UsesPatchMethod,
    UsesDetailEndpoint,
)
from pytest_drf.util import url_for
from pytest_lambda import lambda_fixture

from api.models import Wallet, Transaction


@pytest.mark.django_db
class TestTransactionViewset(ViewSetTest):
    balance = lambda_fixture(lambda: "546.6565768979")
    pos_amount = lambda_fixture(lambda: "513.6565768979")
    neg_amount = lambda_fixture(lambda: "-113.6565768979")
    wallet = lambda_fixture(
        lambda make_wallet, balance: make_wallet(
            balance=balance,
        ),
        autouse=True,
    )
    pos_transaction = lambda_fixture(
        lambda make_transaction, wallet, pos_amount: make_transaction(
            wallet=wallet,
            amount=pos_amount,
        )
    )
    neg_transaction = lambda_fixture(
        lambda make_transaction, wallet, neg_amount: make_transaction(
            wallet=wallet,
            amount=neg_amount,
        )
    )
    detail_url = lambda_fixture(
        lambda pos_transaction: url_for("api:transaction-detail", pos_transaction.pk)
    )
    list_url = lambda_fixture(lambda wallet: url_for("api:transaction-list"))

    class TestRetrieve(
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        def test(self, pos_transaction, wallet, json):
            # confirm the JSON API spec (can be easily/accidentally turned off)
            assert json == {
                "data": {
                    "type": "Transaction",
                    "id": pos_transaction.pk,
                    "attributes": {
                        "txid": pos_transaction.pk,
                        "amount": f"{pos_transaction.amount:.18f}",
                    },
                    "relationships": {
                        "wallet": {"data": {"type": "Wallet", "id": str(wallet.pk)}}
                    },
                }
            }

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        data = lambda_fixture(
            lambda pos_amount, wallet: {
                "data": {
                    "type": "Transaction",
                    "attributes": {
                        "txid": "SomeID",
                        "amount": pos_amount,
                        "wallet": str(wallet.pk),
                    },
                }
            }
        )

        def test(self, json, balance, pos_amount):
            wallet = Wallet.objects.get(
                pk=json["data"]["relationships"]["wallet"]["data"]["id"]
            )
            transaction = Transaction.objects.get(pk=json["data"]["id"])

            assert transaction.txid == "SomeID"
            assert transaction.amount == decimal.Decimal(pos_amount)
            assert transaction.wallet == wallet
            assert wallet.balance == decimal.Decimal(balance) + decimal.Decimal(
                pos_amount
            )

    class TestCreateInvalid(
        UsesPostMethod,
        UsesListEndpoint,
        Returns400,
    ):
        wallet = lambda_fixture(
            lambda make_wallet, balance: make_wallet(
                balance=0,
            ),
            autouse=True,
        )
        data = lambda_fixture(
            lambda neg_amount, wallet: {
                "data": {
                    "type": "Transaction",
                    "attributes": {
                        "txid": "SomeAnotherID",
                        "amount": neg_amount,
                        "wallet": str(wallet.pk),
                    },
                }
            }
        )

        def test(self, json):
            assert json["errors"]

    class TestUpdateNotAllowed(
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns405,
    ):
        data = lambda_fixture(lambda: {})

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        transactions = lambda_fixture(
            lambda make_transaction: [make_transaction() for _ in range(5)],
            autouse=True,
        )

        def test(self, json):
            assert len(json["data"]) == 5
            assert json["meta"]["pagination"]

    class TestFilter(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        transactions = lambda_fixture(
            lambda make_transaction: [
                make_transaction(amount=a + 1) for a in range(10)
            ],
            autouse=True,
        )
        list_url = lambda_fixture(
            lambda wallet: url_for("api:transaction-list") + "?filter[amount__gt]=4"
        )

        def test(self, json):
            # test that JSON API filtering syntax works
            assert len(json["data"]) == Transaction.objects.filter(amount__gt=4).count()
            assert json["meta"]["pagination"]

    class TestOrdering(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        transactions = lambda_fixture(
            lambda make_transaction: [make_transaction(amount=a + 1) for a in range(5)],
            autouse=True,
        )
        list_url = lambda_fixture(
            lambda wallet: url_for("api:transaction-list") + "?sort=-amount"
        )

        def test(self, json):
            # test that JSON API ordering syntax works
            assert list(
                Transaction.objects.order_by("-amount").values_list("txid", flat=True)
            ) == [d["id"] for d in json["data"]]
