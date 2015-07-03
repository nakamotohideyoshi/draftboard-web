#
# lineup/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import LimitOffsetPagination

from lineup.serializers import LineupSerializer
from lineup.models import Lineup

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

    lineup_model = None # TODO

    def get_queryset(self):
        """

        """
        return [] # TODO

class UserLiveAPIView(AbstractLineupAPIView):
    """
    TODO/unimplemented - Get the live lineups for the authenticated user
    """

    lineup_model = None # TODO

    def get_queryset(self):
        """

        """
        return [] # TODO

class UserHistoryAPIView(AbstractLineupAPIView):
    """
    TODO/unimplemented - Get the historical lineups for the authenticated user
    """

    lineup_model = None # TODO

    def get_queryset(self):
        """

        """
        return [] # TODO