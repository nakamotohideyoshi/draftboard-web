from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from cash.models import CashTransactionDetail
from cash.serializers import CashTransactionDetailSerializer
from datetime import datetime, timedelta
from cash.classes import CashTransaction
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

class TransactionHistoryAPIView(generics.ListAPIView):
    """
    Allows the logged in user to get their transaction history

        * |api-text| :dfs:`cash/history/`

        .. note::

            A get parameter of **?days=X** can be used. This argument
            describes how many days of history from today to get. If
            it is not set, by default it will return the max which is 30.
            If anything greater than 30 is set, it will return the 30 days.

    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CashTransactionDetailSerializer

    def get_queryset(self):
        """
        Gets the filtered Cash Transaction Details for the logged in user.


        """
        days = self.request.QUERY_PARAMS.get('days', None)
        if(days == None):
            days = 30
        else:
            days = int(days)
        if(days > 30):
            days = 30

        user = self.request.user
        now = datetime.now()
        days_ago = now - timedelta(days=days)

        return CashTransactionDetail.objects.filter(user=user, created__range=(days_ago, now))


class BalanceAPIView(generics.GenericAPIView):
    """
    Gets the cash balance as a string for the logged in user formatted like '$5.50'.

        * |api-text| :dfs:`cash/balance/`


    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        user = self.request.user
        cash_transaction = CashTransaction(user)
        content = {'cash_balance': cash_transaction.get_balance_string_formatted()}
        return Response(content)

