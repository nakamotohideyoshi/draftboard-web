#
# contest/serializers.py

from rest_framework import serializers
from contest.models import Contest
from prize.models import PrizeStructure, Rank

class RankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rank

class PrizeStructureSerializer(serializers.ModelSerializer):

    ranks = RankSerializer(many=True, read_only=True)

    class Meta:
        model = PrizeStructure
        fields = (
            'id',
            'name',
            'buyin',
            'generator',
            'ranks',
            'prize_pool'
        )

class ContestSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contest
        fields = ('id','name','sport','status','start','buyin',
                  'draft_group','max_entries', 'prize_structure','prize_pool',
                  'entries','current_entries','gpp','doubleup',
                  'respawn')

