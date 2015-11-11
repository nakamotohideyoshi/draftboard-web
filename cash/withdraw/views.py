#
# cash/withdraw/views.py

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from cash.withdraw.serializers import CheckWithdrawSerializer, PayPalWithdrawSerializer

from cash.withdraw.classes import CheckWithdraw, PayPalWithdraw

class CheckWithdrawAPIView(generics.CreateAPIView):
    """
    api for user to submit a withdraw request
    """

    permission_classes  = (IsAuthenticated,)
    serializer_class    = CheckWithdrawSerializer

    def post(self, request, format=None):
        #print( request.data )
        amount = request.data.get('amount')

        withdraw = CheckWithdraw(request.user)
        withdraw.withdraw( amount )

        # except Exception:
        #     return Response( 'Error', status=status.HTTP_403_FORBIDDEN )

        # on successful lineup creation:
        return Response('Withdraw request submitted for approval.', status=status.HTTP_201_CREATED)