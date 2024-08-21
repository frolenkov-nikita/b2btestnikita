from rest_framework_json_api import serializers

from .models import Wallet, Transaction
from .validators import NonZeroValidator, NonNegativeValidator


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        max_digits=27,
        decimal_places=18,
        read_only=True,
        validators=[NonNegativeValidator(serializers.ValidationError)],
    )

    class Meta:
        model = Wallet
        fields = (
            "id",
            "label",
            "balance",
        )

        read_only_fields = ("balance",)


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=27,
        decimal_places=18,
        validators=[NonZeroValidator(serializers.ValidationError)],
    )
    wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = (
            "txid",
            "wallet",
            "amount",
        )

    def validate(self, data):
        wallet = data["wallet"]

        if (wallet.balance + data["amount"]) < 0:
            raise serializers.ValidationError(
                "Transaction is not possible due to the insufficient amount."
            )

        return data
