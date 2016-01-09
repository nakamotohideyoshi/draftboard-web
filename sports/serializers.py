#
# sports/serializers.py

from .models import Player, PlayerStats, PbpDescription, GameBoxscore, Injury
from rest_framework import serializers

# class PlayerSerializer(serializers.ModelSerializer):
#
#     class Meta:
#
#         model = Player
#         fields = ('first_name','last_name')

class GameSerializer(serializers.ModelSerializer):
    """
    parent Game object serializer with common fields
    """
    PARENT_FIELDS = ('srid','start')

class BoxscoreSerializer(serializers.ModelSerializer):
    """
    parent GameBoxscore object serializer with common fields
    """
    PARENT_FIELDS = ('srid_home','srid_away',
                     'status',
                     'attendance','coverage',
                     'home_scoring_json','away_scoring_json')

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

class InjurySerializer(serializers.ModelSerializer): pass       # extended by specific sport

class FantasyPointsSerializer(serializers.Serializer): pass     # extended by specific sport

class TeamSerializer(serializers.ModelSerializer):
    """
    parent TeamSerializer fields that are in every sports.models.Team object
    """
    PARENT_FIELDS = ('id','srid','name','alias')

class PlayerSerializer(serializers.ModelSerializer):
    """
    This is our way of abstracting a model serializer, basically by just setting fields
    we know are in every sports.models.Player...

    child classes can inherit this class in their specific sport.
    ie: sports.nba.serializers.Player, sports.nhl.serializers.Player, etc...
    """
    PARENT_FIELDS = ('id','srid','first_name','last_name')