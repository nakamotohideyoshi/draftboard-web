#
# sports.nba.serializers.py

from sports.serializers import InjurySerializer, FantasyPointsSerializer
from .models import Injury, PlayerStats

class InjurySerializer(InjurySerializer):

    class Meta:

        model = Injury
        fields = ('iid', 'status','description','srid', 'comment', 'player_id')

class FantasyPointsSerializer(FantasyPointsSerializer):

    class Meta:
        model   = PlayerStats
        fields  = ('created','player_id','fantasy_points')