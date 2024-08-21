from django.db import models
from django.core.validators import MinValueValidator
from django.db import transaction


class WalletManager(models.Manager):
    def perform_transaction(self, wallet: "Wallet", transaction_obj: "Transaction"):
        with transaction.atomic():
            wallet = self.select_for_update().get(pk=wallet.pk)
            wallet.balance += transaction_obj.amount
            wallet.save()

        return wallet


class Wallet(models.Model):
    # if the max length is known in advance, we must consider using CharField with max_length
    label = models.TextField()
    # As per requirement 'amount is a number with 18-digits precision', however the max possible amount is not
    # defined in the requirements, so I set it to < 1 Billion.
    balance = models.DecimalField(
        max_digits=27,
        decimal_places=18,
        default=0,
        validators=[MinValueValidator(0)],
    )

    objects = WalletManager()

    def save(self, *args, **kwargs):
        # So we won't be able to introduce an inconsistency on a framework level
        # However it would be possible to do it via SQL, so if it is required, then we should add a custom DB migration
        # which produces SQL code like
        # ALTER TABLE api_wallet ADD CONSTRAINT CHK_balance CHECK (balance>=0);'
        self.full_clean()

        super().save(*args, **kwargs)


class Transaction(models.Model):
    # It is not possible to have TEXT/BLOB in MySQL as unique, so we have to use CHAR/VARCHAR,
    # the decision here depends on the max length, I set it to 255, which should be large enough, but if the max length
    # is known then we should use different number here.
    # Also, as it is unique - we use it as primary key
    txid = models.CharField(
        max_length=255,
        primary_key=True,
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,  # Sometimes you want to drop everything in one .delete() call but more often
        # you would like to receive the last warning and doublecheck what are you doing.
        editable=False,
    )
    # As per requirements, 'amount is a number with 18-digits precision', however the max possible amount is not
    # defined in the requirements, so I set it to < 1 Million.
    amount = models.DecimalField(
        max_digits=24,
        decimal_places=18,
        editable=False,
    )

    def apply(self):
        self.wallet = Wallet.objects.perform_transaction(self.wallet, self)
