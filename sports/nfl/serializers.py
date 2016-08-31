#
# sports.nfl.serializers.py

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
import json
from ast import literal_eval

class BoxscoreSerializer(sports.serializers.BoxscoreSerializer):

    class Meta:

        model = GameBoxscore

        fields = sports.serializers.BoxscoreSerializer.PARENT_FIELDS + \
                 ('clock','completed','quarter')


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

        # parent fields include the 'boxscore' field
        fields = sports.serializers.GameSerializer.PARENT_FIELDS + \
                 ('srid_home','srid_away','title', 'weather_json')

class InjurySerializer(sports.serializers.InjurySerializer):

    class Meta:

        model = Injury
        fields = sports.serializers.InjurySerializer.PARENT_FIELDS + \
                                                ('srid', 'practice_status')

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
        child=serializers.FloatField(), # min_value=-9999, max_value=9999)
        help_text="This is an ARRAY of FLOAT fantasy points"
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
    avg_pass_td  = serializers.FloatField()
    pass_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_pass_yds  = serializers.FloatField()
    pass_yds      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_pass_int  = serializers.FloatField()
    pass_int      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_rush_td  = serializers.FloatField()
    rush_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_rush_yds  = serializers.FloatField()
    rush_yds      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_rec_td  = serializers.FloatField()
    rec_td     = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_rec_yds  = serializers.FloatField()
    rec_yds      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_rec_rec  = serializers.FloatField()
    rec_rec      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_off_fum_lost  = serializers.FloatField()
    off_fum_lost      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_two_pt_conv  = serializers.FloatField()
    two_pt_conv      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_off_fum_rec_td  = serializers.FloatField()
    off_fum_rec_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_sack  = serializers.FloatField()
    sack      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_ints  = serializers.FloatField()
    ints      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_fum_rec  = serializers.FloatField()
    fum_rec      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_sfty  = serializers.FloatField()
    sfty      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_blk_kick  = serializers.FloatField()
    blk_kick      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    #
    # dst stats below
    avg_ret_kick_td  = serializers.FloatField()
    ret_kick_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_ret_punt_td  = serializers.FloatField()
    ret_punt_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_ret_int_td  = serializers.FloatField()
    ret_int_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_ret_fum_td  = serializers.FloatField()
    ret_fum_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_ret_blk_punt_td  = serializers.FloatField()
    ret_blk_punt_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_ret_fg_td  = serializers.FloatField()
    ret_fg_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
    )

    avg_ret_blk_fg_td  = serializers.FloatField()
    ret_blk_fg_td      = serializers.ListField(
        child=serializers.FloatField(), help_text="This is an ARRAY of FLOATS"
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