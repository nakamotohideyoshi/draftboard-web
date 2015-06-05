#
# prize/views.py

from django.views.generic import TemplateView
from prize.classes import Generator

class CreatePrizeStructureView(TemplateView):
    """
    Usage:

        http://localhost:8888/prize/create-prize-structure/?b=10&fp=1700&rp=10&ps=120&pp=10000
        
    """
    template_name = 'create_prize_structure.html'

    #
    # this will be set after the GET
    prize_generator = None

    #
    # get front end arguments #TODO
    def get(self, request, *args, **kwargs):
        print( str(request.GET) )
        # >>> <QueryDict: {'b': ['10'], 'a': ['5']}>
        buyin           = int(request.GET.get('b'))
        first_place     = int(request.GET.get('fp'))
        round_payouts   = int(request.GET.get('rp'))
        payout_spots    = int(request.GET.get('ps'))
        prize_pool      = int(request.GET.get('pp'))

        self.prize_generator = Generator(buyin, first_place,
                                         round_payouts, payout_spots, prize_pool)
        return super().get(request, *args, **kwargs)

    #
    # get the data which we wish to pass to the html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ex url GET params: ?b=10&fp=1500&rp=10&ps=120&pp=10000
        # Generator(b, fp, rp, ps, pp)
        #gen = Generator(10, 1500, 10, 120, 10000)

        context['values'] = [1,2,3,4,5,6]

        prize_list = self.prize_generator.get_prize_list()

        prizes = [ x[1] for x in prize_list ]


        context['prizes'] = prizes
        context['ranks']  = list( range(1, len(prizes)) )
        context['ranges'] = self.prize_generator.get_range_list() # list( odata.items() )

        return context