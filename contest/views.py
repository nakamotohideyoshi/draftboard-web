#
# contest/views.py

from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, date, time, timedelta
import json
import celery
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from debreach.decorators import random_comment_exempt
from rest_framework.views import APIView
from rest_framework import renderers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError, NotFound
from contest.serializers import (
    ContestSerializer,
    UpcomingEntrySerializer,
    CurrentEntrySerializer,
    RegisteredUserSerializer,
    EnterLineupSerializer,
    EnterLineupStatusSerializer,
    PayoutSerializer,
    EditEntryLineupSerializer,
    EditEntryLineupStatusSerializer,
    RemoveAndRefundEntrySerializer,
    RemoveAndRefundEntryStatusSerializer,
    UserLineupHistorySerializer,
    #PlayHistoryLineupSerializer,
    RankedEntrySerializer,
    ContestPoolSerializer,
)
from contest.classes import (
    ContestLineupManager,
)
from contest.models import (
    Contest,
    ContestPool,
    Entry,
    CurrentContest,
    LiveContest,
    HistoryContest,
    HistoryEntry,
    ClosedEntry,
    LobbyContestPool,
    UpcomingContestPool,
)
from contest.payout.models import (
    Payout,
)
from contest.buyin.classes import BuyinManager
from contest.buyin.tasks import buyin_task
from contest.exceptions import (
    ContestLineupMismatchedDraftGroupsException,
    ContestIsInProgressOrClosedException,
    ContestIsFullException,
    ContestCouldNotEnterException,
    ContestMaxEntriesReachedException,
    ContestIsNotAcceptingLineupsException,
)
from contest.refund.tasks import unregister_entry_task
from cash.exceptions import OverdraftException
from lineup.models import Lineup
from lineup.tasks import edit_entry
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from contest.forms import ContestForm, ContestFormAdd
from django.db.models import Count
from mysite.celery_app import TaskHelper
from util.dfsdate import DfsDate

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

    serializer_class = ContestPoolSerializer

    def get_queryset(self):
        """
        Return a QuerySet from the LobbyContestPool model.
        """
        return LobbyContestPool.objects.all()


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
    """
    Get the User's current entries (the Entries they own in live/upcoming contests)
    """

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

class UserUpcomingContestPoolAPIView(UserEntryAPIView):
    """
    a user's registered-in ContestPools in the future
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = UpcomingEntrySerializer

    def get_entries(self, user):
        """
        return a queryset of the users entries (a map between contest & lineup)
        which are from the upcoming ContestPools
        """
        return Entry.objects.filter(lineup__user=user,
                                    contest_pool__in=UpcomingContestPool.objects.all())

    def get_queryset(self):
        """
        Return a QuerySet from the UpcomingContestPool model containing
        all the entries for the user
        """
        return self.get_entries(self.request.user)

class UserUpcomingContestPoolAndLiveContestEntriesAPIView(UserEntryAPIView):
    """
    a user's Entries which are registered-in ContestPools in the future,
    as well as Entries in live Contests
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = UpcomingEntrySerializer

    def get_entries(self, user):
        """
        return a queryset of the users entries (a map between contest & lineup)
        which are from the upcoming ContestPools
        """

        # Q(question__startswith='What')
        # return Entry.objects.filter(lineup__user=user,
        #                             contest_pool__in=UpcomingContestPool.objects.all())
        from contest.models import Entry, UpcomingContestPool, LiveContest
        from django.db.models import Q
        entries = Entry.objects.filter( Q(lineup__user=user),
                        Q(contest_pool__in=UpcomingContestPool.objects.all()) |
                        Q(contest__in=LiveContest.objects.all()))

    def get_queryset(self):
        """
        Return a QuerySet from the UpcomingContestPool model containing
        all the entries for the user
        """
        return self.get_entries(self.request.user)

class UserLiveAPIView(UserEntryAPIView):
    """
    A User's live Contests
    """
    contest_model = LiveContest

class UserHistoryAPIView(generics.GenericAPIView):
    """
    Allows the logged in user to get their historical entries/contests

        * |api-text| :dfs:`contest/history/`

        .. note::

            .By default it will return the last 100 historical entries

            Get parameters of **?start_ts=UNIX_TIMESTAMP&end_ts=UNIX_TIMESTAMP** can be used to
            set a date range to get entries between.

    """

    permission_classes      = (IsAuthenticated,)
    serializer_class        = CurrentEntrySerializer

    def get_user_for_id(self, user_id=None):
        """
        if a user can be found via the 'user_id' return it,
        else return None.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, format=None):
        """
        get the entries
        """
        user = self.request.user

        admin_specified_user_id = self.request.QUERY_PARAMS.get('user_id', None)
        admin_specified_user = self.get_user_for_id( admin_specified_user_id )
        if user.is_superuser and admin_specified_user is not None:
            # override the user whos transactions we will look at
            user = admin_specified_user

        #
        # if the start_ts & end_ts params exist:
        start_ts = self.request.QUERY_PARAMS.get('start_ts', None)
        end_ts = self.request.QUERY_PARAMS.get('end_ts', None)
        if start_ts is None and end_ts is None:
            #
            # get the last 100 entries
            entries = HistoryEntry.objects.filter().order_by('-created')[:100]
            return self.get_entries_response( entries )

        else:
            if start_ts == None:
                return Response(
                    status=409,
                    data={
                        'errors': {
                            'name': {
                                'title': 'start_ts required',
                                'description': 'You must provide unix time stamp variable start_ts in your get parameters.'
                            }
                        }
                    })
            if end_ts == None:
                return Response(
                    status=409,
                    data={
                        'errors': {
                            'name': {
                                'title': 'end_ts required',
                                'description': 'You must provide unix time stamp variable end_ts in your get parameters.'
                            }
                        }
                    })
            entries = self.get_entries_in_range( user, int(start_ts), int(end_ts) )
            return self.get_entries_response( entries )

    def get_entries_in_range(self, user, start_ts, end_ts):
        start   = datetime.utcfromtimestamp( start_ts )
        end     = datetime.utcfromtimestamp( end_ts )
        entries = Entry.objects.filter(contest__start__range=(start, end))
        return entries
        # serialized_entries = self.serializer_class( entries, many=True )
        # return Response(serialized_entries.data, status=status.HTTP_200_OK)

    def get_entries_response(self, entries):
        serialized_entries = self.serializer_class( entries, many=True )
        return Response(serialized_entries.data, status=status.HTTP_200_OK)

class AllLineupsView(View):
    """
    return all the lineups for a given contest as raw bytes, in our special compact format
    """

    @random_comment_exempt
    def get(self, request, contest_id):
        clm = ContestLineupManager( contest_id = contest_id )
        if 'json' in request.GET:
            #print ('json please!' )
            return HttpResponse( json.dumps( clm.dev_get_all_lineups( contest_id ) ) )
        else:
            #clm = ContestLineupManager( contest_id = contest_id )
            #return HttpResponse( ''.join('{:02x}'.format(x) for x in clm.get_bytes() ) )
            return HttpResponse(clm.get_http_payload(), content_type='application/octet-stream')


class SingleLineupView(View):
    """
    get a single lineup for any contest, lineup_id combination.

    this api will mask out players who should not yet be seen
    """

    def get(self, request, contest_id, lineup_id):
        clm = ContestLineupManager( contest_id = contest_id )
        lineup_data = clm.get_lineup_data( user= request.user, lineup_id=lineup_id )

        return HttpResponse( json.dumps(lineup_data), content_type="application/json" )

class SingleContestLineupView(View):
    """
    get a single lineup for any contest, lineup_id combination.

    this api will mask out players who should not yet be seen
    """

    def get(self, request, lineup_id):
        entries = Entry.objects.filter(lineup__pk=lineup_id)
        if entries.count() == 0:
            no_return_data = []
            return HttpResponse( json.dumps(no_return_data), content_type="application/json" )
        else:
            contest = entries[0].contest
            clm = ContestLineupManager( contest_id=contest.pk )
            lineup_data = clm.get_lineup_data( user= request.user, lineup_id=lineup_id )
            return HttpResponse( json.dumps(lineup_data), content_type="application/json" )

class RegisteredUsersAPIView(generics.GenericAPIView):
    """
    get the lineup Players
    """
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

class ContestRanksAPIView(generics.GenericAPIView):
    """
    get the lineup Players
    """
    serializer_class = RankedEntrySerializer

    def get_object(self, contest_id):
        """
        get the contest.models.Entry objects, ordered by their rank, for a given contest pk
        """
        entries = Entry.objects.filter( contest__pk=contest_id ).order_by('final_rank')
        return entries

    def get(self, request, contest_id, format=None):
        """
        get the registered user information
        """
        serialized_data = self.serializer_class( self.get_object(contest_id), many=True ).data
        return Response(serialized_data)

# class EnterLineupAPIView(generics.CreateAPIView):
#     """
#     enter a lineup into the contest. (exceptions may occur based on user balance, etc...)
#     """
#     permission_classes      = (IsAuthenticated,)
#     serializer_class        = EnterLineupSerializer
#     # renderer_classes        = (JSONRenderer, BrowsableAPIRenderer)
#
#     def post(self, request, format=None):
#         #print( request.data )
#         lineup_id       = request.data.get('lineup')
#         contest_id      = request.data.get('contest')
#
#         # ensure the contest is valid
#         try:
#             contest = Contest.objects.get( pk=contest_id )
#         except Contest.DoesNotExist:
#             return Response( 'Contest does not exist', status=status.HTTP_403_FORBIDDEN )
#
#         # ensure the lineup is valid for this user
#         try:
#             lineup = Lineup.objects.get( pk=lineup_id, user=request.user )
#         except Lineup.DoesNotExist:
#             return Response( 'Lineup does not exist', status=status.HTTP_403_FORBIDDEN )
#
#         #
#         # call the buyin task
#         bm = BuyinManager( request.user )
#         # TODO must use task not the regular way
#         try:
#             bm.buyin( contest, lineup )
#         except ContestLineupMismatchedDraftGroupsException:
#             return Response( 'This lineup was not drafted from the same group as this contest.', status=status.HTTP_403_FORBIDDEN )
#         except ContestIsInProgressOrClosedException:
#             return Response( 'You may no longer enter this contest', status=status.HTTP_403_FORBIDDEN )
#         except ContestCouldNotEnterException:
#             return Response( 'ContestCouldNotEnterException', status=status.HTTP_403_FORBIDDEN )
#         except ContestIsNotAcceptingLineupsException:
#             return Response( 'Contest is not accepting entries', status=status.HTTP_403_FORBIDDEN )
#         except (ContestMaxEntriesReachedException, ContestIsFullException) as e:
#             return Response( 'Contest is full', status=status.HTTP_403_FORBIDDEN )
#         except (OverdraftException) as e:
#             return Response('You have insufficient funds to enter this contest.', status=status.HTTP_403_FORBIDDEN )
#
#         # If Entry creation was successful, return the created Entry object.
#         entry = Entry.objects.get(contest__id=contest_id, lineup__id=lineup_id)
#         serializer = CurrentEntrySerializer(entry, many=False)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class EnterLineupAPIView(generics.CreateAPIView): # original for CONTESTS
#     """
#     enter a lineup into the contest. (exceptions may occur based on user balance, etc...)
#     """
#     permission_classes      = (IsAuthenticated,)
#     serializer_class        = EnterLineupSerializer
#     # renderer_classes        = (JSONRenderer, BrowsableAPIRenderer)
#
#     def post(self, request, format=None):
#         lineup_id       = request.data.get('lineup')
#         contest_id      = request.data.get('contest')
#
#         #print('contest_id', str(contest_id), 'str:', isinstance(contest_id, str))
#         # ensure the contest is valid
#         try:
#             contest = Contest.objects.get( pk=contest_id )
#         except Contest.DoesNotExist:
#             return Response( 'Contest does not exist', status=status.HTTP_403_FORBIDDEN )
#
#         # ensure the lineup is valid for this user
#         try:
#             lineup = Lineup.objects.get( pk=lineup_id, user=request.user )
#         except Lineup.DoesNotExist:
#             return Response( 'Lineup does not exist', status=status.HTTP_403_FORBIDDEN )
#
#         #
#         # call the buyin task - it has a time_limit of ~20 seconds before it will timeout
#         task_result = buyin_task.delay( request.user, contest, lineup=lineup )
#
#         #
#         # return task id
#         return Response({'buyin_task_id':task_result.id}, status=status.HTTP_201_CREATED)
#
#         # If Entry creation was successful, return the created Entry object.
#         # entry = Entry.objects.get(contest__id=contest_id, lineup__id=lineup_id)
#         # serializer = CurrentEntrySerializer(entry, many=False)
#         # return Response(serializer.data, status=status.HTTP_201_CREATED)

class EnterLineupAPIView(generics.CreateAPIView):
    """
    enter a lineup into a ContestPool. (exceptions may occur based on user balance, etc...)
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = EnterLineupSerializer

    def post(self, request, format=None):
        lineup_id       = request.data.get('lineup')
        contest_pool_id      = request.data.get('contest_pool')

        # ensure the ContestPool exists
        try:
            contest = ContestPool.objects.get( pk=contest_pool_id )
        except ContestPool.DoesNotExist:
            return Response( 'ContestPool does not exist', status=status.HTTP_403_FORBIDDEN )

        # ensure the lineup is valid for this user
        try:
            lineup = Lineup.objects.get( pk=lineup_id, user=request.user )
        except Lineup.DoesNotExist:
            return Response( 'Lineup does not exist', status=status.HTTP_403_FORBIDDEN )

        #
        # call the buyin task - it has a time_limit of ~20 seconds before it will timeout
        task_result = buyin_task.delay( request.user, contest, lineup=lineup ) # TODO - check this after the call and commit

        #
        # return task id
        return Response({'buyin_task_id':task_result.id}, status=status.HTTP_201_CREATED)

        # If Entry creation was successful, return the created Entry object.
        # entry = Entry.objects.get(contest__id=contest_id, lineup__id=lineup_id)
        # serializer = CurrentEntrySerializer(entry, many=False)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

class EnterLineupStatusAPIView(generics.GenericAPIView):

    permission_classes      = (IsAuthenticated,)
    serializer_class        = EnterLineupStatusSerializer

    def get(self, request, task_id, format=None):
        """
        Given the 'task' parameter, return the status of the task (ie: the buyin)

        :param request:
        :param format:
        :return:
        """
        task_helper = TaskHelper(buyin_task, task_id)
        return Response(task_helper.get_data(), status=status.HTTP_200_OK)

class PayoutsAPIView(generics.ListAPIView):
    """
    get a list of the payouts with ranks, for the paid users in the contest

    may return an empty array if no payouts have happened
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = PayoutSerializer

    def get_queryset(self):
        """
        get the Payout objects for the contest
        """
        contest_id = self.kwargs['contest_id']
        return Payout.objects.filter(entry__contest__pk=contest_id).order_by('rank')

class EditEntryLineupAPIView(APIView):
    """
    edit an existing lineup in a contest
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = EditEntryLineupSerializer

    def post(self, request, format=None):
        entry_id    = request.data.get('entry')
        players     = request.data.get('players', [])
        name        = request.data.get('name','')

        #
        # validate the parameters passed in here.
        if players is None:
            return Response({'error':'you must supply the "players" parameter -- the list of player ids'},
                                        status=status.HTTP_400_BAD_REQUEST )
        if entry_id is None:
            return Response({'error':'you must supply the "entry" parameter -- the Entry id'},
                                        status=status.HTTP_400_BAD_REQUEST )
        try:
            entry = Entry.objects.get(pk=entry_id, user=request.user)
        except Entry.DoesNotExist:
            return Response({'error':'invalid "entry" parameter -- does not exist'},
                                        status=status.HTTP_400_BAD_REQUEST )
        #
        # call task
        task_result = edit_entry.delay(request.user, players, entry)
        return Response({'task_id':task_result.id}, status=status.HTTP_201_CREATED)

class EditEntryLineupStatusAPIView(generics.GenericAPIView):
    """
    get status information for the task which performed work for the "edit entry" api
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = EditEntryLineupStatusSerializer

    def get(self, request, task_id, format=None):
        """
        Given the 'task' parameter, return the status of the task (ie: from performing the edit-entry)

        :param request:
        :param format:
        :return:
        """
        task_helper = TaskHelper(edit_entry, task_id)
        return Response(task_helper.get_data(), status=status.HTTP_200_OK)

class RemoveAndRefundEntryAPIView(APIView):
    """
    removes a contest Entry and refunds the user.
    """

    permission_classes  = (IsAuthenticated, )
    serializer_class    = RemoveAndRefundEntrySerializer

    def post(self, request, entry_id, format=None):
        # entry_id = request.data.get('entry')

        # validate the parameters passed in here.
        if entry_id is None:
            return Response({'error':'you must supply the "entry" parameter -- the Entry id'},
                                        status=status.HTTP_400_BAD_REQUEST )
        try:
            entry = Entry.objects.get(pk=entry_id, user=request.user)
        except Entry.DoesNotExist:
            return Response({'error':'invalid "entry" parameter -- does not exist'},
                                        status=status.HTTP_400_BAD_REQUEST )

        #
        # except for the admin, only the user who created the Entry can unregister it
        user = self.request.user
        #print( user, user.is_superuser, entry.user, 'user == entry.user -> %s' % str(user==entry.user))
        if not (user.is_superuser or user == entry.user):
            return Response({'error':'only an admin or the creating user can unregister this entry'},
                                            status=status.HTTP_403_FORBIDDEN )

        #
        # execute the unregister task (non-blocking) and return the task_id
        task = unregister_entry_task.delay( entry )
        return Response({'task_id':task.id}, status=status.HTTP_201_CREATED)

class RemoveAndRefundEntryStatusAPIView(generics.GenericAPIView):
    """
    get status information for the task which performed the "unregister entry" action
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = RemoveAndRefundEntryStatusSerializer

    def get(self, request, task_id, format=None):
        """
        Given the 'task' parameter, return the status of the task (ie: from performing the edit-entry)

        :param request:
        :param format:
        :return:
        """
        task_helper = TaskHelper(unregister_entry_task, task_id)
        return Response(task_helper.get_data(), status=status.HTTP_200_OK)

# class UserPlayHistoryAPIView(generics.ListAPIView):
#     """
#     get the entry history for a user lineups on a day
#     """
#
#     permission_classes      = (IsAuthenticated,)
#     serializer_class        = UserLineupHistorySerializer
#
#     def get_queryset(self):
#         """
#         retrieve the Lineup objects
#         """
#         rng     = DfsDate.get_current_dfs_date_range()
#         yyyy    = int(self.kwargs['year'])
#         mm      = int(self.kwargs['month'])
#         dd      = int(self.kwargs['day'])
#         start   = rng[0].replace( yyyy, mm, dd )
#         end     = start + timedelta(days=1)
#         print('range(%s, %s)' % (start, end))
#
#         # get a list of the lineups in historical entries for the day
#         history_entries = ClosedEntry.objects.filter( user=self.request.user,
#                                                        contest__start__range=(start, end) ) #,
#                                                        #contest__status=Contest.CLOSED )
#         for he in history_entries:
#             print( he, str(he.contest) )
#         historical_entry_lineups = [ e.lineup for e in history_entries ]
#         return historical_entry_lineups

class UserPlayHistoryAPIView(APIView):
    """
    get the entry history for a user lineups on a day
    """

    permission_classes      = (IsAuthenticated,)
    serializer_class        = UserLineupHistorySerializer

    def get(self, request, year, month, day, format=None):
        """
        Given the 'task' parameter, return the status of the task (ie: the buyin)

        :param request:
        :param format:
        :return:
        """
        #print( year, month, day)
        rng     = DfsDate.get_current_dfs_date_range()
        start   = rng[0].replace( int(year), int(month), int(day) )
        end     = start + timedelta(days=1)
        #print('range(%s, %s)' % (start, end))

        # get a list of the lineups in historical entries for the day
        history_entries = ClosedEntry.objects.filter( user=self.request.user,
                                                       contest__start__range=(start, end) )
        payouts = Payout.objects.filter( entry__in=history_entries)
        distinct_lineup_ids = [ e.lineup.pk for e in history_entries ]
        lineup_map = {}
        for entry in history_entries:
            lineup_map[ entry.lineup.pk ] = entry.lineup

        #
        # sum the values for each lineup (and all its entries for paid contests)
        total_buyins = 0
        num_entries = 0
        winnings = 0
        possible = 0
        contest_map = {}
        for lineup in list(lineup_map.values()):     # for each distinct lineup
            for history_entry in history_entries.filter(lineup=lineup):
                total_buyins += history_entry.contest.buyin
                num_entries += 1
                try:
                    winnings += payouts.get(entry=history_entry).amount
                except Payout.DoesNotExist:
                    pass
                print( possible, 'plus', history_entry.contest.prize_structure.generator.first_place)
                possible += history_entry.contest.prize_structure.generator.first_place
                contest_map[ history_entry.contest.pk ] = history_entry.contest

        overall = {
            "buyins"    : '%.2f' % total_buyins,
            "entries"   : num_entries,
            "winnings"  : '%.2f' % winnings,
            "possible"  : '%.2f' % possible,
            "contests"  : len(contest_map.values()),
        }

        data = {
            'lineups'   : self.serializer_class( list(lineup_map.values()), many=True).data,
            'overall'   : overall,
        }

        return Response(data, status=status.HTTP_200_OK)
