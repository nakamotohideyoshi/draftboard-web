#
# dataden/serializers.py

from rest_framework import serializers
from dataden.models import PbpDebug

class PbpDebugSerializer( serializers.ModelSerializer ):

    class Meta:
        model   = PbpDebug
        fields  = (
            'created',
            'game_srid',
            'srid',
            'timestamp_pushered',
            'description',
            'get_delta_seconds',
            'delta_seconds_valid',
        )