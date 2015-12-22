#
# sports/views.py

from django.db import connection
from rest_framework.response import Response
from django.shortcuts import render
from django.views.generic import TemplateView, View
from sports.forms import PlayerCsvForm
import sports.classes
from sports.serializers import FantasyPointsSerializer
from sports.nba.serializers import InjurySerializer
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
        sport = self.kwargs['sport']
        site_sport_manager = sports.classes.SiteSportManager()
        team_serializer_class = site_sport_manager.get_team_serializer_class( sport )
        return team_serializer_class

    def get_queryset(self):
        """
        Return a QuerySet of the sports.<sport>.models.Team objects
        """
        sport = self.kwargs['sport']
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
        sport = self.kwargs['sport']
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
        sport = self.kwargs['sport']
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
        return injury_model_class.objects.all()


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
        sport = self.kwargs['sport']
        site_sport_manager = sports.classes.SiteSportManager()
        return site_sport_manager.get_fantasypoints_serializer_class( sport )

    def get_queryset(self):
        """
        from django.db import connections
        cursor = connections['my_db_alias'].cursor()
        """
        sport = self.kwargs['sport']
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
                c.execute("select player_id, array_agg(fantasy_points) from (select * from (select *, row_number() over (partition by player_id order by created) as rn from %s) as %s where rn <=10) as agg group by player_id" % (database_table_name, database_table_name))
                player_stats += self.dictfetchall( c )

        return player_stats
