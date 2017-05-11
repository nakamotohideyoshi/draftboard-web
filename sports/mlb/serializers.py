#
# sports.mlb.serializers.py

import json
from ast import literal_eval
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
                 ('srid_home','srid_away','title','day_night','game_number')

class InjurySerializer(sports.serializers.InjurySerializer):

    class Meta:

        model = Injury

        fields = sports.serializers.InjurySerializer.PARENT_FIELDS #

class TeamSerializer(sports.serializers.TeamSerializer):

    city = serializers.SerializerMethodField()
    def get_city(self, team):
        return team.market

    class Meta:

        model = Team
        fields = sports.serializers.TeamSerializer.PARENT_FIELDS + ('city',)

class FantasyPointsSerializer(sports.serializers.FantasyPointsSerializer):

    player_id = serializers.IntegerField()

    #
    #################################################################
    # the fields below are from the models SCORING_FIELDS
    #################################################################

    # raise Exception('UNIMPLEMENTED - mlb.serializers.FantasyPointsSerializer')
    fantasy_points = serializers.ListField(
        source='array_agg',
        child=serializers.FloatField(), # min_value=-9999, max_value=9999)
        help_text="This is an ARRAY of FLOAT fantasy points for trailing games"

    )

class PlayerHistoryHitterSerializer(sports.serializers.PlayerHistorySerializer):
    """
    use the fields, especially from the PlayerStats get_scoring_fields()
    """
    player_id = serializers.IntegerField()

    # from nba PlayerStats.SCORING_FIELDS
    avg_s   = serializers.FloatField()
    s       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_d   = serializers.FloatField()
    d       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_t   = serializers.FloatField()
    t       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_hr   = serializers.FloatField()
    hr       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_rbi   = serializers.FloatField()
    rbi       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_r   = serializers.FloatField()
    r       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_bb   = serializers.FloatField()
    bb       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_hbp   = serializers.FloatField()
    hbp       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_sb   = serializers.FloatField()
    sb       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_cs   = serializers.FloatField()
    cs       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    h = serializers.SerializerMethodField()

    @staticmethod
    def get_h(obj):
        """
        Since we don't save hits to the DB, add up singles, doubles, triples and HRs
        to determine them.
        :param obj: 
        :return: list 
        """
        h = []
        for key, value in enumerate(obj['s']):
            h.append(obj['s'][key] + obj['d'][key] + obj['t'][key] + obj['hr'][key])
        return h


class PlayerHistoryPitcherSerializer(sports.serializers.PlayerHistorySerializer):
    """
    use the fields, especially from the PlayerStats get_scoring_fields()
    """
    player_id = serializers.IntegerField()

    # from scoring fields dont avg
    win       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    loss       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    qstart       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    cg       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    #
    # cgso
    # nono

    # from scoring fields
    avg_ip_1   = serializers.FloatField()
    ip_1       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_ktotal   = serializers.FloatField()
    ktotal       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_er   = serializers.FloatField()
    er       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_h   = serializers.FloatField()
    h       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
    )

    avg_bb   = serializers.FloatField()
    bb       = serializers.ListField(
        child=serializers.IntegerField(),  help_text="This is an ARRAY of INTEGERS"
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
