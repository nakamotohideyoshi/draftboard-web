#
# sports/

from django.shortcuts import render
from django.views.generic import TemplateView
from prize.classes import Generator, CashPrizeStructureCreator, \
                            TicketPrizeStructureCreator, FlatCashPrizeStructureCreator
from prize.forms import PrizeGeneratorForm, TicketPrizeCreatorForm, FlatCashPrizeCreatorForm
from django.http import HttpResponseRedirect

import json

class PieDataObj(object):
    #
    # example:
    # {
    #     'value': 300,
    #     'color':"#F7464A",
    #     'highlight': "#FF5A5E",
    #     'label': "Red"
    # },

    def __init__(self, value, color, highlight, label):
        self.data = {
            'value':        int(value),
            'color':        color,
            'highlight':    highlight,
            'label':        label
        }

    def get_data(self):
        return self.data

class PrizeGeneratorView(View):
    template_name   = 'prize_generator.html'
    form_class      = PrizeGeneratorForm

    initial         = {
        'buyin'             : 10,
        'first_place'       : 1000,
        'round_payouts'     : 20,
        'payout_spots'      : 50,
        'prize_pool'        : 12000,

        'create'            : False
    }

    prize_generator = None

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            buyin           = form.cleaned_data['buyin']
            first_place     = form.cleaned_data['first_place']
            round_payouts   = form.cleaned_data['round_payouts']
            payout_spots    = form.cleaned_data['payout_spots']
            prize_pool      = form.cleaned_data['prize_pool']
            create          = form.cleaned_data['create'] # check if this exists ?

            print(buyin, first_place, round_payouts, payout_spots, prize_pool, create)
            self.prize_generator = Generator(buyin, first_place, round_payouts,
                                                     payout_spots, prize_pool )

            context = {
                'form'      : form
            }

            ##########
            ##########
            prize_list = self.prize_generator.get_prize_list()
            range_list = self.prize_generator.get_range_list()

            prizes          = [ x[1] for x in prize_list ]
            distinct_prizes = [ x[0] for x in range_list ]
            distinct_prize_players = [ len(x[1]) for x in range_list ]
            min_rank_for_prize = [ x[1][len(x[1]) - 1] for x in range_list ]

            context['prizes'] = prizes
            context['ranks']  = list( range(1, len(prizes)) )
            context['ranges'] = self.prize_generator.get_range_list() # list( odata.items() )
            context['distinctprizes']       = distinct_prizes
            context['distinctprizeplayers'] = distinct_prize_players
            context['min_rank_for_prize']   = min_rank_for_prize

            # some values we might want
            context['maxentries'] = self.prize_generator.get_max_entries()
            paid = len(prize_list)
            context['paid'] = paid
            not_paid = int(self.prize_generator.get_max_entries() - len(prize_list))
            context['notpaid'] = not_paid

            # generate the data for 1st pie wheel
            payoutsdata_list = []
            payoutsdata_list.append( PieDataObj(paid,"#46BFBD","#5AD3D1",'Paid' ).get_data() )
            payoutsdata_list.append( PieDataObj(not_paid,"#F7464A","#FF5A5E",'Not Paid' ).get_data() )
            context['payoutsdata'] = json.dumps( payoutsdata_list )

            # top 10 prizes versus the rest of the prizes
            sum_top_10 = 0
            sum_11_plus = 0
            for i,p in enumerate( prizes ):
                if i < 10:
                    sum_top_10 += p
                else:
                    sum_11_plus += p

            piedata_list = []
            piedata_list.append( PieDataObj(sum_top_10,"#46BFBD","#5AD3D1","Top 10").get_data() )
            piedata_list.append( PieDataObj(sum_11_plus,"#FDB45C","#FFC870","All Other").get_data() )
            context['piedata'] = json.dumps( piedata_list )

            # context['piedata'] = json.dumps( [
            #     {
            #         'value': 300,
            #         'color':"#F7464A",
            #         'highlight': "#FF5A5E",
            #         'label': "Red"
            #     },
            #     {
            #         'value': 50,
            #         'color': "#46BFBD",
            #         'highlight': "#5AD3D1",
            #         'label': "Green"
            #     },
            #     {
            #         'value': 100,
            #         'color': "#FDB45C",
            #         'highlight': "#FFC870",
            #         'label': "Yellow"
            #     }
            # ] )

            # top 3 prizes (if there are that many
            topprizes_list = []
            topprizes_list.append( PieDataObj(prizes[0],"#46BFBD","#5AD3D1", '1st').get_data() )
            if len(prizes) >= 2:
                topprizes_list.append( PieDataObj(prizes[1],"#FDB45C","#FFC870",'2nd').get_data() )
            if len(prizes) >= 3:
                topprizes_list.append( PieDataObj(prizes[2],"#F7464A","#FF5A5E",'3rd').get_data() )

            context['topprizes'] = json.dumps( topprizes_list )
            ##########
            ##########

            #
            # at this point, if 'create' is True, we should
            # actually save & commit a new prize structure
            if create:
                creator = CashPrizeStructureCreator( self.prize_generator, 'gui' )
                creator.save()

            context['created']   = create # we should ACTUALLY create it though.

            #return HttpResponseRedirect('/success/')
            return render(request, self.template_name, context)

        #
        #
        context = {'form'  : form}
        return render(request, self.template_name, context)
