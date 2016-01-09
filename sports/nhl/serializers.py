#
# sports.nhl.serializers.py

from rest_framework import serializers
import sports.serializers
from .models import GameBoxscore, Game, Injury, Team, Player

class BoxscoreSerializer(sports.serializers.BoxscoreSerializer):

    class Meta:

        model = GameBoxscore

        fields = sports.serializers.BoxscoreSerializer.PARENT_FIELDS + \
                 ('clock','period')


class GameSerializer(sports.serializers.GameSerializer):

    class Meta:

        model = Game

        fields = sports.serializers.GameSerializer.PARENT_FIELDS + \
                 ('srid_home','srid_away','title')

class InjurySerializer(sports.serializers.InjurySerializer):

    class Meta:

        model = Injury
        fields = ('iid', 'status','description','srid', 'comment', 'player_id')

class TeamSerializer(sports.serializers.TeamSerializer):

    city = serializers.SerializerMethodField()
    def get_city(self, team):
        return team.market

    class Meta:

        model = Team
        fields = sports.serializers.TeamSerializer.PARENT_FIELDS + ('city',)

class FantasyPointsSerializer(sports.serializers.FantasyPointsSerializer):

    # class Meta:
    #     model   = PlayerStats
    #     fields  = ('created','player_id','fantasy_points')

    player_id = serializers.IntegerField()

    fantasy_points = serializers.ListField(
        source='array_agg',
        child=serializers.FloatField() # min_value=-9999, max_value=9999)
    )

class PlayerHistorySerializer(sports.serializers.PlayerHistorySerializer):
    """
    use the fields, especially from the PlayerStats get_scoring_fields()
    """
    player_id = serializers.IntegerField()

    #
    #################################################################
    # the fields below are from the models SCORING_FIELDS
    #################################################################
    avg_goal  = serializers.FloatField()
    goal      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_assist  = serializers.FloatField()
    assist      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_sog  = serializers.FloatField()
    sog      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_blk  = serializers.FloatField()
    blk      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_sh_goal  = serializers.FloatField()
    sh_goal      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_so_goal  = serializers.FloatField()
    so_goal      = serializers.ListField(
        child=serializers.FloatField()
    )

    #
    # goalie stats below

    avg_w  = serializers.FloatField()
    w      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_saves  = serializers.FloatField()
    saves      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_ga  = serializers.FloatField()
    ga      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_shutout  = serializers.FloatField()
    shutout      = serializers.ListField(
        child=serializers.FloatField()
    )

class PlayerSerializer(sports.serializers.PlayerSerializer):
    """
    serializer for this sports player, with more details such as jersey number
    """

    class Meta:

        # sports.<sport>.models.Player
        model = Player

        # fields from the model: sports.<sport>.models.Player
        fields = sports.serializers.PlayerSerializer.PARENT_FIELDS  + ('birth_place',
                                                                       'birthdate',
                                                                       'college',
                                                                       'jersey_number')