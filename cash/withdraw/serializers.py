#
# cash/withdraw/serializers.py

from rest_framework import serializers


class CheckWithdrawSerializer(serializers.Serializer):

    amount = serializers.CharField()


class PayPalWithdrawSerializer(serializers.Serializer):

    amount = serializers.DecimalField(
        max_digits=7, decimal_places=2
    )
    email = serializers.EmailField()
