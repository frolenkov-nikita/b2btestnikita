import pytest
from pytest_lambda import lambda_fixture

from api.models import Wallet, Transaction


@pytest.mark.django_db
class ModelTestCase:
    balance = lambda_fixture(lambda: "10.23124305983")
    pos_amount = lambda_fixture(lambda: "5.23124305983")
    neg_amount = lambda_fixture(lambda: "-5.23124305983")
    wallet = lambda_fixture(
        lambda make_wallet, balance: make_wallet(
            balance=balance,
        ),
        autouse=True,
    )


class TestTransaction(ModelTestCase):
    transaction = lambda_fixture(lambda make_transaction: make_transaction())

    def test_apply(self, transaction):
        wallet_balance = transaction.wallet.balance
        # test that transaction.wallet.balance was updated, no need to mock here
        transaction.apply()

        assert transaction.wallet.balance != wallet_balance

    def test_cannot_create_invalid(self):
        with pytest.raises(Exception):
            Transaction.objects.create(amount=0, txid="Someid")

    def test_cannot_update_to_invalid(self, transaction):
        with pytest.raises(Exception):
            Transaction.objects.filter(pk=transaction.pk).update(amount=0)


class TestWallet(ModelTestCase):
    balance = lambda_fixture(lambda: 0)
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

    def test_valid_transaction(self, wallet, pos_transaction):
        wallet = Wallet.objects.perform_transaction(wallet, pos_transaction)

        assert wallet.balance == pos_transaction.amount

    def test_invalid_transaction(self, wallet, neg_transaction, reload_object):
        with pytest.raises(Exception):
            wallet = Wallet.objects.perform_transaction(wallet, neg_transaction)

        wallet = reload_object(wallet)
        assert wallet.balance == 0

    def test_cannot_create_invalid(self):
        with pytest.raises(Exception):
            Wallet.objects.create(amount=-1, txid="Someid")

    def test_cannot_update_to_invalid(self, wallet):
        with pytest.raises(Exception):
            Wallet.objects.filter(pk=wallet.pk).update(amount=-1)
