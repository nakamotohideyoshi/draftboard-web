import json
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from rest_framework.response import Response
from django.views.generic import TemplateView, View
from rest_framework import generics
from prize.classes import (
    Generator,
    CashPrizeStructureCreator,
    FlatCashPrizeStructureCreator,
    FlatTicketPrizeStructureCreator,
)
from prize.forms import PrizeGeneratorForm, TicketPrizeCreatorForm, FlatCashPrizeCreatorForm
from prize.serializers import PrizeStructureSerializer
from prize.models import PrizeStructure
from rest_framework.exceptions import NotFound


class PrizeStructureAPIView(generics.GenericAPIView):
    serializer_class = PrizeStructureSerializer

    def get_object(self, id):
        try:
            return PrizeStructure.objects.get(pk=id)
        except PrizeStructure.DoesNotExist:
            raise NotFound()

    def get(self, request, id, format=None):
        """
        given the GET param 'id', get the draft_group
        """
        serialized_data = None
        # c = caches['default']
        # serialized_data = c.get(self.__class__.__name__ + str(pk), None)
        if serialized_data is None:
            serialized_data = PrizeStructureSerializer(self.get_object(id), many=False).data
        # c.add( self.__class__.__name__ + str(pk), serialized_data, 1 ) # 300 seconds
        return Response(serialized_data)


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
            'value': int(value),
            'color': color,
            'highlight': highlight,
            'label': label
        }

    def get_data(self):
        return self.data


class PrizeGeneratorView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'prize_generator.html'
    form_class = PrizeGeneratorForm
    permission_required = 'superuser'
    initial = {
        'buyin': 10,
        'first_place': 1000,
        'round_payouts': 20,
        'payout_spots': 50,
        'prize_pool': 12000,

        'create': False
    }

    prize_generator = None

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            buyin = form.cleaned_data['buyin']
            first_place = form.cleaned_data['first_place']
            round_payouts = form.cleaned_data['round_payouts']
            payout_spots = form.cleaned_data['payout_spots']
            prize_pool = form.cleaned_data['prize_pool']
            create = form.cleaned_data['create']  # check if this exists ?

            print(buyin, first_place, round_payouts, payout_spots, prize_pool, create)
            self.prize_generator = Generator(buyin, first_place, round_payouts,
                                             payout_spots, prize_pool)

            context = {
                'form': form
            }

            ##########
            ##########
            prize_list = self.prize_generator.get_prize_list()
            range_list = self.prize_generator.get_range_list()

            prizes = [x[1] for x in prize_list]
            distinct_prizes = [x[0] for x in range_list]
            distinct_prize_players = [len(x[1]) for x in range_list]
            min_rank_for_prize = [x[1][len(x[1]) - 1] for x in range_list]

            context['prizes'] = prizes
            context['ranks'] = list(range(1, len(prizes)))
            context['ranges'] = self.prize_generator.get_range_list()  # list( odata.items() )
            context['distinctprizes'] = distinct_prizes
            context['distinctprizeplayers'] = distinct_prize_players
            context['min_rank_for_prize'] = min_rank_for_prize

            # some values we might want
            context['maxentries'] = self.prize_generator.get_max_entries()
            paid = len(prize_list)
            context['paid'] = paid
            not_paid = int(self.prize_generator.get_max_entries() - len(prize_list))
            context['notpaid'] = not_paid

            # generate the data for 1st pie wheel
            payoutsdata_list = [
                PieDataObj(paid, "#46BFBD", "#5AD3D1", 'Paid').get_data(),
                PieDataObj(not_paid, "#F7464A", "#FF5A5E", 'Not Paid').get_data(),
            ]
            context['payoutsdata'] = json.dumps(payoutsdata_list)

            # top 10 prizes versus the rest of the prizes
            sum_top_10 = 0
            sum_11_plus = 0
            for i, p in enumerate(prizes):
                if i < 10:
                    sum_top_10 += p
                else:
                    sum_11_plus += p

            piedata_list = [
                PieDataObj(sum_top_10, "#46BFBD", "#5AD3D1", "Top 10").get_data(),
                PieDataObj(sum_11_plus, "#FDB45C", "#FFC870", "All Other").get_data(),
            ]
            context['piedata'] = json.dumps(piedata_list)

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
            topprizes_list = [
                PieDataObj(prizes[0], "#46BFBD", "#5AD3D1", '1st').get_data(),
            ]
            if len(prizes) >= 2:
                topprizes_list.append(PieDataObj(prizes[1], "#FDB45C", "#FFC870", '2nd').get_data())
            if len(prizes) >= 3:
                topprizes_list.append(PieDataObj(prizes[2], "#F7464A", "#FF5A5E", '3rd').get_data())

            context['topprizes'] = json.dumps(topprizes_list)

            # at this point, if 'create' is True, we should
            # actually save & commit a new prize structure
            if create:
                creator = CashPrizeStructureCreator(self.prize_generator, 'generated')
                creator.save()

            context['created'] = create  # we should ACTUALLY create it though.

            # return HttpResponseRedirect('/success/')
            return render(request, self.template_name, context)

        context = {'form': form}
        return render(request, self.template_name, context)


class CreatePrizeStructureView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    Usage:

        http://localhost:8888/prize/create-prize-structure/?b=10&fp=1700&rp=10&ps=120&pp=10000
    """
    template_name = 'create_prize_structure.html'
    #
    # this will be set after the GET
    prize_generator = None
    permission_required = 'superuser'

    # get front end arguments #TODO
    def get(self, request, *args, **kwargs):
        print(str(request.GET))
        # >>> <QueryDict: {'b': ['10'], 'a': ['5']}>
        buyin = int(request.GET.get('b'))
        first_place = int(request.GET.get('fp'))
        round_payouts = int(request.GET.get('rp'))
        payout_spots = int(request.GET.get('ps'))
        prize_pool = int(request.GET.get('pp'))

        self.prize_generator = Generator(buyin, first_place,
                                         round_payouts, payout_spots, prize_pool)
        return super().get(request, *args, **kwargs)

    #
    # get the data which we wish to pass to the html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ex url GET params: ?b=10&fp=1500&rp=10&ps=120&pp=10000
        # Generator(b, fp, rp, ps, pp)
        # gen = Generator(10, 1500, 10, 120, 1000
        context['values'] = [1, 2, 3, 4, 5, 6]

        prize_list = self.prize_generator.get_prize_list()
        range_list = self.prize_generator.get_range_list()

        prizes = [x[1] for x in prize_list]
        distinct_prizes = [x[0] for x in range_list]
        distinct_prize_players = [len(x[1]) for x in range_list]
        min_rank_for_prize = [x[1][len(x[1]) - 1] for x in range_list]

        context['prizes'] = prizes
        context['ranks'] = list(range(1, len(prizes)))
        context['ranges'] = self.prize_generator.get_range_list()  # list( odata.items() )
        context['distinctprizes'] = distinct_prizes
        context['distinctprizeplayers'] = distinct_prize_players
        context['min_rank_for_prize'] = min_rank_for_prize

        # some values we might want
        context['maxentries'] = self.prize_generator.get_max_entries()
        paid = len(prize_list)
        context['paid'] = paid
        not_paid = int(self.prize_generator.get_max_entries() - len(prize_list))
        context['notpaid'] = not_paid

        # generate the data for 1st pie wheel
        payoutsdata_list = [
            PieDataObj(paid, "#46BFBD", "#5AD3D1", 'Paid').get_data(),
            PieDataObj(not_paid, "#F7464A", "#FF5A5E", 'Not Paid').get_data(),
        ]
        context['payoutsdata'] = json.dumps(payoutsdata_list)

        # top 10 prizes versus the rest of the prizes
        sum_top_10 = 0
        sum_11_plus = 0
        for i, p in enumerate(prizes):
            if i < 10:
                sum_top_10 += p
            else:
                sum_11_plus += p

        piedata_list = [
            PieDataObj(sum_top_10, "#46BFBD", "#5AD3D1", "Top 10").get_data(),
            PieDataObj(sum_11_plus, "#FDB45C", "#FFC870", "All Other").get_data(),
        ]
        context['piedata'] = json.dumps(piedata_list)

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
        topprizes_list = [
            PieDataObj(prizes[0], "#46BFBD", "#5AD3D1", '1st').get_data()
        ]
        if len(prizes) >= 2:
            topprizes_list.append(PieDataObj(prizes[1], "#FDB45C", "#FFC870", '2nd').get_data())
        if len(prizes) >= 3:
            topprizes_list.append(PieDataObj(prizes[2], "#F7464A", "#FF5A5E", '3rd').get_data())

        context['topprizes'] = json.dumps(topprizes_list)

        return context


class TicketPrizeStructureCreatorView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    This view uses FlatTicketPrizeStructureCreator to help create
    a prize structure with an even 10% total rake.
    """
    template_name = 'ticket_prize_creator.html'
    form_class = TicketPrizeCreatorForm  # this is for FLAT structures
    initial = {
        'buyin': 1,
        'ticket_amount': 2,
        'num_prizes': 25,
        'create': False
    }
    permission_required = 'superuser'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            #
            # get the values from the from fields
            buyin = form.cleaned_data['buyin']
            ticket_amount = form.cleaned_data['ticket_amount']
            num_prizes = form.cleaned_data['num_prizes']
            create = form.cleaned_data['create']
            print('buyin', buyin, 'ticket_amount:', ticket_amount, 'num_prizes:', num_prizes, 'create:', create)
            #

            buyin = float(buyin)
            num_prizes = int(num_prizes)
            ticket_value = float(ticket_amount.amount)
            # max_entries     = (float(ticket_value) * num_prizes) / buyin
            # have FlatTicketPrizeStructureCreator calculate the entries for us
            creator = FlatTicketPrizeStructureCreator(buyin, ticket_value, num_prizes, name='flat-ticket-gui')
            max_entries = creator.entries

            context = {'form': form}

            context['prizes'] = num_prizes
            context['ranks'] = list(range(1, num_prizes))
            context['ranges'] = [(ticket_value, list(range(1, num_prizes + 1)))]
            context['distinctprizes'] = 1
            context['distinctprizeplayers'] = num_prizes
            context['min_rank_for_prize'] = num_prizes

            # some values we might want
            context['maxentries'] = max_entries
            context['paid'] = num_prizes
            not_paid = max_entries - num_prizes
            context['notpaid'] = not_paid

            # generate the data for 1st pie wheel
            payoutsdata_list = []
            payoutsdata_list.append(PieDataObj(num_prizes, "#46BFBD", "#5AD3D1", 'Paid').get_data())
            payoutsdata_list.append(PieDataObj(not_paid, "#F7464A", "#FF5A5E", 'Not Paid').get_data())
            context['payoutsdata'] = json.dumps(payoutsdata_list)

            # top 10 prizes versus the rest of the prizes
            sum_top_10 = 0
            sum_11_plus = 0
            for i, p in enumerate(range(0, num_prizes)):
                if i < 10:
                    sum_top_10 += ticket_value
                else:
                    sum_11_plus += ticket_value

            piedata_list = []
            piedata_list.append(PieDataObj(sum_top_10, "#46BFBD", "#5AD3D1", "Top 10").get_data())
            piedata_list.append(PieDataObj(sum_11_plus, "#FDB45C", "#FFC870", "All Other").get_data())
            context['piedata'] = json.dumps(piedata_list)

            # top 3 prizes (if there are that many
            topprizes_list = [
                PieDataObj(ticket_value, "#46BFBD", "#5AD3D1", '1st').get_data()
            ]
            if num_prizes >= 2:
                topprizes_list.append(PieDataObj(ticket_value, "#FDB45C", "#FFC870", '2nd').get_data())
            if num_prizes >= 3:
                topprizes_list.append(PieDataObj(ticket_value, "#F7464A", "#FF5A5E", '3rd').get_data())

            context['topprizes'] = json.dumps(topprizes_list)

            #
            # at this point, if 'create' is True, we should
            # actually save & commit a new prize structure
            if create:
                # creator = FlatTicketPrizeStructureCreator( buyin, ticket_value, num_prizes, 'ticket-gui' )
                creator.save()

            context['created'] = create  # we should ACTUALLY create it though.

            # return HttpResponseRedirect('/success/')
            return render(request, self.template_name, context)

        #
        #
        context = {'form': form}
        return render(request, self.template_name, context)


class FlatCashPrizeStructureCreatorView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'superuser'
    template_name = 'flat_cash_prize_creator.html'
    form_class = FlatCashPrizeCreatorForm
    initial = {
        'buyin': 1.00,
        'first_place': 1.80,
        'payout_spots': 5,
        'create': False
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            buyin = form.cleaned_data['buyin']
            first_place = form.cleaned_data['first_place']
            payout_spots = form.cleaned_data['payout_spots']
            create = form.cleaned_data['create']

            print('buyin', buyin, 'first_place:', first_place,
                  'payout_spots:', payout_spots, 'create:', create)
            # need to be able to create this:
            # >>> creator = FlatCashPrizeStructureCreator(buyin, ticket_amount, num_payouts, name=name)
            # >>> creator.save()

            max_entries = (float(first_place) * payout_spots) / buyin

            context = {'form': form}

            context['prizes'] = payout_spots
            context['ranks'] = list(range(1, payout_spots))
            context['ranges'] = [(first_place, list(range(1, payout_spots + 1)))]
            context['distinctprizes'] = 1
            context['distinctprizeplayers'] = payout_spots
            context['min_rank_for_prize'] = payout_spots

            # some values we might want
            context['maxentries'] = max_entries
            context['paid'] = payout_spots
            not_paid = max_entries - payout_spots
            context['notpaid'] = not_paid

            # generate the data for 1st pie wheel
            payoutsdata_list = [
                PieDataObj(payout_spots, "#46BFBD", "#5AD3D1", 'Paid').get_data(),
                PieDataObj(not_paid, "#F7464A", "#FF5A5E", 'Not Paid').get_data(),
            ]
            context['payoutsdata'] = json.dumps(payoutsdata_list)

            # top 10 prizes versus the rest of the prizes
            sum_top_10 = 0
            sum_11_plus = 0
            for i, p in enumerate(range(0, payout_spots)):
                if i < 10:
                    sum_top_10 += first_place
                else:
                    sum_11_plus += first_place

            piedata_list = [
                PieDataObj(sum_top_10, "#46BFBD", "#5AD3D1", "Top 10").get_data(),
                PieDataObj(sum_11_plus, "#FDB45C", "#FFC870", "All Other").get_data(),
            ]
            context['piedata'] = json.dumps(piedata_list)

            # top 3 prizes (if there are that many
            topprizes_list = [
                PieDataObj(first_place, "#46BFBD", "#5AD3D1", '1st').get_data()
            ]
            if payout_spots >= 2:
                topprizes_list.append(PieDataObj(first_place, "#FDB45C", "#FFC870", '2nd').get_data())
            if payout_spots >= 3:
                topprizes_list.append(PieDataObj(first_place, "#F7464A", "#FF5A5E", '3rd').get_data())

            context['topprizes'] = json.dumps(topprizes_list)

            # at this point, if 'create' is True, we should
            # actually save & commit a new prize structure
            if create:
                creator = FlatCashPrizeStructureCreator(buyin, first_place, payout_spots,
                                                        'flat-cash-prize-structure')
                creator.save()

            context['created'] = create  # we should ACTUALLY create it though.

            # return HttpResponseRedirect('/success/')
            return render(request, self.template_name, context)

        context = {'form': form}
        return render(request, self.template_name, context)
