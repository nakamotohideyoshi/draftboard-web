from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Ticket, TicketAmount
from .serializers import TicketSerializer
from .classes import TicketManager
class TicketAvailableListAPIView(generics.GenericAPIView):
    """
    Gets the cash balance as a string for the logged in user formatted like '$5.50'.

        * |api-text| :dfs:`cash/balance/`


    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = TicketSerializer
    def get(self, request, format=None):

        user = self.request.user
        tm = TicketManager(user)
        tickets = tm.get_available_tickets()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

