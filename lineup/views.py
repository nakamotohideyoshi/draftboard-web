from datetime import timedelta
from logging import getLogger

from django.utils import timezone
from raven.contrib.django.raven_compat.models import client
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    APIException,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account import const as _account_const
from account.permissions import (
    HasIpAccess,
    HasVerifiedIdentity,
)
from account.utils import create_user_log
from draftgroup.models import DraftGroup
from lineup.classes import LineupManager
from lineup.exceptions import (
    LineupDoesNotMatchUser,
    NotEnoughTeamsException,
    LineupDoesNotMatchExistingEntryLineup,
    InvalidLineupSizeException,
    InvalidLineupSalaryException,
    LineupInvalidRosterSpotException,
    PlayerDoesNotExistInDraftGroupException,
    DuplicatePlayerException,
    PlayerSwapGameStartedException,
    EditLineupInProgressException,
    LineupUnchangedException,
    CreateLineupExpiredDraftgroupException,
    DraftgroupLineupLimitExceeded,
)
from lineup.models import Lineup, Player
from lineup.serializers import (
    LineupSerializer,
    PlayerSerializer,
    CreateLineupSerializer,
    EditLineupSerializer,
    LineupIdSerializer,
    LineupUsernamesSerializer,
    EditLineupStatusSerializer,
    LineupCurrentSerializer,
    LineupLiveSerializer,
)
from lineup.tasks import edit_lineup
from mysite.celery_app import TaskHelper

logger = getLogger('lineup/views')


class CreateLineupAPIView(generics.CreateAPIView):
    """
    create a new lineup
    """
    permission_classes = (IsAuthenticated, HasIpAccess, HasVerifiedIdentity)
    serializer_class = CreateLineupSerializer

    def post(self, request):
        draft_group_id = request.data.get('draft_group')
        players = request.data.get('players', [])
        name = request.data.get('name', '')

        user_lineups = Lineup.objects.filter(user=request.user,
                                             draft_group_id=draft_group_id).values_list('name',
                                                                                        flat=True)
        if name and name in user_lineups:
            raise ValidationError(
                {'detail': 'You already have lineup with this name.'})

        # the draft_group_id has been validated by the serializer
        try:
            draft_group = DraftGroup.objects.get(pk=draft_group_id)
        except DraftGroup.DoesNotExist:
            raise ValidationError({'detail': 'Draft group does not exist.'})

        # use the lineup manager to create the lineup
        try:
            lm = LineupManager(request.user)
        except:
            raise APIException('Invalid user')

        # Attempt to create the lineup.
        try:
            lineup = lm.create_lineup(players, draft_group, name)
        # Catch all of the lineupManager exceptions and return validation errors.
        except (
                LineupDoesNotMatchUser,
                NotEnoughTeamsException,
                LineupDoesNotMatchExistingEntryLineup,
                InvalidLineupSizeException,
                InvalidLineupSalaryException,
                LineupInvalidRosterSpotException,
                PlayerDoesNotExistInDraftGroupException,
                DuplicatePlayerException,
                PlayerSwapGameStartedException,
                EditLineupInProgressException,
                LineupUnchangedException,
                CreateLineupExpiredDraftgroupException,
                DraftgroupLineupLimitExceeded,
        ) as e:
            logger.warning("%s | user: %s" % (e, self.request.user))
            raise ValidationError({'detail': e})
        # Catch everything else and log.
        except Exception as e:
            logger.error(e)
            client.captureException()
            raise APIException({'detail': 'Unable to save lineup.'})

        # Log event to user log
        create_user_log(
            request=request,
            user=request.user,
            type=_account_const.CONTEST,
            action=_account_const.LINEUP_CREATED,
            metadata={
                'detail': 'Lineup was created.',
                'lineup_id': lineup.id,
                'players': players,
            }
        )

        # Serialize the lineup and send it back to the client.
        saved_lineup = LineupSerializer(lineup)
        # On successful lineup creation:
        return Response({
            'detail': 'Lineup created.',
            'lineup_id': lineup.id,
            'lineup': saved_lineup.data,
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
            msg = (
                'The POST param "contest_id" is required along with either: "lineup_ids",'
                '"search_str"')
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
    permission_classes = (IsAuthenticated, HasIpAccess, HasVerifiedIdentity)
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

        # Make sure the lineup exists.
        try:
            lineup = Lineup.objects.get(pk=lineup_id, user=request.user)
        except Lineup.DoesNotExist:
            raise ValidationError({'detail': 'Lineup id does not exist.'})

        # change the lineups name if it differs from the existing name
        if lineup.name != name:
            user_lineups = Lineup.objects.filter(user=request.user,
                                                 draft_group_id=lineup.draft_group_id).values_list(
                'name', flat=True)
            if name in user_lineups:
                raise ValidationError(
                    {'detail': 'You already have lineup with this name.'})
            lineup.name = name
            lineup.save()

        # Attempt to edit the lineup.
        try:
            edit_lineup(request.user, players, lineup)
        # Various lineup editing/saving exceptions will be thrown above. (due to salary restrictions
        # or contests being full or stuff like that)
        except (
                LineupDoesNotMatchUser,
                NotEnoughTeamsException,
                LineupDoesNotMatchExistingEntryLineup,
                InvalidLineupSizeException,
                InvalidLineupSalaryException,
                LineupInvalidRosterSpotException,
                PlayerDoesNotExistInDraftGroupException,
                DuplicatePlayerException,
                PlayerSwapGameStartedException,
                EditLineupInProgressException,
                LineupUnchangedException,
                CreateLineupExpiredDraftgroupException,
        ) as e:
            logger.error("%s | user: %s" % (e, self.request.user))
            raise ValidationError({'detail': e})
        except Exception as e:
            logger.error("%s | user: %s" % (e, self.request.user))
            client.captureException()
            raise APIException({'detail': 'Unable to save lineup.'})

        # Log this edit action to the user's log.
        create_user_log(
            request=request,
            type=_account_const.CONTEST,
            action=_account_const.LINEUP_EDIT,
            user=request.user,
            metadata={
                'detail': 'Lineup was edited.',
                'lineup_id': lineup.id,
                'players': players
            }
        )

        saved_lineup = LineupSerializer(lineup)
        # If successful, return the lineup to the client.
        return Response({
            'detail': 'Lineup Saved.',
            'lineup': saved_lineup.data
        }, status=status.HTTP_200_OK)


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
    Get the User's currently live lineups.
    """

    lineup_model = Lineup

    serializer_class = LineupCurrentSerializer

    def get_queryset(self):
        """
        get live/upcoming lineups
        """
        return Lineup.objects.filter(
            user=self.request.user,
            draft_group__closed=None
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
        ).order_by(
            '-updated'
        ).prefetch_related(
            'players__draft_group_player__salary_player'
        )


class UserLiveAPIView(AbstractLineupAPIView):
    """
    Get the User's lineups that are after the draft group start time, and within 12 hours of the
    end time.

    This is similar to the UserCurrentAPIView, except it keeps lineups around for longer. And it
    has players embeded in each lineup.
    It's used by the mobile app so that they are viewable the next day after contests are over.
    """

    lineup_model = Lineup
    serializer_class = LineupLiveSerializer

    def get_queryset(self):
        """
        retrieve the Lineup objects
        """
        offset_hours = 24
        now = timezone.now()
        dt = now - timedelta(hours=offset_hours)
        return Lineup.objects.filter(
            user=self.request.user,
            draft_group__start__lte=now,
            draft_group__end__gt=dt
        ).exclude(
            entries__contest_pool=None
        ).order_by(
            'draft_group__start'
        ).select_related(
            'draft_group', 'user'
        ).prefetch_related(
            'entries', 'players'
        ).distinct()


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
