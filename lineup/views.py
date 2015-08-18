#
# lineup/views.py

from django.core.cache import caches
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import LimitOffsetPagination

from lineup.serializers import LineupSerializer, PlayerSerializer
from lineup.models import Lineup, Player

class PlayersAPIView(generics.GenericAPIView):
    """
    get the lineup Players
    """
    authentication_classes  = (SessionAuthentication, BasicAuthentication)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = PlayerSerializer

    def get_object(self, id):
        return Player.objects.filter(lineup__id=id)

    def get(self, request, format=None):
        """
        get the lineup along with its players
        """
        pk = self.request.GET.get('id')

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