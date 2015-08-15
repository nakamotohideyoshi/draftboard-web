#
# lineup/serializers.py

from rest_framework import serializers
from lineup.models import Lineup, Player

class LineupSerializer(serializers.ModelSerializer):

    class Meta:

        model   = Lineup
        fields  = ('user', 'fantasy_points', 'draftgroup')

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Player
        fields = ('player_id', 'full_name', 'lineup', 'roster_spot', 'idx')