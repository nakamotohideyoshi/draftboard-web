#
# lineup/views.py

from django.core.cache import caches
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import LimitOffsetPagination

from lineup.serializers import LineupSerializer, PlayerSerializer, \
                                CreateLineupSerializer, EditLineupSerializer
from lineup.models import Lineup, Player
from lineup.classes import LineupManager
from lineup.tasks import edit_lineup, edit_entry
from lineup.exceptions import CreateLineupExpiredDraftgroupException, InvalidLineupSizeException, \
                                LineupInvalidRosterSpotException, PlayerDoesNotExistInDraftGroupException
from draftgroup.models import DraftGroup
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

class CreateLineupAPIView(generics.CreateAPIView):
    """
    create a new lineup
    """
    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = CreateLineupSerializer

    def post(self, request, format=None):
        #print( request.data )
        draft_group_id  = request.data.get('draft_group')
        players         = request.data.get('players', [])

        # the draft_group_id has been validated by the serializer
        draft_group = DraftGroup.objects.get(pk=draft_group_id)

        #
        # call task
        lm = LineupManager( request.user )
        try:
            lineup = lm.create_lineup( players, draft_group )
        except CreateLineupExpiredDraftgroupException:
            return Response(
                'You can no longer create lineups for this draft group',
                status=status.HTTP_403_FORBIDDEN
            )
        except InvalidLineupSizeException:
            return Response(
                'You have not drafted enough players.',
                status=status.HTTP_403_FORBIDDEN
            )
        except LineupInvalidRosterSpotException:
            return Response(
                'One or more of the players are invalid for the roster.',
                status=status.HTTP_403_FORBIDDEN
            )
        except PlayerDoesNotExistInDraftGroupException as e:
            return Response(
                str(e),
                status=status.HTTP_403_FORBIDDEN
            )

        # on successful lineup creation:
        return Response('Lineup created.', status=status.HTTP_201_CREATED)

class EditLineupAPIView(generics.CreateAPIView):
    """
    edit an existing lineup
    """
    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = EditLineupSerializer

    def post(self, request, format=None):
        #print( request.data )
        lineup_id   = request.data.get('lineup')
        players     = request.data.get('players', [])

        #
        # call task
        task_result = edit_lineup.delay()

        return Response('lineup created')

class PlayersAPIView(generics.GenericAPIView):
    """
    get the lineup Players
    """
    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = PlayerSerializer

    def get_object(self, id):
        return Player.objects.filter(lineup__id=id)

    def get(self, request, pk, format=None):
        """
        get the lineup along with its players
        """
        serialized_data = PlayerSerializer( self.get_object(pk), many=True ).data
        return Response(serialized_data)

class AbstractLineupAPIView(generics.ListAPIView):
    """
    Abstract class.
    """
    lineup_model            = None

    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = LineupSerializer

    def get_queryset(self):
        """

        """
        return [] # TODO

class UserUpcomingAPIView(AbstractLineupAPIView):
    """
    Get the User's upcoming lineups which are before the draft group start time
    """

    lineup_model = Lineup

    def get_queryset(self):
        """
        get the Lineup objects
        """
        return Lineup.objects.filter( user=self.request.user,
                                      draft_group__start__gt=timezone.now() )

class UserLiveAPIView(AbstractLineupAPIView):
    """
    Get the User's lineups that are after the draft group start time, and within 12 hours of the end time
    """

    lineup_model = Lineup

    def get_queryset(self):
        """
        retrieve the Lineup objects
        """
        offset_hours = 12
        now = timezone.now()
        dt = now - timedelta(hours=offset_hours)
        #print('now', str(now), 'dt', str(dt))
        return Lineup.objects.filter( user=self.request.user,
                                      draft_group__start__lte=now,
                                      draft_group__end__gt=dt )

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
        #print(str(dt))
        return Lineup.objects.filter( user=self.request.user,
                                      draft_group__end__lte=dt )
