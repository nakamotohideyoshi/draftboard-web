#
# sports.mlb.serializers.py

from rest_framework import serializers
import sports.serializers
from .models import (
    Game,
    GameBoxscore,
    Injury,
    Team,
    Player,

    TsxNews,        # parent: TsxItem
    TsxInjury,      # parent: TsxItem
    TsxTransaction, # parent: TsxItem

    TsxPlayer,      # references TsxItem children
    TsxTeam,        # references TsxItem children
)

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

    #
    #################################################################
    # the fields below are from the models SCORING_FIELDS
    #################################################################

    # raise Exception('UNIMPLEMENTED - mlb.serializers.FantasyPointsSerializer')

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

class TsxItemRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tsxitem' generic relationship.

    A tsxitem maybe a TsxNews, TsxInjury, TsxTransaction, andy child of TsxItem
    """

    def to_representation(self, value):
        """
        serialize the relations
        """
        if isinstance(value, TsxNews):
            return TsxNewsSerializer(value).data
        elif isinstance(value, TsxInjury):
            return TsxInjurySerializer(value).data
        elif isinstance(value, TsxTransaction):
            return TsxTransactionSerializer(value).data

        raise Exception('nhl.serializers.TsxItemRelatedField Unexpected type of TsxItem object: ' + str(type(value)))

class TsxNewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TsxNews
        fields = sports.serializers.TsxItemSerializer.PARENT_FIELDS # there are no more fields

class TsxInjurySerializer(serializers.ModelSerializer):

    class Meta:
        model = TsxInjury
        fields = sports.serializers.TsxItemSerializer.PARENT_FIELDS # there are no more fields

class TsxTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TsxTransaction
        fields = sports.serializers.TsxItemSerializer.PARENT_FIELDS # there are no more fields

class TsxPlayerSerializer(serializers.ModelSerializer):

    tsxitem = TsxItemRelatedField(read_only=True)

    class Meta:
        model = TsxPlayer
        fields = sports.serializers.TsxPlayerSerializer.PARENT_FIELDS + ('tsxitem',)# there are no more fields

class PlayerNewsSerializer(sports.serializers.PlayerNewsSerializer):

    # it is required we set the TsxPlayer class and the TsxPlayerSerializer class
    tsxplayer_class         = TsxPlayer
    tsxplayer_serializer    = TsxPlayerSerializer

    class Meta:
        model = Player
        fields = sports.serializers.PlayerNewsSerializer.PARENT_FIELDS
