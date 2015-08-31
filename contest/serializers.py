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
            'ranks'
        )


class ContestSerializer(serializers.ModelSerializer):
    prize_structure = PrizeStructureSerializer(read_only=True)

    class Meta:

        model = Contest
        fields = ('id','name','sport','status','start',
                  'draft_group','max_entries',
                  'entries','current_entries','gpp',
                  'respawn', 'prize_structure')
