#
# sports.nba.serializers.py

from rest_framework import serializers
from sports.serializers import InjurySerializer, FantasyPointsSerializer
import sports.serializers
from .models import Injury, PlayerStats, Team

class InjurySerializer(InjurySerializer):

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
        # fields = (
        #     # you shouldnt change id, srid, name, alias
        #     'id', 'srid', 'name', 'alias',
        #
        #     # sport market/city just called city in this serializer
        #     'city'
        # )

class FantasyPointsSerializer(FantasyPointsSerializer):

    # class Meta:
    #     model   = PlayerStats
    #     fields  = ('created','player_id','fantasy_points')

    player_id = serializers.IntegerField()

    fantasy_points = serializers.ListField(
        source='array_agg',
        child=serializers.FloatField() # min_value=-9999, max_value=9999)
    )