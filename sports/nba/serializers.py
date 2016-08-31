#
# sports.nba.serializers.py

from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
import json
from ast import literal_eval
from itertools import chain
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
                 ('clock','duration','lead_changes','quarter','times_tied','updated')


class GameSerializer(sports.serializers.GameSerializer):

    boxscore = serializers.SerializerMethodField()
    def get_boxscore(self, game):
        boxscore_data = game.boxscore_data
        if boxscore_data is not None:
            ast_j = literal_eval(boxscore_data)
            boxscore_data = json.loads(json.dumps(ast_j))
        return boxscore_data


    class Meta:

        model = Game

        fields = sports.serializers.GameSerializer.PARENT_FIELDS + \
                 ('srid_home','srid_away','title','updated')

class InjurySerializer(sports.serializers.InjurySerializer):

    class Meta:

        model = Injury

        fields = sports.serializers.InjurySerializer.PARENT_FIELDS + \
                                                ('srid', 'comment')

class TeamSerializer(sports.serializers.TeamSerializer):

    city = serializers.SerializerMethodField()
    def get_city(self, team):
        return team.market

    class Meta:

        model = Team
        fields = sports.serializers.TeamSerializer.PARENT_FIELDS + ('city',)

class FantasyPointsSerializer(sports.serializers.FantasyPointsSerializer):

    player_id = serializers.IntegerField()

    fantasy_points = serializers.ListField(
        source='array_agg',
        child=serializers.FloatField(), # min_value=-9999, max_value=9999)
        help_text="This is an ARRAY of FLOAT fantasy points for trailing games"

    )

class PlayerHistorySerializer(sports.serializers.PlayerHistorySerializer):
    """
    use the fields, especially from the PlayerStats get_scoring_fields()
    """
    player_id = serializers.IntegerField()

    #games       = serializers.Char
    #
    #################################################################
    # the fields below are from the models SCORING_FIELDS
    #################################################################
    avg_points  = serializers.FloatField()

    points      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    # from nba PlayerStats.SCORING_FIELDS
    avg_three_points_made   = serializers.FloatField()
    three_points_made       = serializers.ListField(
        child=serializers.FloatField(),  help_text="This is an ARRAY of FLOATS"
    )

    avg_rebounds  = serializers.FloatField()
    rebounds      = serializers.ListField(
        child=serializers.FloatField(),  help_text="This is an ARRAY of FLOATS"
    )

    avg_assists  = serializers.FloatField()
    assists      = serializers.ListField(
        child=serializers.FloatField(),  help_text="This is an ARRAY of FLOATS"
    )

    avg_steals  = serializers.FloatField()
    steals      = serializers.ListField(
        child=serializers.FloatField(),  help_text="This is an ARRAY of FLOATS"
    )

    avg_blocks  = serializers.FloatField()
    blocks      = serializers.ListField(
        child=serializers.FloatField(),  help_text="This is an ARRAY of FLOATS"
    )

    avg_turnovers  = serializers.FloatField()
    turnovers      = serializers.ListField(
        child=serializers.FloatField(),  help_text="This is an ARRAY of FLOATS"
    )

    avg_minutes  = serializers.FloatField()
    minutes      = serializers.ListField(
        child=serializers.FloatField(),  help_text="This is an ARRAY of FLOATS"
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

class TsxItemRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tsxitem' generic relationship.

    A tsxitem maybe a TsxNews, TsxInjury, TsxTransaction, andy child of TsxItem
    """

    def to_representation(self, value):
        """
        serialize the relations
        """

        # print(str(type(value)))
        # print(str(type(value)))
        # print(str(type(value)))

        # ctype = ContentType.objects.get_for_model(value)
        # print('')
        # print(str(ref_obj))
        # tsxref, c = tsx_ref_model_class.objects.get_or_create( tsxitem_type=ctype,
        #                                                       tsxitem_id=ctype.pk)

        if isinstance(value, TsxNews):
            #return TsxNewsSerializer(value).data
            return TsxNewsSerializer(value).data #TsxNews.objects.all(), many=True).data
        elif isinstance(value, TsxInjury):
            #return TsxInjurySerializer(value).data
            return TsxInjurySerializer(value).data #TsxInjury.objects.all(), many=True).data
        elif isinstance(value, TsxTransaction):
            #return TsxTransactionSerializer(value).data
            return TsxTransactionSerializer(value).data #TsxTransaction.objects.all(), many=True).data

        #return
        # this works
        # return json.dumps({
        #     'title'     : value.title,
        #     'byline'    : value.byline,
        # })

        #
        # this stuff below was for testing --- should remove it!
        # if isinstance(value, TsxNews) or isinstance(value, TsxInjury) or isinstance(value, TsxTransaction):
        #     # return 'TsxNews: ' + value.title
        #     return TsxNewsSerializer(value)
        # elif isinstance(value, Note):
        #     return 'Note: ' + value.text
        raise Exception('nba.serializers.TsxItemRelatedField Unexpected type of TsxItem object: ' + str(type(value)))

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
