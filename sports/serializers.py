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
    PARENT_FIELDS = ('srid_game',
                     'srid_home','srid_away',
                     'home_score','away_score',
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

class InjurySerializer(serializers.ModelSerializer):
    """
    extended by the specific sport
    """
    PARENT_FIELDS = ('iid','player_id','status','description','created')

class FantasyPointsSerializer(serializers.Serializer):
    """
    extended by the specific sport
    """
    pass

class PlayerHistorySerializer(serializers.Serializer):
    """
    extended by the specific sport
    """
    # we will get an array of games
    games = serializers.ListField(
        #source='fp',
        child=serializers.CharField()
    )

    #
    # the Fantasy Points have to get a different name in this
    # serializer because there is already a column called fantasy_points which
    # on the PlayerStats models
    avg_fp = serializers.FloatField()
    fp = serializers.ListField(
        #source='fp',
        child=serializers.FloatField()
    )

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

class TsxItemSerializer(serializers.ModelSerializer):

    PARENT_FIELDS = ('srid','pcid','content_published','title',
                     'byline','dateline','credit','content')

class TsxNewsSerializer(serializers.ModelSerializer):

    PARENT_FIELDS = ('title','dateline')

class TsxPlayerSerializer(serializers.ModelSerializer):

    PARENT_FIELDS = ('name','sportsdataid','sportradarid')

class PlayerNewsSerializer(serializers.ModelSerializer):

    PARENT_FIELDS = ('id','news')

    # maximum trailing news items to return
    limit_news_items = 5

    # child classes must override these to the sport's
    # own TsxPlayer model
    tsxplayer_class         = None
    tsxplayer_serializer    = None

    news = serializers.SerializerMethodField()
    def get_news(self, player):
        # dt_from = timezone.now() - timedelta(days=30) # start from 30 days ago
        # query_set = TsxPlayer.objects.filter(player=player,
        #                 content_published__gte=dt_from).select_related('player')

        query_set = self.tsxplayer_class.objects.filter(player=player) \
                            .select_related('player')[:self.limit_news_items]
        return self.tsxplayer_serializer( query_set, many=True ).data