#
# sports/serializers.py

from .models import Player, PlayerStats, PbpDescription, GameBoxscore, Injury
from rest_framework import serializers

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Player
        fields = ('first_name','last_name')

class GameBoxscoreSerializer(serializers.ModelSerializer):

    class Meta:

        model = GameBoxscore
        fields = ('home_id','away_id','title',
                  'home_score','away_score',
                  'home_scoring_json','away_scoring_json',
                  'attendance')

class PbpDescriptionSerializer(serializers.ModelSerializer):

    class Meta:

        model = PbpDescription
        fields = ('created','pbp_id', 'idx', 'description')

class PlayerStatsSerializer(serializers.ModelSerializer):

    class Meta:

        model = PlayerStats
        fields = ('game_id', 'player_id','fantasy_points')

class InjurySerializer(serializers.ModelSerializer): pass

    #class Meta:

        #model = Injury
        #fields = ('iid', 'status','description')