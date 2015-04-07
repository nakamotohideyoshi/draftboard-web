from rest_framework import serializers
from cash.models import CashTransactionDetail
from transaction.serializers import TransactionTypeSerializer, TransactionSerializer



class CashTransactionDetailSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    class Meta:
        model = CashTransactionDetail
        fields = ("amount", "created","transaction")

