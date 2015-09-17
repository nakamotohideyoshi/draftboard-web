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
    TODO/unimplemented - Get the upcoming lineups for the authenticated user
    """

    lineup_model = Lineup

    def get_queryset(self):
        """

        """
        return Lineup.objects.all() # TODO - just get upcoming

class UserLiveAPIView(AbstractLineupAPIView):
    """
    TODO/unimplemented - Get the live lineups for the authenticated user
    """

    lineup_model = Lineup

    def get_queryset(self):
        """

        """
        return Lineup.objects.all() # TODO - just get upcoming

class UserHistoryAPIView(AbstractLineupAPIView):
    """
    TODO/unimplemented - Get the historical lineups for the authenticated user
    """

    lineup_model = Lineup

    def get_queryset(self):
        """

        """
        return Lineup.objects.all() # TODO - just get upcoming
