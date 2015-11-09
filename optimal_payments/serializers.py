#
# optimal_payments/serializers.py

from rest_framework import serializers
from .models import Card

class AddPaymentMethodSerializer(serializers.Serializer):
    """
    serializer for the creation of a payment method.

    primarily this serializer is for the information
    for an Address and a Card
    """

    # billing fields
    billing_nickname    = serializers.CharField()
    street              = serializers.CharField()
    city                = serializers.CharField()
    state               = serializers.CharField()
    country             = serializers.CharField()
    zip                 = serializers.CharField()

    # card fields
    card_nickname       = serializers.CharField()
    holder_name         = serializers.CharField()
    card_num            = serializers.CharField()
    exp_month           = serializers.CharField()
    exp_year            = serializers.CharField()

class PaymentMethodSerializer(serializers.ModelSerializer):
    """
    serializer for displaying Cards on the front end site
    """

    class Meta:
        model = Card
        fields = (
            'oid',
            'last_digits',
            'card_type',
        )

class RemovePaymentMethodSerializer(serializers.Serializer):
    """
    serializer for the params necessary to remove a payment method
    """

    oid    = serializers.CharField()


