#
# contest/views.py

import json

from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError, NotFound
from contest.serializers import ContestSerializer, CurrentEntrySerializer
from contest.classes import ContestLineupManager
from contest.models import Contest, Entry, LobbyContest, \
                            UpcomingContest, LiveContest, HistoryContest, CurrentContest

from dataden.util.simpletimer import SimpleTimer
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from contest.forms import ContestForm, ContestFormAdd


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
