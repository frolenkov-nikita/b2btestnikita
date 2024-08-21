import decimal

import pytest

from faker import Faker
from pytest_factoryboy import register
from faker.providers import misc

from api.factories import TransactionFactory, WalletFactory

fake = Faker()
fake.add_provider(misc)

for factory in (
    TransactionFactory,
    WalletFactory,
):
    register(factory)


@pytest.fixture
def make_transaction():
    def _make(**kwargs):
        if "amount" in kwargs:
            kwargs["amount"] = decimal.Decimal(kwargs["amount"])

        return TransactionFactory.create(**kwargs)

    return _make


@pytest.fixture
def make_wallet():
    def _make(**kwargs):
        if "balance" in kwargs:
            kwargs["balance"] = decimal.Decimal(kwargs["balance"])

        return WalletFactory.create(**kwargs)

    return _make


@pytest.fixture
def reload_object():
    def _reload(obj):
        return obj.__class__.objects.get(pk=obj.pk)

    return _reload
