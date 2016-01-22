from rest_framework import serializers
from cash.models import CashTransactionDetail
from transaction.serializers import TransactionTypeSerializer, TransactionSerializer
import django_filters



class CashTransactionDetailSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    class Meta:
        model = CashTransactionDetail
        fields = ("amount", "created","transaction")


class TransactionHistorySerializer(serializers.Serializer):
    created = serializers.DateField()
    id = serializers.IntegerField()


class BalanceSerializer(serializers.Serializer):
    pass


