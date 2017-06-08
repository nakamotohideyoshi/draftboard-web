import json
import logging
from datetime import timedelta

from debreach.decorators import random_comment_exempt
from django.http import HttpResponse
from django.views.generic import View
from raven.contrib.django.raven_compat.models import client
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    APIException,
    PermissionDenied,
)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account import const as _account_const
from account.models import Limit
from account.permissions import (
    HasIpAccess,
    HasVerifiedIdentity,
)
from account.tasks import send_entry_alert_email
from account.utils import create_user_log
from cash.exceptions import OverdraftException
from contest.buyin.tasks import buyin_task
from contest.classes import (
    ContestLineupManager,
    SkillLevelManager,
)
from contest.exceptions import (
    ContestMaxEntriesReachedException,
)
from contest.models import (
    Contest,
    ContestPool,
    Entry,
    CurrentContest,
    LiveContest,
    CurrentEntry,
    ClosedEntry,
    LobbyContestPool,
    UpcomingContestPool,
)
from contest.payout.models import (
    Payout,
)
from contest.refund.tasks import unregister_entry_task
from contest.serializers import (
    ContestSerializer,
    UpcomingEntrySerializer,
    CurrentEntrySerializer,
    RegisteredUserSerializer,
    EnterLineupSerializer,
    PayoutSerializer,
    EditEntryLineupSerializer,
    EntryResultSerializer,
    RemoveAndRefundEntrySerializer,
    UserLineupHistorySerializer,
    RankedEntrySerializer,
    ContestPoolSerializer,
)
from lineup.models import Lineup
from lineup.tasks import edit_entry
from mysite.celery_app import TaskHelper
from ticket.exceptions import UserDoesNotHaveTicketException
from util.dfsdate import DfsDate

logger = logging.getLogger('contest.views')


class SingleContestAPIView(generics.GenericAPIView):
    """
    get the information related to a specific Contest
    """

    serializer_class = ContestSerializer

    def get_object(self, pk):
        try:
            return Contest.objects.get(pk=pk)
        except Contest.DoesNotExist:
            raise NotFound()

    def get(self, request, contest_id, format=None):
        """
        given the GET param 'contest_id', get the contest
        """
        serialized_data = ContestSerializer(self.get_object(contest_id), many=False).data
        return Response(serialized_data)


class SingleContestPoolAPIView(generics.GenericAPIView):
    """
    get the information related to a specific Contest
    """

    serializer_class = ContestPoolSerializer

    def get_object(self, pk):
        try:
            return ContestPool.objects.get(pk=pk)
        except ContestPool.DoesNotExist:
            raise NotFound()

    def get(self, request, contest_pool_id, format=None):
        """
        given the GET param 'contest_pool_id', get the contest pool
        """
        serialized_data = ContestPoolSerializer(self.get_object(contest_pool_id), many=False).data
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
        return LobbyContestPool.objects.select_related(
            'site_sport', 'draft_group', 'prize_structure'
        ).prefetch_related('prize_structure__ranks', 'prize_structure__generator').all()


class UserEntryAPIView(generics.ListAPIView):
    contest_model = None  # child class must set this, see UserUpcomingAPIView for example

    permission_classes = (IsAuthenticated,)
    serializer_class = ContestSerializer

    def get_entries(self, user, contests):
        """
        return a queryset of the users entries (a map between contest & lineup)
        which are from the
        """
        return Entry.objects.filter(lineup__user=user, contest__in=contests)

    def get_contests(self, user):
        if self.contest_model is None:
            raise Exception(self.__class__.__name__ +
                            'get_queryset() - contest_model must be set in inheriting class')

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
        distinct_entry_contests = self.get_entries(
            self.request.user, contests).distinct('contest__id')
        data = [x.contest for x in distinct_entry_contests]
        # timer.stop() - takes about 40 milliseconds for small datasets: ie: 100 entries
        return data


class CurrentEntryAPIView(generics.ListAPIView):
    """
    Get the User's current entries (the Entries they own in live/upcoming contests)
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CurrentEntrySerializer

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
    permission_classes = (IsAuthenticated,)
    serializer_class = UpcomingEntrySerializer

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
    permission_classes = (IsAuthenticated,)
    serializer_class = UpcomingEntrySerializer

    def get_entries(self, user):
        """
        return a queryset of the users entries (a map between contest & lineup)
        which are from the upcoming ContestPools
        """
        return CurrentEntry.objects.all()

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


# class UserHistoryAPIView(generics.GenericAPIView):
#     """
#     Allows the logged in user to get their historical entries/contests
#
#         * |api-text| :dfs:`contest/history/`
#
#         .. note::
#
#             .By default it will return the last 100 historical entries
#
#             Get parameters of **?start_ts=UNIX_TIMESTAMP&end_ts=UNIX_TIMESTAMP** can be used to
#             set a date range to get entries between.
#
#     """
#
#     permission_classes = (IsAuthenticated,)
#     serializer_class = CurrentEntrySerializer
#
#     def get_user_for_id(self, user_id=None):
#         """
#         if a user can be found via the 'user_id' return it,
#         else return None.
#         """
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
#
#     def get(self, request, format=None):
#         """
#         get the entries
#         """
#         user = self.request.user
#
#         admin_specified_user_id = self.request.QUERY_PARAMS.get('user_id', None)
#         admin_specified_user = self.get_user_for_id(admin_specified_user_id)
#         if user.is_superuser and admin_specified_user is not None:
#             # override the user whos transactions we will look at
#             user = admin_specified_user
#
#         #
#         # if the start_ts & end_ts params exist:
#         start_ts = self.request.QUERY_PARAMS.get('start_ts', None)
#         end_ts = self.request.QUERY_PARAMS.get('end_ts', None)
#         if start_ts is None and end_ts is None:
#             #
#             # get the last 100 entries
#             entries = HistoryEntry.objects.filter().order_by('-created')[:100]
#             return self.get_entries_response(entries)
#
#         else:
#             if start_ts is None:
#                 return Response(
#                     status=409,
#                     data={
#                         'errors': {
#                             'name': {
#                                 'title': 'start_ts required',
#                                 'description': """You must provide unix time stamp variable start_ts
#                                                     in your get parameters."""
#                             }
#                         }
#                     })
#             if end_ts is None:
#                 return Response(
#                     status=409,
#                     data={
#                         'errors': {
#                             'name': {
#                                 'title': 'end_ts required',
#                                 'description': """You must provide unix time stamp variable end_ts in
#                                                     your get parameters."""
#                             }
#                         }
#                     })
#             entries = self.get_entries_in_range(user, int(start_ts), int(end_ts))
#             return self.get_entries_response(entries)
#
#     def get_entries_in_range(self, user, start_ts, end_ts):
#         start = datetime.utcfromtimestamp(start_ts)
#         end = datetime.utcfromtimestamp(end_ts)
#         entries = Entry.objects.filter(contest__start__range=(start, end))
#         return entries
#         # serialized_entries = self.serializer_class( entries, many=True )
#         # return Response(serialized_entries.data, status=status.HTTP_200_OK)
#
#     def get_entries_response(self, entries):
#         serialized_entries = self.serializer_class(entries, many=True)
#         return Response(serialized_entries.data, status=status.HTTP_200_OK)
#

class AllLineupsView(View):
    """
    return all the lineups for a given contest as raw bytes, in our special compact format
    """

    @random_comment_exempt
    def get(self, request, contest_id):
        clm = ContestLineupManager(contest_id=contest_id)
        if 'json' in request.GET:
            return HttpResponse(json.dumps(clm.dev_get_all_lineups(contest_id)))
        else:
            # clm = ContestLineupManager( contest_id = contest_id )
            # return HttpResponse( ''.join('{:02x}'.format(x) for x in clm.get_bytes() ) )
            return HttpResponse(clm.get_http_payload(), content_type='application/octet-stream')


class SingleLineupView(View):
    """
    get a single lineup for any contest, lineup_id combination.

    this api will mask out players who should not yet be seen
    """

    def get(self, request, contest_id, lineup_id):
        clm = ContestLineupManager(contest_id=contest_id)
        lineup_data = clm.get_lineup_data(user=request.user, lineup_id=lineup_id)

        return HttpResponse(json.dumps(lineup_data), content_type="application/json")


class SingleContestLineupView(View):
    """
    get a single lineup for any contest, lineup_id combination.

    this api will mask out players who should not yet be seen
    """

    def get(self, request, lineup_id):
        entries = Entry.objects.filter(lineup__pk=lineup_id).exclude(contest__pk=None)
        if entries.count() == 0:
            no_return_data = []
            return HttpResponse(json.dumps(no_return_data), content_type="application/json")
        else:
            contest = entries[0].contest
            clm = ContestLineupManager(contest_id=contest.pk)
            lineup_data = clm.get_lineup_data(user=request.user, lineup_id=lineup_id)
            return HttpResponse(json.dumps(lineup_data), content_type="application/json")


class RegisteredUsersAPIView(generics.ListAPIView):
    """
    get the lineup Players
    """
    serializer_class = RegisteredUserSerializer

    def get_queryset(self):
        """
        get the registered user information
        """
        return Entry.objects.filter(
            contest_pool_id=self.kwargs['contest_id']).values('lineup__user__username', 'id')


class ContestRanksAPIView(generics.GenericAPIView):
    """
    get the lineup Players
    """
    serializer_class = RankedEntrySerializer

    def get_object(self, contest_id):
        """
        get the contest.models.Entry objects, ordered by their rank, for a given contest pk
        """
        entries = Entry.objects.filter(contest__pk=contest_id).order_by('final_rank')
        return entries

    def get(self, request, contest_id, format=None):
        """
        get the registered user information
        """
        serialized_data = self.serializer_class(self.get_object(contest_id), many=True).data
        return Response(serialized_data)


class EnterLineupAPIView(generics.CreateAPIView):
    """
    enter a lineup into a ContestPool. (exceptions may occur based on user balance, etc...)
    """
    log_action = _account_const.CONTEST_ENTERED
    permission_classes = (IsAuthenticated, HasIpAccess, HasVerifiedIdentity)
    serializer_class = EnterLineupSerializer

    def post(self, request, format=None):
        lineup_id = request.data.get('lineup')
        contest_pool_id = request.data.get('contest_pool')

        # ensure the ContestPool exists
        try:
            contest_pool = ContestPool.objects.get(pk=contest_pool_id)
        except ContestPool.DoesNotExist:
            # return Response( 'ContestPool does not exist', status=status.HTTP_403_FORBIDDEN )
            raise APIException('ContestPool does not exist')

        # ensure the lineup is valid for this user
        try:
            lineup = Lineup.objects.get(pk=lineup_id, user=request.user)
        except Lineup.DoesNotExist:
            # return Response( 'Lineup does not exist', status=status.HTTP_403_FORBIDDEN )
            raise APIException('Lineup does not exist')

        # check if this user can enter this skill level
        skill_level_manager = SkillLevelManager()
        try:
            skill_level_manager.validate_can_enter(request.user, contest_pool)
        except SkillLevelManager.CanNotEnterSkillLevel:
            raise APIException('You may not enter this Skill Level.')

        try:
            contest_entry_alert = request.user.limits.get(type=Limit.ENTRY_ALERT)
            entries_count = Entry.objects.filter(
                user=request.user,
                created__range=contest_entry_alert.time_period_boundaries,
                contest_pool__draft_group=contest_pool.draft_group,
            ).count()
            if entries_count == contest_entry_alert.value:
                send_entry_alert_email.delay(user=request.user)
        except Limit.DoesNotExist:
            pass

        try:
            contest_entry_limit = request.user.limits.get(type=Limit.ENTRY_LIMIT)
            entries_count = Entry.objects.filter(
                user=request.user,
                created__range=contest_entry_limit.time_period_boundaries,
                contest_pool__draft_group=contest_pool.draft_group,
            ).count()
            if entries_count == contest_entry_limit.value:
                raise APIException(
                    'You have reached your contest entry limit of {} entries.'.format(
                        contest_entry_limit.value))
        except Limit.DoesNotExist:
            pass

        try:
            entry_fee_limit = request.user.limits.get(type=Limit.ENTRY_FEE)
            if contest_pool.prize_structure.buyin > entry_fee_limit.value:
                raise APIException(
                    'You have reached your entry fee limit of {}.'.format(entry_fee_limit.value))
        except Limit.DoesNotExist:
            pass

        try:
            # get() blocks the view from returning until the task completes its work
            task_result = buyin_task.delay(request.user, contest_pool, lineup=lineup)
            task_result.get()
        except OverdraftException:
            raise ValidationError(
                {"detail": "You do not have the necessary funds for this action."})
        except ContestMaxEntriesReachedException as e:
            raise ValidationError({"detail": "%s" % e})
        except UserDoesNotHaveTicketException:
            raise ValidationError({"detail": "You do not have the necessary funds."})
        except Exception as e:
            logger.error("EnterLineupAPIView: %s" % str(e))
            client.captureException()
            raise APIException({"detail": "Unable to enter contest."})

        task_helper = TaskHelper(buyin_task, task_result.id)
        data = task_helper.get_data()
        # dont break what was there by adding this extra field
        data['buyin_task_id'] = task_result.id

        # Create a user log entry.
        create_user_log(
            request=request,
            type=_account_const.CONTEST,
            action=_account_const.CONTEST_ENTERED,
            metadata={
                'detail': 'Contest Entered.',
                'contest_pool': contest_pool_id,
                'lineup': lineup_id,
            }
        )

        return Response(data, status=status.HTTP_200_OK)


class EntryResultAPIView(generics.RetrieveAPIView):
    """
    Returns everything we need to display the results of the specified contest entry.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EntryResultSerializer

    def get_object(self):
        obj = get_object_or_404(Entry.objects.select_related('contest', 'contest__prize_structure'),
                                id=self.kwargs['entry_id'])
        if not (obj.user == self.request.user):
            raise PermissionDenied()

        self.check_object_permissions(self.request, obj)
        return obj


class PayoutsAPIView(generics.ListAPIView):
    """
    get a list of the payouts with ranks, for the paid users in the contest

    may return an empty array if no payouts have happened
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PayoutSerializer

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
    permission_classes = (IsAuthenticated,)
    serializer_class = EditEntryLineupSerializer

    def post(self, request, format=None):
        entry_id = request.data.get('entry')
        players = request.data.get('players', [])
        # name = request.data.get('name', '')

        #
        # validate the parameters passed in here.
        if players is None:
            raise APIException('you must supply the list of Player ids.')

        if entry_id is None:
            raise APIException('you must supply the Entry id')

        try:
            entry = Entry.objects.get(pk=entry_id, user=request.user)
        except Entry.DoesNotExist:
            raise APIException('invalid Entry id')

        # execute task
        task_result = edit_entry.delay(request.user, players, entry)
        # get() blocks the view until the task completes its work
        task_result.get()
        task_helper = TaskHelper(edit_entry, task_result.id)
        return Response(task_helper.get_data(), status=status.HTTP_201_CREATED)


class RemoveAndRefundEntryAPIView(APIView):
    """
    removes a contest Entry and refunds the user.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RemoveAndRefundEntrySerializer

    def post(self, request, entry_id, format=None):
        # entry_id = request.data.get('entry')

        # validate the parameters passed in here.
        if entry_id is None:
            raise APIException('you must supply the Entry id')

        try:
            entry = Entry.objects.get(pk=entry_id, user=request.user)
        except Entry.DoesNotExist:
            raise APIException('Entry does not exist.')

        # except for the admin, only the user who created the Entry can unregister it
        user = self.request.user
        if not (user.is_superuser or user == entry.user):
            raise APIException('You are restricted from unregistering this Entry.')

        if entry.contest_pool not in UpcomingContestPool.objects.all():
            raise APIException('You may not unregister at this time.')

        #
        # execute the unregister task (non-blocking) and return the task_id
        task_result = unregister_entry_task.delay(entry)
        # get() blocks the view from returning until the task finishes
        task_result.get()
        task_helper = TaskHelper(unregister_entry_task, task_result.id)

        create_user_log(
            request=request,
            type=_account_const.CONTEST,
            action=_account_const.CONTEST_DEREGISTERED,
            metadata={
                'detail': 'Contest entry was deregistered.',
                'entry': entry_id,
            }
        )

        return Response(task_helper.get_data(), status=status.HTTP_201_CREATED)


class UserPlayHistoryAPIView(APIView):
    """
    get the entry history for a user lineups on a day
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserLineupHistorySerializer

    def get_history_data(self, year, month, day):
        """
        get the historical lineup data
        """
        rng = DfsDate.get_current_dfs_date_range()
        start = rng[0].replace(int(year), int(month), int(day))
        end = start + timedelta(days=1)

        # get a list of the lineups in historical entries for the day
        history_entries = ClosedEntry.objects.filter(user=self.request.user,
                                                     contest__start__range=(start, end))
        payouts = Payout.objects.filter(entry__in=history_entries)
        # distinct_lineup_ids = [e.lineup.pk for e in history_entries]
        lineup_map = {}
        for entry in history_entries:
            lineup_map[entry.lineup.pk] = entry.lineup

        #
        # sum the values for each lineup (and all its entries for paid contests)
        total_buyins = 0
        num_entries = 0
        winnings = 0
        possible = 0
        contest_map = {}
        for lineup in list(lineup_map.values()):  # for each distinct lineup
            for history_entry in history_entries.filter(lineup=lineup):
                total_buyins += history_entry.contest.buyin
                num_entries += 1
                try:
                    winnings += payouts.get(entry=history_entry).amount
                except Payout.DoesNotExist:
                    pass
                possible += history_entry.contest.prize_structure.generator.first_place
                contest_map[history_entry.contest.pk] = history_entry.contest

        overall = {
            "buyins": '%.2f' % total_buyins,
            "entries": num_entries,
            "winnings": '%.2f' % winnings,
            "possible": '%.2f' % possible,
            "contests": len(contest_map.values()),
        }

        data = {
            'lineups': self.serializer_class(list(lineup_map.values()), many=True).data,
            'overall': overall,
        }

        return data

    def get(self, request, year, month, day, format=None):
        """

        """
        data = self.get_history_data(year, month, day)
        return Response(data, status=status.HTTP_200_OK)


class UserPlayHistoryWithCurrentAPIView(UserPlayHistoryAPIView):
    """
    inherits UserPlayHistoryAPIView for the get_history_data() method.

    get the entry history & the Current lineups for a user on a day.
    """

    def get_current_data(self):
        """
        get the Current lineup data
        """

        # get a list of the lineups in live entries for the day
        current_entries = CurrentEntry.objects.filter(user=self.request.user)

        # TODO below
        payouts = Payout.objects.filter(entry__in=current_entries)
        # distinct_lineup_ids = [e.lineup.pk for e in current_entries]
        lineup_map = {}
        for entry in current_entries:
            lineup_map[entry.lineup.pk] = entry.lineup

        #
        # sum the values for each lineup (and all its entries for paid contests)
        total_buyins = 0
        num_entries = 0
        winnings = 0
        possible = 0
        contest_map = {}
        for lineup in list(lineup_map.values()):  # for each distinct lineup
            for current_entry in current_entries.filter(lineup=lineup):
                if current_entry.contest is None:
                    # this means the lineup is not yet live. skip it.
                    continue
                total_buyins += current_entry.contest.buyin
                num_entries += 1
                try:
                    winnings += payouts.get(entry=current_entry).amount
                except Payout.DoesNotExist:
                    pass

                possible += current_entry.contest.prize_structure.generator.first_place
                contest_map[current_entry.contest.pk] = current_entry.contest

        overall = {
            "buyins": '%.2f' % total_buyins,
            "entries": num_entries,
            "winnings": '%.2f' % winnings,
            "possible": '%.2f' % possible,
            "contests": len(contest_map.values()),
        }

        data = {
            'lineups': self.serializer_class(list(lineup_map.values()), many=True).data,
            'overall': overall,
        }

        return data

    def get(self, request, year, month, day, format=None):
        """
        Given the 'task' parameter, return the status of the task (ie: the buyin)

        :param request:
        :param format:
        :return:
        """

        # build the historical lineup data
        history_data = self.get_history_data(year, month, day)

        # build the data for any lineups that are currently live
        current_data = self.get_current_data()

        # pack it into this dict and return it
        data = {
            'history': history_data,
            'current': current_data,
        }

        # return http response with the data
        return Response(data, status=status.HTTP_200_OK)
