#
# contest/serializers.py

from rest_framework import serializers
from contest.models import Contest, Entry
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

class ContestIdSerializer(serializers.ModelSerializer):

    class Meta:

        model   = Contest
        fields  = ('id', 'draft_group')

class CurrentEntrySerializer(serializers.ModelSerializer):

    draft_group = serializers.SerializerMethodField()

    def get_draft_group(self, entry):
        return entry.contest.draft_group.id

    start = serializers.SerializerMethodField()

    def get_start(self, entry):
        return entry.contest.start

    class Meta:

        model  = Entry
        fields = ('id', 'contest', 'lineup', 'draft_group', 'start') #, 'lineup')

class RegisteredUserSerializer(serializers.Serializer):

    #lineup__user__username  = serializers.CharField()
    total_entries = serializers.IntegerField()

    username = serializers.SerializerMethodField()
    def get_username(self, entry):
        return entry.get('lineup__user__username')

    # class Meta:
    #     fields  = ('total', 'username')
