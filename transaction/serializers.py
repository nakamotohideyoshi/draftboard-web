from rest_framework import serializers
from django.contrib.auth.models import User
from transaction.models import TransactionType, Transaction

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ("category", "name", "description")

class TransactionSerializer(serializers.ModelSerializer):
    category = TransactionTypeSerializer()
    class Meta:
        model = Transaction
        fields = ("category",)