#
# prize/serializers.py

from rest_framework import serializers
from prize.models import PrizeStructure, Rank

class RankSerializer(serializers.ModelSerializer):

    class Meta:

        model = Rank
        fields = ('rank','value','category')

class PrizeStructureSerializer(serializers.ModelSerializer):

    # ranks must be the 'related_name' in the model of the Rank !!!!
    ranks = RankSerializer(many=True, read_only=True)

    class Meta:

        model   = PrizeStructure
        fields  = ('pk','name', 'prize_pool', 'payout_spots', 'buyin', 'ranks')



