#
# contest/serializers.py

from rest_framework import serializers
from contest.models import Contest, Entry
import contest.payout.models
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

    lineup_name = serializers.SerializerMethodField()
    def get_lineup_name(self, entry):
        return entry.lineup.name

    class Meta:

        model  = Entry
        fields = ('id', 'contest', 'lineup', 'draft_group', 'start', 'lineup_name')

class RegisteredUserSerializer(serializers.Serializer):

    #lineup__user__username  = serializers.CharField()
    total_entries = serializers.IntegerField()

    username = serializers.SerializerMethodField()
    def get_username(self, entry):
        return entry.get('lineup__user__username')

    # class Meta:
    #     fields  = ('total', 'username')

class EnterLineupSerializer(serializers.Serializer):

    contest = serializers.IntegerField()
    lineup = serializers.IntegerField()

class EnterLineupStatusSerializer(serializers.Serializer):

    task = serializers.CharField()

class PayoutSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    def get_user(self, payout):
        return payout.transaction.user

    contest = serializers.SerializerMethodField()
    def get_contest(self, payout):
        return payout.entry.contest

    class Meta:
        model = contest.payout.models.Payout

        fields = ('contest','rank','amount','user')

class EditEntryLineupSerializer(serializers.Serializer):

    entry = serializers.IntegerField(
        help_text='the pk of the Entry'
    )

    players = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=9999999),
        help_text="This is an ARRAY of INTEGER primary keys to players in a DraftGroup"
    )

class EditEntryLineupStatusSerializer(serializers.Serializer):

    task = serializers.CharField()

class RemoveAndRefundEntrySerializer(serializers.Serializer):

    entry = serializers.IntegerField()
