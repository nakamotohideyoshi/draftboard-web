#
# sports/views.py

from django.shortcuts import render
from django.views.generic import TemplateView, View
from sports.forms import PlayerCsvForm
import sports.classes
from sports.nba.serializers import InjurySerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import json
from dataden.cache.caches import PlayByPlayCache
from django.http import HttpResponse

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
