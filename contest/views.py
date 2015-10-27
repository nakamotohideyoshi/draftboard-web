#
# contest/views.py

import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError, NotFound
from contest.serializers import ContestSerializer, CurrentEntrySerializer, \
                                RegisteredUserSerializer, EnterLineupSerializer
from contest.classes import ContestLineupManager
from contest.models import Contest, Entry, LobbyContest, \
                            UpcomingContest, LiveContest, HistoryContest, CurrentContest
from contest.buyin.classes import BuyinManager
from contest.exceptions import ContestLineupMismatchedDraftGroupsException, \
                                ContestIsInProgressOrClosedException, \
                                ContestIsFullException, ContestCouldNotEnterException, \
                                ContestMaxEntriesReachedException, \
                                ContestIsNotAcceptingLineupsException
from lineup.models import Lineup
from dataden.util.simpletimer import SimpleTimer
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from contest.forms import ContestForm, ContestFormAdd

from django.db.models import Count

# test the generic add view
class ContestCreate(CreateView):
    model       = Contest
    form_class  = ContestFormAdd
    #fields      = ['name','ends_tonight','start']

# testing the generic edit view
class ContestUpdate(UpdateView):
    model       = Contest
    form_class  = ContestForm
    #fields      = ['name','start']

class SingleContestAPIView(generics.GenericAPIView):
    """
    get the information related to a specific Contest
    """

    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    serializer_class        = ContestSerializer
    permission_classes      = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Contest.objects.get(pk=pk)
        except Contest.DoesNotExist:
            raise NotFound()

    def get(self, request, contest_id, format=None):
        """
        given the GET param 'contest_id', get the contest
        """
        serialized_data = ContestSerializer( self.get_object(contest_id), many=False ).data
        return Response(serialized_data)

class LobbyAPIView(generics.ListAPIView):
    """
    Retrieve the contests which are relevant to the home page lobby.
    """

    authentication_classes  = (SessionAuthentication, BasicAuthentication)

    #
    # Dont need permission - we want everyone to be able to view upcoming contests!
    #permission_classes      = (IsAuthenticated,)

    serializer_class        = ContestSerializer

    #
    # Dont paginate - we really always want this api to return
    # the full list of lobby contests!
    #pagination_class        = LimitOffsetPagination

    def get_queryset(self):
        """
        Return a QuerySet from the LobbyContest model.
        """
        return LobbyContest.objects.all()

class UserEntryAPIView(generics.ListAPIView):

    contest_model           = None # child class must set this, see UserUpcomingAPIView for example

    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = ContestSerializer

    def get_entries(self, user, contests):
        """
        return a queryset of the users entries (a map between contest & lineup)
        which are from the
        """
        return Entry.objects.filter(lineup__user=user, contest__in=contests)

    def get_contests(self, user):
        if self.contest_model is None:
            raise Exception(self.__class__.__name__ + 'get_queryset() - contest_model must be set in inheriting class')

        # get a list of our entries to every possible distinct contest
        # timer = SimpleTimer()
        # timer.start()
        return self.contest_model.objects.all()

    def get_queryset(self):
        """
        Return a QuerySet from the UpcomingContest model, for authenticated user.

        raises Exception if the inheriting class did not set 'contest_model'
        """

        # distinct_entry_contests = Entry.objects.filter(lineup__user=self.request.user,
        #                                     contest__in=contests).distinct('contest__id')
        contests = self.get_contests(self.request.user)
        distinct_entry_contests = self.get_entries(self.request.user, contests).distinct('contest__id')
        data =  [ x.contest for x in distinct_entry_contests ]
        # timer.stop() - takes about 40 milliseconds for small datasets: ie: 100 entries
        return data

class CurrentEntryAPIView(generics.ListAPIView):

    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = CurrentEntrySerializer

    def get_entries(self, user, contests):
        """
        return a queryset of the users entries (a map between contest & lineup)
        which are from the
        """
        return Entry.objects.filter(lineup__user=user, contest__in=contests)

    def get_contests(self, user):
        # get a list of our entries to every possible distinct contest
        # timer = SimpleTimer()
        # timer.start()
        return CurrentContest.objects.all()

    def get_queryset(self):
        """
        Return a QuerySet from the UpcomingContest model, for authenticated user.

        raises Exception if the inheriting class did not set 'contest_model'
        """

        contests = self.get_contests(self.request.user)
        return self.get_entries(self.request.user, contests)

class UserUpcomingAPIView(UserEntryAPIView):
    """
    A User's upcoming Contests
    """
    contest_model = UpcomingContest

class UserLiveAPIView(UserEntryAPIView):
    """
    A User's live Contests
    """
    contest_model = LiveContest

class UserHistoryAPIView(UserEntryAPIView):
    """
    A User's historical contests.

    "next", "prev":  holds the link to paged data.
    "next", "prev":  may return null, which indicates no more paged data in that direction
    """

    contest_model   = HistoryContest
    pagination_class = LimitOffsetPagination

class AllLineupsView(View):
    """
    return all the lineups for a given contest as raw bytes, in our special compact format
    """

    def get(self, request, contest_id):
        clm = ContestLineupManager( contest_id = contest_id )
        if 'json' in request.GET:
            print ('json please!' )
            return HttpResponse( json.dumps( clm.dev_get_all_lineups( contest_id ) ) )
        else:
            #clm = ContestLineupManager( contest_id = contest_id )
            #return HttpResponse( ''.join('{:02x}'.format(x) for x in clm.get_bytes() ) )
            return HttpResponse( clm.get_http_payload() )

class SingleLineupView(View):
    """
    get a single lineup for any contest, lineup_id combination.

    this api will mask out players who should not yet be seen
    """

    def get(self, request, contest_id, lineup_id):
        clm = ContestLineupManager( contest_id = contest_id )
        lineup_data = clm.get_lineup_data( user= request.user, lineup_id=lineup_id )

        return HttpResponse( json.dumps(lineup_data), content_type="application/json" )

class RegisteredUsersAPIView(generics.GenericAPIView):
    """
    get the lineup Players
    """
    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    serializer_class        = RegisteredUserSerializer

    def get_object(self, contest_id):
        #
        # get the count of the # of lineups each distinct user has in the contest
        # In [53]: from django.db.models import Count
        # In [49]: entries = Entry.objects.filter( contest=c ).values('lineup__user__username').annotate(total=Count('lineup__user')).order_by('total')
        #
        # In [50]: entries
        # Out[50]: [{'total': 1, 'lineup__user__username': 'Villain34'}, {'total': 3, 'lineup__user__username': 'Hero'}]

        #
        # ***
        # WARNING - YOU MUST ALSO EDIT contest/serializers.RegisteredUserSerializer if you modify the values()  !!!
        # ***
        entries = Entry.objects.filter( contest__pk=contest_id ).values('lineup__user__username').annotate(total_entries=Count('lineup__user'))
        # example:
        # [
        #   {'total_entries': 3, 'lineup__user__username': 'Hero'},
        #   {'total_entries': 1, 'lineup__user__username': 'Villain34'}
        # ]
        return entries

    def get(self, request, contest_id, format=None):
        """
        get the registered user information
        """
        serialized_data = RegisteredUserSerializer( self.get_object(contest_id), many=True ).data
        return Response(serialized_data)

class EnterLineupAPIView(generics.CreateAPIView):
    """
    enter a lineup into the contest. (exceptions may occur based on user balance, etc...)
    """
    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = EnterLineupSerializer

    def post(self, request, format=None):
        #print( request.data )
        lineup_id       = request.data.get('lineup')
        contest_id      = request.data.get('contest')

        # ensure the contest is valid
        try:
            contest = Contest.objects.get( pk=contest_id )
        except Contest.DoesNotExist:
            return Response( 'Contest does not exist', status=status.HTTP_403_FORBIDDEN )

        # ensure the lineup is valid for this user
        try:
            lineup = Lineup.objects.get( pk=lineup_id, user=request.user )
        except Lineup.DoesNotExist:
            return Response( 'Lineup does not exist', status=status.HTTP_403_FORBIDDEN )

        #
        # call the buyin task
        bm = BuyinManager( request.user )
        try:
            bm.buyin( contest, lineup )
        except ContestLineupMismatchedDraftGroupsException:
            return Response( 'This lineup was not drafted from the same group as this contest.', status=status.HTTP_403_FORBIDDEN )
        except ContestIsInProgressOrClosedException:
            return Response( 'You may no longer enter this contest', status=status.HTTP_403_FORBIDDEN )
        except ContestCouldNotEnterException:
            return Response( 'ContestCouldNotEnterException', status=status.HTTP_403_FORBIDDEN )
        except ContestIsNotAcceptingLineupsException:
            return Response( 'Contest is not accepting entries', status=status.HTTP_403_FORBIDDEN )
        except (ContestMaxEntriesReachedException, ContestIsFullException) as e:
            return Response( 'Contest is full', status=status.HTTP_403_FORBIDDEN )

        #
        return Response('Lineup was successfully entered into the Contest!')
