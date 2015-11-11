#
# cash/withdraw/serializers.py

from rest_framework import serializers

class CheckWithdrawSerializer(serializers.Serializer):

    amount = serializers.CharField()

class PayPalWithdrawSerializer(serializers.Serializer):

    amount  = serializers.CharField()
    email   = serializers.CharField()