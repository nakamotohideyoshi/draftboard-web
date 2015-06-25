#
# sports/views.py

from django.shortcuts import render
from django.views.generic import TemplateView, View
from sports.forms import PlayerCsvForm
import sports.classes
import json

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
