#
# sports.nfl.serializers.py

from rest_framework import serializers
import sports.serializers
from .models import Game, GameBoxscore, Injury, Team, Player

class BoxscoreSerializer(sports.serializers.BoxscoreSerializer):

    class Meta:

        model = GameBoxscore

        fields = sports.serializers.BoxscoreSerializer.PARENT_FIELDS + \
                 ('clock','completed','quarter')


class GameSerializer(sports.serializers.GameSerializer):

    class Meta:

        model = Game

        fields = sports.serializers.GameSerializer.PARENT_FIELDS + \
                 ('srid_home','srid_away','title', 'weather_json')

class InjurySerializer(sports.serializers.InjurySerializer):

    class Meta:

        model = Injury
        fields = ('iid', 'status','description','srid', 'practice_status', 'player_id')

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
    avg_pass_td  = serializers.FloatField()
    pass_td      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_pass_yds  = serializers.FloatField()
    pass_yds      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_pass_int  = serializers.FloatField()
    pass_int      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_rush_td  = serializers.FloatField()
    rush_td      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_rush_yds  = serializers.FloatField()
    rush_yds      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_rec_td  = serializers.FloatField()
    rec_td     = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_rec_yds  = serializers.FloatField()
    rec_yds      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_rec_rec  = serializers.FloatField()
    rec_rec      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_off_fum_lost  = serializers.FloatField()
    off_fum_lost      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_two_pt_conv  = serializers.FloatField()
    two_pt_conv      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_off_fum_rec_td  = serializers.FloatField()
    off_fum_rec_td      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_sack  = serializers.FloatField()
    sack      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_ints  = serializers.FloatField()
    ints      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_fum_rec  = serializers.FloatField()
    fum_rec      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_sfty  = serializers.FloatField()
    sfty      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_blk_kick  = serializers.FloatField()
    blk_kick      = serializers.ListField(
        child=serializers.FloatField()
    )

    #
    # dst stats below
    avg_ret_kick_td  = serializers.FloatField()
    ret_kick_td      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_ret_punt_td  = serializers.FloatField()
    ret_punt_td      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_ret_int_td  = serializers.FloatField()
    ret_int_td      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_ret_fum_td  = serializers.FloatField()
    ret_fum_td      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_ret_blk_punt_td  = serializers.FloatField()
    ret_blk_punt_td      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_ret_fg_td  = serializers.FloatField()
    ret_fg_td      = serializers.ListField(
        child=serializers.FloatField()
    )

    avg_ret_blk_fg_td  = serializers.FloatField()
    ret_blk_fg_td      = serializers.ListField(
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