from rest_framework import serializers

import contest.payout.models
from contest.models import (
    Contest,
    ClosedContest,
    Entry,
    ClosedEntry,
    ContestPool,
    SkillLevel,
)
from draftgroup.classes import DraftGroupManager
from lineup.models import (
    Lineup,
)
from lineup.serializers import (
    PlayerSerializer,
)
from prize.models import PrizeStructure, Rank
from sports.classes import TeamNameCache


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

    @staticmethod
    def get_is_h2h(prize_structure):
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

    @staticmethod
    def get_contest_size(contest_pool):
        return contest_pool.prize_structure.get_entries()

    class Meta:
        model = ContestPool
        fields = ('id', 'name', 'sport', 'start', 'buyin',
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
    start = serializers.SerializerMethodField()
    lineup_name = serializers.SerializerMethodField()
    sport = serializers.SerializerMethodField()

    @staticmethod
    def get_draft_group(entry):
        return entry.contest_pool.draft_group.id

    @staticmethod
    def get_start(entry):
        return entry.contest_pool.start

    @staticmethod
    def get_lineup_name(entry):
        return entry.lineup.name

    @staticmethod
    def get_sport(entry):
        return entry.lineup.sport

    class Meta:
        model = Entry
        fields = (
            'id', 'contest_pool', 'contest', 'lineup', 'draft_group', 'start',
            'lineup_name', 'sport')


class CurrentEntrySerializer(serializers.ModelSerializer):
    """
    serializers for an Entry with a non-null Contest
    """

    draft_group = serializers.SerializerMethodField()
    lineup_name = serializers.SerializerMethodField()
    start = serializers.SerializerMethodField()
    sport = serializers.SerializerMethodField()

    @staticmethod
    def get_draft_group(entry):
        # if entry.contest is None:
        #     return None
        # print('get_draft_group(self, entry):', str(entry), 'contest:', str(entry.contest),
        #         'draft_group:', str(entry.contest.draft_group))
        return entry.contest_pool.draft_group.id

    @staticmethod
    def get_start(entry):
        return entry.contest_pool.start

    @staticmethod
    def get_lineup_name(entry):
        return entry.lineup.name

    @staticmethod
    def get_sport(entry):
        return entry.lineup.sport

    class Meta:
        model = Entry
        fields = (
            'id', 'contest_pool', 'contest', 'lineup', 'draft_group', 'start',
            'lineup_name', 'sport')


class RegisteredUserSerializer(serializers.ModelSerializer):
    """
    serializers for entries in contest, shows id and username
    """
    username = serializers.SerializerMethodField()

    def get_username(self, entry):
        return entry['lineup__user__username']

    class Meta:
        model = Entry
        fields = ('id', 'username')


class EnterLineupSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()

    @staticmethod
    def get_detail(entry):
        return "You entered \"%s\" into the %s!" % (entry.lineup.name, entry.contest_pool.name)

    class Meta:
        model = Entry
        fields = ('id', 'contest_pool', 'lineup', 'detail')


class EnterLineupStatusSerializer(serializers.Serializer):
    task = serializers.CharField()


class PayoutSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    contest = serializers.SerializerMethodField()

    @staticmethod
    def get_user(payout):
        return payout.transaction.user

    @staticmethod
    def get_contest(payout):
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


class SimpleBoxscoreSerialzer(serializers.Serializer):
    """
    A reduced boxscore serializer that will work with all types of sport-specific boxscore models.
    Only contains fields that are in the abstract `sports.models.GameBoxscore` model.
    """
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()

    def get_home_team(self, game):
        return self.get_team_name_from_srid(game.srid_home)

    def get_away_team(self, game):
        return self.get_team_name_from_srid(game.srid_away)

    @staticmethod
    def get_team_name_from_srid(srid):
        tnc = TeamNameCache()
        return tnc.get_team_from_srid(srid).get('alias', 'not found')

    class Meta:
        fields = ('home_team', 'away_team')


class EntryResultSerializer(serializers.ModelSerializer):
    """
    Everything we need to show the results of a contest for a single entry.
        This includes the contest details, prize structure, and other entries
        in the contest.
    """
    contest = ContestSerializer()
    prize_structure = serializers.SerializerMethodField()
    ranked_entries = serializers.SerializerMethodField()
    games = serializers.SerializerMethodField()

    @staticmethod
    def get_games(entry):
        """
        Grab the boxscore for this entry's draftgroup and run it through a very simplified
        serializers, all we need is the team names.
        """
        dgm = DraftGroupManager()
        boxscores = dgm.get_game_boxscores(entry.contest.draft_group)
        games = SimpleBoxscoreSerialzer(boxscores, many=True)
        return games.data

    @staticmethod
    def get_prize_structure(entry):
        prize = PrizeStructureSerializer(entry.contest.prize_structure)
        return prize.data

    @staticmethod
    def get_ranked_entries(entry):
        """
        Get a ranked list of all entries in the contest
        """
        entries = Entry.objects.filter(
            contest=entry.contest).order_by('final_rank').select_related('lineup', 'user')
        ranked_entries = RankedEntrySerializer(entries, many=True)
        return ranked_entries.data

    class Meta:
        model = Entry
        fields = (
            'id', 'final_rank', 'lineup', 'contest', 'prize_structure', 'ranked_entries',
            'games')


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

    @staticmethod
    def get_username(entry):
        return entry.user.username

    fantasy_points = serializers.SerializerMethodField()

    @staticmethod
    def get_fantasy_points(entry):
        return entry.lineup.fantasy_points

    payout = SuccinctPayoutSerializer()

    class Meta:
        model = Entry
        fields = ('username', 'final_rank', 'payout', 'fantasy_points')
