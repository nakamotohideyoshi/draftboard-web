#
# contest/views.py

from django.contrib.auth.models import User
from django.utils import timezone
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
    CurrentEntrySerializer,
    RegisteredUserSerializer,
    EnterLineupSerializer,
    EnterLineupStatusSerializer,
    PayoutSerializer,
    EditEntryLineupSerializer,
    EditEntryLineupStatusSerializer,
)
from contest.classes import ContestLineupManager
from contest.models import (
    Contest,
    Entry,
    LobbyContest,
    UpcomingContest,
    LiveContest,
    HistoryContest,
    CurrentContest,
    HistoryEntry,
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

from cash.exceptions import OverdraftException
from lineup.models import Lineup
from lineup.tasks import edit_entry
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from contest.forms import ContestForm, ContestFormAdd
from django.db.models import Count
from mysite.celery_app import TaskHelper

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

class UserHistoryAPIView(generics.GenericAPIView):
    """
    Allows the logged in user to get their historical entries/contests

        * |api-text| :dfs:`contest/history/`

        .. note::

            By default it will return the last 100 historical entries.

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

class EnterLineupAPIView(generics.CreateAPIView):
    """
    enter a lineup into the contest. (exceptions may occur based on user balance, etc...)
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = EnterLineupSerializer
    # renderer_classes        = (JSONRenderer, BrowsableAPIRenderer)

    def post(self, request, format=None):
        lineup_id       = request.data.get('lineup')
        contest_id      = request.data.get('contest')

        #print('contest_id', str(contest_id), 'str:', isinstance(contest_id, str))
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
        # call the buyin task - it has a time_limit of ~20 seconds before it will timeout
        task_result = buyin_task.delay( request.user, contest, lineup=lineup )

        #
        # return task id
        return Response({'buyin_task_id':task_result.id}, status=status.HTTP_201_CREATED)

        # If Entry creation was successful, return the created Entry object.
        # entry = Entry.objects.get(contest__id=contest_id, lineup__id=lineup_id)
        # serializer = CurrentEntrySerializer(entry, many=False)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

class EnterLineupStatusAPIView(APIView):
    """
    check the status of enter-lineup, having previously attempted to
    buy a lineup into a contest...

    TODO - add more description here about returned data

    TODO - clean this up:
    In [4]: t1
    Out[4]: <AsyncResult: a0a793e6-195c-45c4-afbe-8447e3507278>

    In [5]: t2
    Out[5]: <AsyncResult: de582118-c33a-43b0-930d-b94aa95f2526>

    In [6]: t1.status
    Out[6]: 'FAILURE'

    In [7]: t2.status
    Out[7]: 'SUCCESS'

    In [8]: th1 = TaskHelper( pause_then_raise, t1.id )

    In [9]: th1.get_data()
    Out[9]:
    {'result': None,
     'exception': {'msg': 'this was throw on purpose to test',
      'name': 'Exception'},
     'status': 'FAILURE',
     'task': {'status': 'FAILURE', 'description': 'Task failed'},
     'note': "status will be in ['SUCCESS', 'PENDING', 'FAILURE']. if status is in ['PENDING'], you may poll this api."}

    In [10]: th2 = TaskHelper( heartbeat, t2.id )

    In [11]: th2.get_data()
    Out[11]:
    {'result': {'value': None},
     'exception': None,
     'status': 'SUCCESS',
     'task': {'status': 'SUCCESS', 'description': 'Task succeeded'},
     'note': "status will be in ['SUCCESS', 'PENDING', 'FAILURE']. if status is in ['PENDING'], you may poll this api."}

    """

    permission_classes      = (IsAuthenticated,)
    serializer_class        = EnterLineupStatusSerializer # TODO create a serializer for response for swagger

    def post(self, request, format=None):
        """
        Given the 'task' parameter, return the status of the task (ie: the buyin)

        :param request:
        :param format:
        :return:
        """
        task_id = request.data.get('task_id')
        if task_id is None:
            # make sure to return error if the task id is not given in the request
            return Response({'error':'you must supply the "task" parameter'},
                                        status=status.HTTP_400_BAD_REQUEST )

        #
        # the TaskHelper class helps us retrieve useful information
        # about the status, and any exceptions that may have happened,
        # and that data is retrieved with the get_result_data() method.
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

        return Response('lineup created')

class EditEntryLineupStatusAPIView(generics.GenericAPIView):
    """
    check the status of a previous call to edit-entry, using the task id
    returned from edit-entry call
    """

    permission_classes      = (IsAuthenticated,)
    serializer_class        = EditEntryLineupStatusSerializer # TODO create a serializer for response for swagger

    def post(self, request, format=None):
        """
        Given the 'task_id' parameter, return the status of the task (ie: the edit-lineup call)

        :param request:
        :param format:
        :return:
        """
        task_id = request.data.get('task_id')
        if task_id is None:
            # make sure to return error if the task id is not given in the request
            return Response({'error':'you must supply the "task_id" parameter'},
                                        status=status.HTTP_400_BAD_REQUEST )

        #
        # the TaskHelper class helps us retrieve useful information
        # about the status, and any exceptions that may have happened,
        # and that data is retrieved with the get_result_data() method.
        task_helper = TaskHelper(edit_entry, task_id)
        return Response(task_helper.get_data(), status=status.HTTP_200_OK)