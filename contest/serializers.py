#
# contest/serializers.py

from rest_framework import serializers
from contest.models import (
    Contest,
    ClosedContest,
    Entry,
    ClosedEntry,
    ContestPool,
    SkillLevel,
)
from lineup.models import (
    Lineup,
)
import contest.payout.models
from prize.models import PrizeStructure, Rank
from lineup.serializers import (
    PlayerSerializer,
)


class SkillLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillLevel
        fields = (
            'name',
        )


class RankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rank
        fields = (
            'rank',
            'value',
        )


class PrizeStructureSerializer(serializers.ModelSerializer):

    ranks = RankSerializer(many=True, read_only=True)
    is_h2h = serializers.SerializerMethodField()

    def get_is_h2h(self, prize_structure):
        return prize_structure.get_entries() == 2

    class Meta:
        model = PrizeStructure
        fields = (
            'id',
            'name',
            'buyin',
            'ranks',
            'prize_pool',
            'is_h2h',
        )


class ContestPoolSerializer(serializers.ModelSerializer):

    skill_level = SkillLevelSerializer()
    prize_structure = PrizeStructureSerializer()
    contest_size = serializers.SerializerMethodField()

    def get_contest_size(self, contest_pool):
        return contest_pool.prize_structure.get_entries()

    class Meta:

        model = ContestPool
        fields = ('id', 'name', 'sport', 'status', 'start', 'buyin',
                  'draft_group', 'max_entries', 'prize_structure', 'prize_pool',
                  'entries', 'current_entries', 'contest_size', 'skill_level')


class ContestSerializer(serializers.ModelSerializer):

    skill_level = SkillLevelSerializer()

    class Meta:

        model = Contest
        fields = ('id', 'name', 'sport', 'status', 'start', 'buyin',
                  'draft_group', 'max_entries', 'prize_structure', 'prize_pool',
                  'entries', 'current_entries', 'gpp', 'doubleup',
                  'respawn', 'skill_level')


class ContestIdSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contest
        fields = ('id', 'draft_group')


class UpcomingEntrySerializer(serializers.ModelSerializer):
    """
    serializer for an Entry in an upcoming ContestPool
    """
    draft_group = serializers.SerializerMethodField()

    def get_draft_group(self, entry):
        return entry.contest_pool.draft_group.id

    start = serializers.SerializerMethodField()

    def get_start(self, entry):
        return entry.contest_pool.start

    lineup_name = serializers.SerializerMethodField()

    def get_lineup_name(self, entry):
        return entry.lineup.name

    sport = serializers.SerializerMethodField()

    def get_sport(self, entry):
        return entry.lineup.sport

    class Meta:

        model = Entry
        fields = ('id', 'contest_pool', 'contest', 'lineup', 'draft_group', 'start', 'lineup_name', 'sport')


class CurrentEntrySerializer(serializers.ModelSerializer):
    """
    serializers for an Entry with a non-null Contest
    """

    draft_group = serializers.SerializerMethodField()

    def get_draft_group(self, entry):
        # if entry.contest is None:
        #     return None
        # print('get_draft_group(self, entry):', str(entry), 'contest:', str(entry.contest),
        #         'draft_group:', str(entry.contest.draft_group))
        return entry.contest_pool.draft_group.id

    start = serializers.SerializerMethodField()

    def get_start(self, entry):
        return entry.contest_pool.start

    lineup_name = serializers.SerializerMethodField()

    def get_lineup_name(self, entry):
        return entry.lineup.name

    sport = serializers.SerializerMethodField()

    def get_sport(self, entry):
        return entry.lineup.sport

    class Meta:

        model = Entry
        fields = ('id', 'contest_pool', 'contest', 'lineup', 'draft_group', 'start', 'lineup_name', 'sport')


class RegisteredUserSerializer(serializers.ModelSerializer):
    """
    serializers for entries in contest, shows id and username
    """
    username = serializers.SerializerMethodField()

    def get_username(self, entry):
        return entry.lineup.user.username

    class Meta:
        model = Entry
        fields = ('id', 'username')


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

        fields = ('contest', 'rank', 'amount', 'user')


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

    entry = serializers.IntegerField(help_text='the id of the Entry to remove and refund')


class RemoveAndRefundEntryStatusSerializer(serializers.Serializer):

    task = serializers.CharField()


class SuccinctPayoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = contest.payout.models.Payout

        fields = ('amount',)


class SuccinctContestSerializer(serializers.ModelSerializer):
    """
    limited number of contest properties (basically just the name)
    """
    class Meta:

        model = ClosedContest
        fields = ('id', 'name', 'status')


class EntrySerializer(serializers.ModelSerializer):
    """
    Entry object serializer for the UserLineupHistorySerializer primarily
    """

    contest = SuccinctContestSerializer()

    payout = SuccinctPayoutSerializer()

    class Meta:
        model = ClosedEntry
        fields = ('id', 'final_rank', 'contest', 'payout',)


class UserLineupHistorySerializer(serializers.ModelSerializer):
    """
    primarily returns Entry data, containing information about the Contest, and payouts
    """

    # entries = serializers.SerializerMethodField()
    # def get_entries(self, lineup):
    #     return EntrySerializer(many=True, read_only=True)

    entries = EntrySerializer(many=True, read_only=True)

    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Lineup
        fields = ('id', 'players', 'entries', 'name', 'sport',)


class RankedEntrySerializer(serializers.ModelSerializer):
    """
    for an entry in a contest that has been paid out.
    there may or may not be a payout, but this entry
    should be ranked and have fantasy points for the lineup
    """

    username = serializers.SerializerMethodField()

    def get_username(self, entry):
        return entry.user.username

    fantasy_points = serializers.SerializerMethodField()

    def get_fantasy_points(self, entry):
        return entry.lineup.fantasy_points

    payout = SuccinctPayoutSerializer()

    class Meta:

        model = Entry
        fields = ('username', 'final_rank', 'payout', 'fantasy_points')
