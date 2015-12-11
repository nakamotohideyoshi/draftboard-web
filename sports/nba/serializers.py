#
# sports.nba.serializers.py

from rest_framework import serializers
from sports.serializers import InjurySerializer, FantasyPointsSerializer
from .models import Injury, PlayerStats, Team

class InjurySerializer(InjurySerializer):

    class Meta:

        model = Injury
        fields = ('iid', 'status','description','srid', 'comment', 'player_id')

class TeamSerializer(InjurySerializer):

    class Meta:

        model = Team
        fields = ('id', 'srid', 'name', 'alias')

class FantasyPointsSerializer(FantasyPointsSerializer):

    # class Meta:
    #     model   = PlayerStats
    #     fields  = ('created','player_id','fantasy_points')

    player_id = serializers.IntegerField()

    fantasy_points = serializers.ListField(
        source='array_agg',
        child=serializers.FloatField() # min_value=-9999, max_value=9999)
    )