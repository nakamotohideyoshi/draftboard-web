#
# sports.nba.serializers.py

from rest_framework import serializers
import sports.serializers
from .models import Game, GameBoxscore, Injury, Team, Player

class BoxscoreSerializer(sports.serializers.BoxscoreSerializer):

    class Meta:

        model = GameBoxscore

        fields = sports.serializers.BoxscoreSerializer.PARENT_FIELDS + \
                 ('clock','duration','lead_changes','quarter','times_tied')


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
    avg_points  = serializers.FloatField()
    points      = serializers.ListField(
        child=serializers.FloatField()
    )

    # from nba PlayerStats.SCORING_FIELDS
    avg_three_points_made   = serializers.FloatField()
    three_points_made       = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_rebounds  = serializers.FloatField()
    rebounds      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_assists  = serializers.FloatField()
    assists      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_steals  = serializers.FloatField()
    steals      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_blocks  = serializers.FloatField()
    blocks      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_turnovers  = serializers.FloatField()
    turnovers      = serializers.ListField(
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