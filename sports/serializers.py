from ast import literal_eval

from rest_framework import serializers

from .models import PlayerStats, PbpDescription, GameBoxscore


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
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()

    def get_home_team(self, game):
        return self.get_team_name_from_srid(game.srid_home)

    def get_away_team(self, game):
        return self.get_team_name_from_srid(game.srid_away)

    @staticmethod
    def get_team_name_from_srid(srid):
        from sports.classes import TeamNameCache
        tnc = TeamNameCache()
        return tnc.get_team_from_srid(srid).get('alias', 'not found')

    PARENT_FIELDS = ('srid', 'start', 'status', 'boxscore', 'home_team', 'away_team')


class BoxscoreSerializer(serializers.ModelSerializer):
    """
    parent GameBoxscore object serializer with common fields
    """

    # def to_representation(self, boxscore):
    #     return {
    #         boxscore.srid_game : {
    #             'srid_game' : boxscore.srid_game,
    #             'srid_home' : boxscore.srid_home,
    #             'srid_away' : boxscore.srid_away,
    #             'status'    : boxscore.status,
    #             'attendance': boxscore.attendance,
    #             ''
    #         }
    #     }

    def __get_dict(self, json_str):
        if json_str is None or json_str == '':
            return None
        else:
            return literal_eval(json_str)

    home_scoring_data = serializers.SerializerMethodField()
    away_scoring_data = serializers.SerializerMethodField()
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()

    def get_home_scoring_data(self, boxscore):
        return self.__get_dict(boxscore.home_scoring_json)

    def get_away_scoring_data(self, boxscore):
        return self.__get_dict(boxscore.away_scoring_json)

    def get_home_team(self, game):
        return self.get_team_name_from_srid(game.srid_home)

    def get_away_team(self, game):
        return self.get_team_name_from_srid(game.srid_away)

    @staticmethod
    def get_team_name_from_srid(srid):
        from sports.classes import TeamNameCache
        tnc = TeamNameCache()
        return tnc.get_team_from_srid(srid).get('alias', 'not found')

    PARENT_FIELDS = ('srid_game',
                     'home_team', 'away_team',
                     'srid_home', 'srid_away',
                     'home_score', 'away_score',
                     # 'status', # remove because we want to start using only the Game.status!
                     'attendance', 'coverage',
                     'home_scoring_data', 'away_scoring_data')


class GameBoxscoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameBoxscore
        fields = ('home_id', 'away_id', 'title',
                  'home_score', 'away_score',
                  'home_scoring_json', 'away_scoring_json',
                  'attendance')


class PbpDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PbpDescription
        fields = ('created', 'pbp_id', 'idx', 'description')


class PlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStats
        fields = ('game_id', 'player_id', 'fantasy_points', 'updated')


class InjurySerializer(serializers.ModelSerializer):
    """
    extended by the specific sport
    """
    PARENT_FIELDS = ('iid', 'player_id', 'status', 'description', 'created')


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
        # source='fp',
        child=serializers.CharField(),
        help_text="This is an ARRAY of STRING game srid(s)"
    )

    #
    # home_id, away_id, start, srid_home, srid_away
    home_id = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="This is an ARRAY of INTEGER primary keys to home teams referenced by the srid in games at the same index"
    )
    away_id = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="This is an ARRAY of INTEGER primary keys to away teams referenced by the srid in games at the same index"
    )
    start = serializers.ListField(
        child=serializers.DateTimeField(),
        help_text="This is an ARRAY of DATETIMES to the start of each game referenced by the srid in games at the same index"
    )
    srid_home = serializers.ListField(
        child=serializers.CharField(),
        help_text="This is an ARRAY of STRINGS of sportradar ids (srids) for each home team for the game at the same index"
    )
    srid_away = serializers.ListField(
        child=serializers.CharField(),
        help_text="This is an ARRAY of STRINGS of sportradar ids (srids) for each away team for the game at the same index"
    )
    #
    # the Fantasy Points have to get a different name in this
    # serializer because there is already a column called fantasy_points which
    # on the PlayerStats models
    avg_fp = serializers.FloatField()
    fp = serializers.ListField(
        # source='fp',
        child=serializers.FloatField(),
        help_text="This is an ARRAY of FLOAT fantasy points  of each game referenced by the srid in games at the same index"
    )


class TeamSerializer(serializers.ModelSerializer):
    """
    parent TeamSerializer fields that are in every sports.models.Team object
    """
    PARENT_FIELDS = ('id', 'srid', 'name', 'alias')


class PlayerSerializer(serializers.ModelSerializer):
    """
    This is our way of abstracting a model serializer, basically by just setting fields
    we know are in every sports.models.Player...

    child classes can inherit this class in their specific sport.
    ie: sports.nba.serializers.Player, sports.nhl.serializers.Player, etc...
    """
    PARENT_FIELDS = ('id', 'srid', 'first_name', 'last_name')


class TsxItemSerializer(serializers.ModelSerializer):
    PARENT_FIELDS = ('srid', 'pcid', 'content_published', 'title',
                     'byline', 'dateline', 'credit', 'content')


class TsxNewsSerializer(serializers.ModelSerializer):
    PARENT_FIELDS = ('title', 'dateline')


class TsxPlayerSerializer(serializers.ModelSerializer):
    PARENT_FIELDS = ('name', 'sportsdataid', 'sportradarid')


class PlayerNewsSerializer(serializers.ModelSerializer):
    PARENT_FIELDS = ('id', 'news')

    # maximum trailing news items to return
    limit_news_items = 5

    # child classes must override these to the sport's
    # own TsxPlayer model
    tsxplayer_class = None
    tsxplayer_serializer = None

    news = serializers.SerializerMethodField()

    def get_news(self, player):
        # dt_from = timezone.now() - timedelta(days=30) # start from 30 days ago
        # query_set = TsxPlayer.objects.filter(player=player,
        #                 content_published__gte=dt_from).select_related('player')

        query_set = self.tsxplayer_class.objects.filter(player=player) \
                        .select_related('player')[:self.limit_news_items]
        return self.tsxplayer_serializer(query_set, many=True).data
