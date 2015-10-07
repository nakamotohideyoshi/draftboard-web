#
# sports.nba.serializers.py

#from rest_framework import serializers
from sports.serializers import InjurySerializer
from .models import Injury

class InjurySerializer(InjurySerializer):

    class Meta:

        model = Injury
        fields = ('iid', 'status','description','srid', 'comment', 'player_id')
