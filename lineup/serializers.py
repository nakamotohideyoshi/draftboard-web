#
# lineup/serializers.py

from rest_framework import serializers
from lineup.models import Lineup, Player

class LineupSerializer(serializers.ModelSerializer):

    class Meta:

        model   = Lineup
        fields  = ('id','user', 'fantasy_points', 'draft_group')

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Player
        fields = ('player_id', 'full_name', 'lineup', 'roster_spot', 'idx')

