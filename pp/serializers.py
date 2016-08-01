#
# serializers.py

from rest_framework import serializers

class VZeroShippingSerializer(serializers.Serializer):

    first_name          = serializers.CharField(required=True)
    last_name           = serializers.CharField(required=True)
    # company             = serializers.CharField(required=True)    # dont require this
    street_address      = serializers.CharField(required=True)
    extended_address    = serializers.CharField(required=True)      # ie: Suite 15
    locality            = serializers.CharField(required=True)
    region              = serializers.CharField(required=True)
    postal_code         = serializers.CharField(required=True)
    country_code_alpha2 = serializers.CharField(required=True)      # in ['US','CA']

class VZeroDepositSerializer(VZeroShippingSerializer):

    payment_method_nonce    = serializers.CharField(required=True)
    amount                  = serializers.CharField(required=True)