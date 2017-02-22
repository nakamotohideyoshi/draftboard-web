#
# lineup/views.py

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    APIException,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from lineup.serializers import (
    LineupSerializer,
    PlayerSerializer,
    CreateLineupSerializer,
    EditLineupSerializer,
    LineupIdSerializer,
    LineupUsernamesSerializer,
    EditLineupStatusSerializer,
    LineupCurrentSerializer,
)
from lineup.models import Lineup, Player
from lineup.classes import LineupManager
from lineup.tasks import edit_lineup
from lineup.exceptions import (
    CreateLineupExpiredDraftgroupException,
    InvalidLineupSizeException,
    LineupInvalidRosterSpotException,
    PlayerDoesNotExistInDraftGroupException,
    InvalidLineupSalaryException,
    NotEnoughTeamsException,
)
from draftgroup.models import DraftGroup
from django.utils import timezone
from datetime import timedelta
from mysite.celery_app import TaskHelper
from account.permissions import (
    HasIpAccess,
    HasVerifiedIdentity,
    EmailConfirmed,
)
from account import const as _account_const
from account.utils import create_user_log


class CreateLineupAPIView(generics.CreateAPIView):
    """
    create a new lineup
    """
    permission_classes = (IsAuthenticated, HasIpAccess, HasVerifiedIdentity, EmailConfirmed)
    serializer_class = CreateLineupSerializer

    def post(self, request, format=None):
        draft_group_id = request.data.get('draft_group')
        players = request.data.get('players', [])
        name = request.data.get('name', '')

        user_lineups = Lineup.objects.filter(user=request.user, draft_group_id=draft_group_id).values_list('name', flat=True)
        if name and name in user_lineups:
            raise ValidationError(
                {'detail': 'You already have lineup with this name.'})

        # the draft_group_id has been validated by the serializer
        try:
            draft_group = DraftGroup.objects.get(pk=draft_group_id)
        except DraftGroup.DoesNotExist:
            raise ValidationError({'detail': 'Draft group does not exist.'})

        #
        # use the lineup manager to create the lineup
        try:
            lm = LineupManager(request.user)
        except:
            raise APIException('Invalid user')

        try:
            lineup = lm.create_lineup(players, draft_group, name)

        except NotEnoughTeamsException:
            raise ValidationError(
                {'detail': 'Lineup must include players from at least three different teams'})

        except InvalidLineupSalaryException:
            raise ValidationError({'detail': 'Lineup exceeds max salary'})

        except CreateLineupExpiredDraftgroupException:
            raise ValidationError(
                {'detail': 'You can no longer create lineups for this draft group'})

        except InvalidLineupSizeException:
            raise ValidationError({'detail': 'You have not drafted enough players'})

        except LineupInvalidRosterSpotException:
            raise ValidationError(
                {'detail': 'One or more of the players are invalid for the roster'})

        except PlayerDoesNotExistInDraftGroupException:
            raise ValidationError(
                {'detail': 'Player is not contained in the list of draftable players'})

        except Exception as e:
            raise APIException(e)

        create_user_log(
            request=request,
            type=_account_const.CONTEST,
            action=_account_const.LINEUP_CREATED,
            metadata={
                'detail': 'Lineup was created.',
                'lineup_id': lineup.id,
                'players': players,
            }
        )

        # On successful lineup creation:
        return Response({
            'detail': 'Lineup created.',
            'lineup_id': lineup.id

        }, status=status.HTTP_201_CREATED)


class LineupUserAPIView(APIView):
    """
    Get the usernames for lineups by providing a list of lineup ids.
        OR
    Get the lineups for a given contest by providing a valid contest_id and search string
        OR
    Get the lineups for a given contest by providing a valid contest_id

    The 'lineup_ids' parameter overrides the lookup by name. (ie: if all parameters
        are specified, we will return data for the specified lineup_ids list)

    POST params:

        (Required)
        contest_id      :  the contest id to search for lineups in

        (Use lineup_ids OR search_str)
        lineup_ids      : list of lineup ids, ie: [123, 432, 5234]
            ... OR ...
        search_str      : the search string for the lineup name (lineup names are based on username)
            ... OR ...
        nothing and it will default ot using just the contest_id

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LineupUsernamesSerializer

    def get_serialized_lineups(self, lineups=[]):
        data = []
        for l in lineups:
            data.append(LineupIdSerializer(l).data)
        return data

    def post(self, request, *args, **kwargs):
        """
        get the Lineup objects
        """
        args = request.data

        # get the contest_id post param - it is required
        contest_id = args.get('contest_id', None)

        # get the lineup_ids or the search_str
        lineup_ids = args.get('lineup_ids', [])
        search_str = args.get('search_str', None)

        # return Response({}, status=status.HTTP_200_OK)
        # return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        if contest_id is None:
            msg = 'The POST param "contest_id" is required along with either: "lineup_ids", "search_str"'
            raise ValidationError(msg)

        lm = LineupManager(self.request.user)

        if lineup_ids:
            #
            # return the lineup usernames for the lineups with the ids, in the particular contest
            # return lm.get_for_contest_by_ids( contest_id, lineup_ids)
            lineups = lm.get_for_contest_by_ids(contest_id, lineup_ids)
            serialized_lineup_data = self.get_serialized_lineups(lineups)
            return Response(serialized_lineup_data, status=status.HTTP_200_OK)

        elif search_str:
            #
            # get the distinct lineups in this contest where the lineup_id matches
            # return lm.get_for_contest_by_search_str(contest_id, search_str)
            lineups = lm.get_for_contest_by_search_str(contest_id, search_str)
            serialized_lineup_data = self.get_serialized_lineups(lineups)
            return Response(serialized_lineup_data, status=status.HTTP_200_OK)
        else:
            lineups = lm.get_for_contest(contest_id)
            serialized_lineup_data = self.get_serialized_lineups(lineups)
            return Response(serialized_lineup_data, status=status.HTTP_200_OK)


class EditLineupAPIView(generics.CreateAPIView):
    """
    edit an existing lineup
    """
    permission_classes = (IsAuthenticated, HasIpAccess, HasVerifiedIdentity, EmailConfirmed)
    serializer_class = EditLineupSerializer

    def post(self, request, format=None):
        lineup_id = request.data.get('lineup')
        players = request.data.get('players', [])
        name = request.data.get('name', '')

        # validate the parameters passed in here.
        if players is None:
            raise ValidationError(
                {'detail': 'You must supply the "players" parameter -- the list of player ids.'})

        if lineup_id is None:
            raise ValidationError(
                {'detail': 'You must supply the "lineup_id" parameter -- the Lineup id.'})
        try:
            lineup = Lineup.objects.get(pk=lineup_id, user=request.user)
        except Lineup.DoesNotExist:
            raise ValidationError({'detail': 'Lineup id does not exist.'})
        #
        # change the lineups name if it differs from the existing name
        if lineup.name != name:
            user_lineups = Lineup.objects.filter(user=request.user, draft_group_id=lineup.draft_group_id).values_list('name', flat=True)
            if name in user_lineups:
                raise ValidationError(
                    {'detail': 'You already have lineup with this name.'})
            lineup.name = name
            lineup.save()

        #
        # call task
        # we could call the same task like this, fwiw:
        # >>> task_result = edit_lineup.apply_async(args=(request.user, players, lineup))
        task_result = edit_lineup.delay(request.user, players, lineup)
        # get() blocks the view from returning until the task finishes
        task_result.get()
        task_helper = TaskHelper(edit_lineup, task_result.id)

        create_user_log(
            request=request,
            type=_account_const.CONTEST,
            action=_account_const.LINEUP_EDIT,
            metadata={
                'detail': 'Lineup was edited.',
                'lineup_id': lineup.id,
                'players': players
            }
        )
        return Response(task_helper.get_data(), status=status.HTTP_200_OK)


class EditLineupStatusAPIView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = EditLineupStatusSerializer

    def get(self, request, task_id, format=None):
        """
        Given the 'task' parameter, return the status of the task (ie: from performing the
        edit-entry)

        :param request:
        :param format:
        :return:
        """
        task_helper = TaskHelper(edit_lineup, task_id)
        return Response(task_helper.get_data(), status=status.HTTP_200_OK)


class PlayersAPIView(generics.GenericAPIView):
    """
    get the lineup Players
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayerSerializer

    def get_object(self, id):
        return Player.objects.filter(lineup__id=id)

    def get(self, request, pk, format=None):
        """
        get the lineup along with its players
        """
        serialized_data = PlayerSerializer(self.get_object(pk), many=True).data
        return Response(serialized_data)


class AbstractLineupAPIView(generics.ListAPIView):
    """
    Abstract class.
    """
    lineup_model = None

    permission_classes = (IsAuthenticated,)
    serializer_class = LineupSerializer

    def get_queryset(self):
        """

        """
        return []  # TODO


class UserCurrentAPIView(AbstractLineupAPIView):
    """
    Get the User's upcoming lineups which are before the draft group start time
    """

    lineup_model = Lineup

    serializer_class = LineupCurrentSerializer

    def get_queryset(self):
        """
        get live/upcoming lineups
        """
        return Lineup.objects.filter(
            user=self.request.user,
            draft_group__end__gt=timezone.now()
        ).exclude(
            entries__contest_pool=None
        ).order_by(
            'draft_group__start'
        ).select_related(
            'draft_group'
        ).prefetch_related(
            'entries'
        ).distinct()


class UserUpcomingAPIView(AbstractLineupAPIView):
    """
    Get the User's upcoming lineups which are before the draft group start time
    """

    lineup_model = Lineup

    def get_queryset(self):
        """
        get the Lineup objects
        """
        return Lineup.objects.filter(
            user=self.request.user,
            draft_group__start__gt=timezone.now()
        ).order_by('-updated')


class UserLiveAPIView(AbstractLineupAPIView):
    """
    Get the User's lineups that are after the draft group start time, and within 12 hours of the
    end time
    """

    lineup_model = Lineup

    def get_queryset(self):
        """
        retrieve the Lineup objects
        """
        offset_hours = 12
        now = timezone.now()
        dt = now - timedelta(hours=offset_hours)
        return Lineup.objects.filter(user=self.request.user,
                                     draft_group__start__lte=now,
                                     draft_group__end__gt=dt)


class UserHistoryAPIView(AbstractLineupAPIView):
    """
    Get a User's lineups that are within 12 hours of the draft group's end datetime
    """

    lineup_model = Lineup

    def get_queryset(self):
        """
        retrieve the Lineup objects
        """
        offset_hours = 12
        now = timezone.now()
        dt = now - timedelta(hours=offset_hours)
        return Lineup.objects.filter(user=self.request.user, draft_group__end__lte=dt)
