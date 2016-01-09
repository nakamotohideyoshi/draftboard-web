#
# sports.mlb.serializers.py

from rest_framework import serializers
import sports.serializers
from .models import Game, GameBoxscore, Injury, Team, Player

class BoxscoreSerializer(sports.serializers.BoxscoreSerializer):

    class Meta:

        model = GameBoxscore

        fields = sports.serializers.BoxscoreSerializer.PARENT_FIELDS + \
                 ('day_night','game_number','inning','inning_half',
                  'srid_home_pp','srid_home_sp',
                  'srid_away_pp','srid_away_sp',
                  'srid_win','srid_loss',
                  'home_errors', 'home_hits',
                  'away_errors', 'away_hits',)


class GameSerializer(sports.serializers.GameSerializer):

    class Meta:

        model = Game

        fields = sports.serializers.GameSerializer.PARENT_FIELDS + \
                 ('srid_home','srid_away','title','day_night','game_number')

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

class PlayerSerializer(sports.serializers.PlayerSerializer):
    """
    serializer for this sports player, with more details such as jersey number
    """

    class Meta:

        # sports.<sport>.models.Player
        model = Player

        # fields from the model: sports.<sport>.models.Player
        fields = sports.serializers.PlayerSerializer.PARENT_FIELDS  + ('birthcity', 'birthcountry',
                                                                       'birthdate',
                                                                       'college',
                                                                       'jersey_number')