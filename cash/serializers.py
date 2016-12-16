#
# cash/serializers.py

from rest_framework import serializers
from cash.models import CashTransactionDetail
from transaction.serializers import TransactionSerializer


class CashTransactionDetailSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()

    class Meta:
        model = CashTransactionDetail
        fields = ("amount", "created","transaction")


class TransactionHistorySerializer(serializers.Serializer):
    created = serializers.DateField()
    id = serializers.IntegerField()


class BalanceSerializer(serializers.Serializer):
    cash_balance = serializers.SerializerMethodField()
    deposit_sum = serializers.SerializerMethodField()
    deposit_limit = serializers.SerializerMethodField()

    def get_cash_balance(self, obj):
        return obj.get_balance_amount()

    def get_deposit_sum(self, obj):
        return obj.user.information.deposits_for_period

    def get_deposit_limit(self, obj):
        return obj.user.information.deposits_limit


