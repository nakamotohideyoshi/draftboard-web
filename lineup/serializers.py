#
# lineup/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from lineup.models import Lineup, Player
from sports.nfl.models import Player as NflPlayer
from sports.nba.models import Player as NbaPlayer
from sports.nhl.models import Player as NhlPlayer
from sports.mlb.models import Player as MlbPlayer
from sports.nfl.models import Team as NflTeam
from sports.nba.models import Team as NbaTeam
from sports.nhl.models import Team as NhlTeam
from sports.mlb.models import Team as MlbTeam
from sports.serializers import PlayerSerializer
import draftgroup.models

class AbstractTeamSerializer:
    FIELDS = ('id', 'alias', 'market', 'name')

class AbstractPlayerSerializer:
    FIELDS = ('first_name', 'last_name', 'status', 'status', 'srid', 'team')

class NflTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model   = NflTeam
        fields  = AbstractTeamSerializer.FIELDS

class NflPlayerSerializer(serializers.ModelSerializer):
    team = NflTeamSerializer()
    class Meta:
        model   = NflPlayer
        fields  = AbstractTeamSerializer.FIELDS

class NbaTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model   = NbaTeam
        fields  = AbstractTeamSerializer.FIELDS

class NbaPlayerSerializer(serializers.ModelSerializer):
    team = NbaTeamSerializer()
    class Meta:
        model   = NbaPlayer
        fields  = AbstractPlayerSerializer.FIELDS

class NhlTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model   = NhlTeam
        fields  = AbstractTeamSerializer.FIELDS

class NhlPlayerSerializer(serializers.ModelSerializer):
    team = NhlTeamSerializer()
    class Meta:
        model   = NhlPlayer
        fields  = AbstractPlayerSerializer.FIELDS

class MlbTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model   = MlbTeam
        fields  = AbstractTeamSerializer.FIELDS

class MlbPlayerSerializer(serializers.ModelSerializer):
    team = MlbTeamSerializer()
    class Meta:
        model   = MlbPlayer
        fields  = AbstractPlayerSerializer.FIELDS

class LineupUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class LineupUsernamesSerializer(serializers.Serializer):
    # contest_id      = args.get('contest_id', None)
    # # get the lineup_ids or the search_str
    # lineup_ids      = args.get('lineup_ids', [])
    # search_str      = args.get('search_str', None)
    contest_id = serializers.IntegerField()
    lineup_ids  = serializers.ListField(
        required=False,
        child=serializers.IntegerField(min_value=0, max_value=9999999),
        help_text="This is an ARRAY of Integer Primary Keys to Lineups"
    )
    search_str  = serializers.CharField(required=False)

class LineupIdSerializer(serializers.ModelSerializer):
    user = LineupUsernameSerializer()

    class Meta:
        model = Lineup
        fields = ('id', 'user')

# Choose the correct serializer for the sport the player plays.
class GenericSportPlayerSerializer(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, NflPlayer):
            serializer = NflPlayerSerializer(value)
        elif isinstance(value, NbaPlayer):
            serializer = NbaPlayerSerializer(value)
        elif isinstance(value, NhlPlayer):
            serializer = NhlPlayerSerializer(value)
        elif isinstance(value, MlbPlayer):
            serializer = MlbPlayerSerializer(value)
        else:
            err_msg = 'Unexpected type of player object [%s] in GenericSportPlayerSerializer' % type(value)
            raise Exception(err_msg)

        return serializer.data

class PlayerSerializer(serializers.ModelSerializer):

    player_meta = GenericSportPlayerSerializer(read_only=True, source='player')
    roster_spot = serializers.StringRelatedField()

    fppg = serializers.SerializerMethodField()
    def get_fppg(self, lineup_player):
        return lineup_player.draft_group_player.fppg

    salary = serializers.SerializerMethodField()
    def get_salary(self, lineup_player):
        return lineup_player.draft_group_player.salary

    fantasy_points = serializers.SerializerMethodField()
    def get_fantasy_points(self, lineup_player):
        return lineup_player.draft_group_player.final_fantasy_points

    class Meta:
        model = Player
        fields = ('player_id', 'full_name', 'roster_spot', 'idx', 'player_meta','fppg','salary', 'fantasy_points')

class LineupSerializer(serializers.ModelSerializer):

    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Lineup
        fields = ('id', 'user', 'name', 'sport', 'fantasy_points', 'draft_group', 'players')

class CreateLineupSerializer(serializers.Serializer):
    draft_group = serializers.IntegerField()

    players = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=9999999),
        help_text="This is an ARRAY of INTEGER primary keys to players in a DraftGroup"
    )

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        draft_group_id = data['draft_group']
        if draft_group_id is None:
            raise serializers.ValidationError("invalid draft_group id")
        try:
            draftgroup.models.DraftGroup.objects.get(pk=draft_group_id)
        except draftgroup.models.DraftGroup.DoesNotExist:
            raise serializers.ValidationError('invalid draft_group id')

        return data


class EditLineupSerializer(serializers.Serializer):

    lineup = serializers.IntegerField(
        help_text='the pk of the Lineup'
    )

    players = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=9999999),
        help_text="This is an ARRAY of INTEGER primary keys to players in a DraftGroup"

    )

    name = serializers.CharField()

class EditLineupStatusSerializer(serializers.Serializer):

    task = serializers.CharField(
        help_text='the task id from a /api/lineup/edit/ api call'
    )