import factory
from factory import fuzzy
from faker import Factory as FakerFactory

from api.models import Transaction, Wallet


faker = FakerFactory.create()


class WalletFactory(factory.django.DjangoModelFactory):
    label = factory.LazyAttribute(lambda x: faker.name())
    balance = fuzzy.FuzzyDecimal(1e-18, 1e9 - 1e-18)

    class Meta:
        model = Wallet


class TransactionFactory(factory.django.DjangoModelFactory):
    txid = factory.LazyAttribute(
        # the best option from builtin providers,
        # it is possible to find better in community
        lambda x: faker.md5(raw_output=False)
    )
    wallet = factory.SubFactory(WalletFactory)
    amount = fuzzy.FuzzyDecimal(-1e-18, 1e6 - 1e-18)

    class Meta:
        model = Transaction
