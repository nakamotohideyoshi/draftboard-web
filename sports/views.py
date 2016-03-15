#
# sports/views.py

from django.db import connection
from rest_framework.response import Response
from django.shortcuts import render
from django.views.generic import TemplateView, View
from sports.forms import PlayerCsvForm
import sports.classes
from sports.serializers import FantasyPointsSerializer
from sports.nba.serializers import (
    InjurySerializer,
    PlayerNewsSerializer,
)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import json
from dataden.cache.caches import PlayByPlayCache
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType

class LeagueTeamAPIView(generics.ListAPIView):
    """
    Get the teams for the league teams for a sport.
    """

    #serializer class will be dynamic

    def get_serializer_class(self):
        """
        use site sport manager to get the site_sport from the sport param
        """
        try:
            sport = self.kwargs['sport']
        except KeyError:
            sport = "nba"
        site_sport_manager = sports.classes.SiteSportManager()
        team_serializer_class = site_sport_manager.get_team_serializer_class( sport )
        return team_serializer_class

    def get_queryset(self):
        """
        Return a QuerySet of the sports.<sport>.models.Team objects
        """
        try:
            sport = self.kwargs['sport']
        except KeyError:
            sport = "nba"
        site_sport_manager = sports.classes.SiteSportManager()
        team_model_class = site_sport_manager.get_team_class( sport )
        return team_model_class.objects.all()

class LeaguePlayerAPIView(generics.ListAPIView):
    """
    Get the players in the league, with more detailed information
    """

    #serializer class will be dynamic

    def get_serializer_class(self):
        """
        use site sport manager to get the site_sport from the sport param
        """
        try:
            sport = self.kwargs['sport']
        except KeyError:
            sport = "nba"
        site_sport_manager = sports.classes.SiteSportManager()
        return site_sport_manager.get_player_serializer_class(sport)

    def get_queryset(self):
        """
        Return a QuerySet of the sports.<sport>.models.Team objects
        """
        sport = self.kwargs['sport']
        site_sport_manager = sports.classes.SiteSportManager()
        site_sport = site_sport_manager.get_site_sport(sport)
        player_model_class = site_sport_manager.get_player_class( site_sport )
        return player_model_class.objects.all()

class LeagueInjuryAPIView(generics.ListAPIView):
    """
    Retrieve the contests which are relevant to the home page lobby.
    """

    permission_classes      = (IsAuthenticated,)

    #serializer_class        = None #InjurySerializer
    def get_serializer_class(self):
        """
        override for having to set the self.serializer_class
        """
        try:
            sport = self.kwargs['sport']
        except KeyError:
            sport = "nba"
        site_sport_manager = sports.classes.SiteSportManager()
        injury_serializer_class = site_sport_manager.get_injury_serializer_class( sport )
        return injury_serializer_class

    def get_queryset(self):
        """
        Return a QuerySet from the LobbyContest model.
        """
        sport = self.kwargs['sport']
        site_sport_manager = sports.classes.SiteSportManager()
        injury_model_class = site_sport_manager.get_injury_class( sport )
        # fetch the highest ddtimestamp, and then return all the
        # objects with that timestamp
        most_recent_injuries = injury_model_class.objects.filter().order_by('-ddtimestamp')[:1]
        if most_recent_injuries.count() == 0:
            return []

        last_updated_ts = most_recent_injuries[0].ddtimestamp
        #return injury_model_class.objects.all() # we dont want to return multiple injuries for same player
        return injury_model_class.objects.filter(ddtimestamp=last_updated_ts) # only return the most recent for each player

class PlayerCsvView(View):
    template_name   = 'player_csv.html'
    form_class      = PlayerCsvForm

    initial         = {
        # 'buyin'             : 10,
        # 'first_place'       : 1000,
        # 'round_payouts'     : 20,
        # 'payout_spots'      : 50,
        # 'prize_pool'        : 12000,
        #
        # 'create'            : False
    }

    player_csv_obj = None

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            site_sport      = form.cleaned_data['site_sport']

            print(site_sport, 'site_sport')
            if site_sport.name == 'mlb':
                self.player_csv_obj = sports.classes.MlbPlayerNamesCsv()
            elif site_sport.name == 'nfl':
                self.player_csv_obj = sports.classes.NflPlayerNamesCsv()
            elif site_sport.name == 'nhl':
                self.player_csv_obj = sports.classes.NhlPlayerNamesCsv()
            elif site_sport.name == 'nba':
                self.player_csv_obj = sports.classes.NbaPlayerNamesCsv()
            else:
                print('invalid site_sport:', str(site_sport))
                raise Exception('site_sport was invalid')

            rows = self.player_csv_obj.get_rows()

            context = {
                'form'      : form,
                'rows'      : rows
            }

            return render(request, self.template_name, context)

        #
        #
        context = {'form'  : form}
        return render(request, self.template_name, context)


class LivePbpView(View):
    """
    uses dataden.cache.caches.PlayByPlayCache to access the most recent pbp objects (~100 per sport)
    """

    def get(self, request, sport):
        pbp_cache = PlayByPlayCache( sport )

        return HttpResponse( json.dumps(pbp_cache.get_pbps()), content_type='application/json' )


class FantasyPointsHistoryAPIView(generics.ListAPIView):
    """
    Get all Player's trailing history of Fantasy Points
    """
    permission_classes      = (IsAuthenticated,)

    def dictfetchall(self, cursor):
        """Return all rows from a cursor as a dict"""
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def get_serializer_class(self):
        """
        override for having to set the self.serializer_class
        """
        try:
            sport = self.kwargs['sport']
        except KeyError:
            sport = "nba"
        site_sport_manager = sports.classes.SiteSportManager()
        return site_sport_manager.get_fantasypoints_serializer_class( sport )

    def get_queryset(self):
        """
        from django.db import connections
        cursor = connections['my_db_alias'].cursor()
        """
        try:
            sport = self.kwargs['sport']
        except KeyError:
            sport = "nba"
        site_sport_manager = sports.classes.SiteSportManager()
        site_sport = site_sport_manager.get_site_sport( sport )
        player_stats_class_list = site_sport_manager.get_player_stats_class( site_sport )
        player_stats = []
        for player_stats_class in player_stats_class_list:
            ct = ContentType.objects.get_for_model( player_stats_class )
            database_table_name = ct.app_label + '_' + ct.model    # ie: 'nba_playerstats'
            # player_stats_list = player_stats_class.objects.raw(
            #     #
            #     # example:
            #     # "select * from (select *, row_number() over (partition by player_id order by created) as rn from %s) as %s where rn <=10;"
            #     "select * from (select *, row_number() over (partition by player_id order by created) as rn from %s) as %s where rn <=10;" % (database_table_name, database_table_name)
            # )

            with connection.cursor() as c:
                #q_str = "select player_id, array_agg(fantasy_points) from (select * from (select *, row_number() over (partition by player_id order by created DESC) as rn from nba_playerstats) as nba_playerstats where rn <=10) as agg group by player_id"
                q_str = "select player_id, array_agg(fantasy_points) from (select * from (select *, row_number() over (partition by player_id order by created DESC) as rn from %s) as %s where rn <=10) as agg group by player_id" % (database_table_name, database_table_name)
                #print(q_str)
                c.execute(q_str)
                player_stats += self.dictfetchall( c )

        return player_stats

class PlayerHistoryAPIView(generics.ListAPIView):
    """
    averages for the primary scoring categories


    """
    permission_classes      = (IsAuthenticated,)
    sport = None
    def dictfetchall(self, cursor):
        """Return all rows from a cursor as a dict"""
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def get_serializer_class(self):
        """
        override for having to set the self.serializer_class
        """
        try:
            sport = self.kwargs['sport']
        except KeyError:
            sport = "nba"
        site_sport_manager = sports.classes.SiteSportManager()
        class_sport = site_sport_manager.get_playerhistory_serializer_class( sport )
        return class_sport

    def get_queryset(self):
        """
        from django.db import connections
        cursor = connections['my_db_alias'].cursor()
        """
        sport = self.kwargs['sport']

        n_games_history = self.kwargs['n_games_history']
        #print( str(n_games_history), 'games for', sport )
        site_sport_manager = sports.classes.SiteSportManager()
        site_sport = site_sport_manager.get_site_sport( sport )
        player_stats_class_list = site_sport_manager.get_player_stats_class( site_sport )
        game_class = site_sport_manager.get_game_class( site_sport )
        player_stats = []
        for player_stats_class in player_stats_class_list:
            ct = ContentType.objects.get_for_model( player_stats_class )
            playerstats_table_name = ct.app_label + '_' + ct.model              # ie: 'nba_playerstats'

            game_ctype = ContentType.objects.get_for_model( game_class )
            game_table_name = game_ctype.app_label + '_' + game_ctype.model     # ie: 'nba_game'

            # these are the fields we want to aggregate and average for the serializer.
            # we use a raw query for efficiency purposes.

            # excluding player_id, srid_game, fantasy_points (these existed before re-write)
            # add the fields to game_fields to array_agg(),
            # add the fields to scoring_fields to array_agg() AND to avg()
            game_fields     = ['start','home_id','away_id','srid_home','srid_away']
            scoring_fields  = player_stats_class.SCORING_FIELDS
            scoring_fields_dont_avg = player_stats_class.SCORING_FIELDS_DONT_AVG

            #
            # build the statement:
            # select player_id,
            #   array_agg(srid_game) as games,
            #   array_agg(home_id) as home_ids,
            #   array_agg(away_id) as away_ids,
            #   array_agg(start) as starts,
            #   array_agg(fantasy_points) as fp,
            #   avg(fantasy_points) as avg_fp,
            #   array_agg(points) as points,
            #   avg(points) as avg_points,
            #   array_agg(three_points_made) as three_points_made,
            #   avg(three_points_made) as avg_three_points_made,
            #   array_agg(rebounds) as rebounds,
            #   avg(rebounds) as avg_rebounds,
            #   array_agg(assists) as assists,
            #   avg(assists) as avg_assists,
            #   array_agg(steals) as steals,
            #   avg(steals) as avg_steals,
            #   array_agg(blocks) as blocks,
            #   avg(blocks) as avg_blocks,
            #   array_agg(turnovers) as turnovers,
            #   avg(turnovers) as avg_turnovers
            #  from

            # outter select
            select_str = 'select player_id, array_agg(srid_game) as games, array_agg(fantasy_points) as fp, avg(fantasy_points) as avg_fp'
            for field in game_fields:
                select_str += ', array_agg({0}) as {0}'.format(field)
            for field in scoring_fields:
                select_str += ', array_agg({0}) as {0}, avg({0}) as avg_{0}'.format(field)
            for field in scoring_fields_dont_avg:
                select_str += ', array_agg({0}) as {0}'.format(field)
            # inner select
            # (select all_player_stats.*, nba_game.home_id, nba_game.away_id, nba_game.start from (select * from (select *, row_number() over (partition by player_id order by created) as rn from nba_playerstats) as nba_playerstats where rn <=5) as all_player_stats join nba_game on nba_game.srid = all_player_stats.srid_game) as player_stats group by player_id
            final_select_str = "{0} from (select all_player_stats.*, {1}.home_id, {1}.away_id, {1}.srid_home, {1}.srid_away, {1}.start from (select * from (select *, row_number() over (partition by player_id order by created DESC) as rn from {2}) as {2} where rn <= {3}) as all_player_stats join {1} on {1}.srid = all_player_stats.srid_game) as player_stats group by player_id".format(select_str, game_table_name, playerstats_table_name, str(n_games_history))

            # the final query string
            #query_str = "{4} (select {0} from (select * from (select *, row_number() over (partition by player_id order by created) as rn from {1}) as {1} where rn <={2}) as agg group by player_id) as player_stats on {3}.srid = ANY(player_stats.games)".format(select_columns_str, database_table_name, str(n_games_history), game_table_name, outter_select_str)
            # query_str = """select player_id, array_agg(points) as points, avg(points) as avg_points, array_agg(three_points_made) as three_points_made, avg(three_points_made) as avg_three_points_made from (select * from (select *, row_number() over (partition by player_id order by created) as rn from nba_playerstats) as nba_playerstats where rn <=10) as agg group by player_id"""

            print('')
            print('final_select_str')
            print(final_select_str)
            print('')
            print('')

            with connection.cursor() as c:
                c.execute(final_select_str)
                player_stats += self.dictfetchall( c )

        return player_stats

class TsxPlayerNewsAPIView(generics.ListAPIView):
    """
    gets the news for the sport
    """

    permission_classes      = (IsAuthenticated,)

    def get_serializer_class(self):
        """
        override for having to set the self.serializer_class
        """
        try:
            sport = self.kwargs['sport']
        except KeyError:
            sport = "nba"
        site_sport_manager = sports.classes.SiteSportManager()
        injury_serializer_class = site_sport_manager.get_tsxplayer_serializer_class( sport )
        return injury_serializer_class

    def get_queryset(self):
        """
        Return a QuerySet from the LobbyContest model.
        """
        sport = self.kwargs['sport']
        site_sport_manager = sports.classes.SiteSportManager()
        tsxplayer_model_class = site_sport_manager.get_tsxplayer_class(sport)

        # TODO return them all for now as a test
        return tsxplayer_model_class.objects.all()

class TsxPlayerItemsAPIView(generics.ListAPIView):
    """
    gets the news for the sport
    """

    permission_classes      = (IsAuthenticated,)

    def get_serializer_class(self):
        """
        override for having to set the self.serializer_class
        """
        try:
            sport = self.kwargs['sport']
        except KeyError:
            sport = "nba"
        site_sport_manager = sports.classes.SiteSportManager()
        injury_serializer_class = site_sport_manager.get_tsxplayer_serializer_class( sport )
        return injury_serializer_class

    def get_queryset(self):
        """
        Return a QuerySet from the LobbyContest model.
        """
        sport = self.kwargs['sport']
        site_sport_manager = sports.classes.SiteSportManager()
        tsxplayer_model_class = site_sport_manager.get_tsxplayer_class(sport)

        # TODO return them all for now as a test
        return tsxplayer_model_class.objects.all()

class PlayerNewsAPIView(generics.ListAPIView):
    """
    gets the news for the sport
    """

    permission_classes      = (IsAuthenticated,)

    def __get_sport(self):
        return self.kwargs['sport']

    def get_serializer_class(self):
        """
        override for having to set the self.serializer_class
        """
        #return PlayerNewsSerializer
        site_sport_manager = sports.classes.SiteSportManager()
        site_sport = site_sport_manager.get_site_sport(self.__get_sport())
        return site_sport_manager.get_playernews_serializer_class( site_sport )

    def get_queryset(self):
        """
        Return a QuerySet from the LobbyContest model.
        """
        player_id = self.kwargs.get('player')
        site_sport_manager = sports.classes.SiteSportManager()
        site_sport = site_sport_manager.get_site_sport(self.__get_sport())
        sport_player_class = site_sport_manager.get_player_class( site_sport )
        if player_id is None:
            # get all of them
            return sport_player_class.objects.all()
        else:
            # # return 1 of them
            # player_model = sport_player_class.objects.get(pk=player_id)
            # player_ctype = ContentType.objects.get_for_model(player_model)
            return sport_player_class.objects.filter(pk=player_id)

# class DraftGroupGameBoxscoresView(View):
class ScheduleGameBoxscoresView(View):
    """
    return all the boxscores for the given draft group (basically, all
    the live games (ie: Home @ Away with scores) from the context
    of the draftgroup)

    for /api/sports/nba/scoreboard-games/
    """

    # def __add_to_dict(self, target, extras):
    #     for k,v in extras.items():
    #         target[ k ] = v
    #     return target

    def get(self, request, sport):

        # return HttpResponse( {}, content_type='application/json', status=status.HTTP_404_NOT_FOUND)

        ssm     = sports.classes.SiteSportManager()
        data    = ssm.get_serialized_scoreboard_data(sport)
        #
        # # notes:
        # # boxscores   = dgm.get_game_boxscores( draft_group )
        # # get_game_serializer_class(sport)
        # # get_boxscore_serializer_class(sport)
        #
        # # data = []
        # # for b in boxscores:
        # #     data.append( b.to_json() )
        # data = {}
        # for game in games:
        #     # initial inner_data
        #     inner_data = {}
        #
        #     # add the game data
        #     g = game_serializer_class( game ).data
        #     self.__add_to_dict( inner_data, g )
        #
        #     # add the boxscore data
        #     boxscore = None
        #     try:
        #         boxscore = boxscores.get(srid_game=game.srid) # may not exist
        #     except:
        #         pass
        #     b = {}
        #     if boxscore is not None:
        #         b = {
        #             'boxscore' : boxscore_serializer_class( boxscore ).data
        #         }
        #     self.__add_to_dict( inner_data, b )
        #
        #     # finish it by adding the game data to the return data dict
        #     data[ game.srid ] = inner_data

        return HttpResponse( json.dumps(data), content_type='application/json' )
