#
# views.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from cash.withdraw.serializers import PayPalWithdrawSerializer
from cash.withdraw.classes import PayPalWithdraw
from mysite.exceptions import (
    MaxCurrentWithdrawsException,
    CashoutWithdrawOutOfRangeException,
)
from account.permissions import (HasIpAccess, HasVerifiedIdentity)
from account import const as _account_const
from account.utils import create_user_log


# class CheckWithdrawAPIView(generics.CreateAPIView):
#     """
#     api for user to submit a withdraw request
#     """
#
#     permission_classes = (IsAuthenticated, HasIpAccess,)
#     serializer_class = CheckWithdrawSerializer
#
#     def post(self, request, *args, **kwargs):
#         amount = request.data.get('amount')
#
#         withdraw = CheckWithdraw(request.user)
#         withdraw.withdraw(amount)
#
#         # except Exception:
#         #     return Response( 'Error', status=status.HTTP_403_FORBIDDEN )
#
#         create_user_log(
#             request=request,
#             type=_account_const.FUNDS,
#             action=_account_const.WITHDRAWAL_CHECK,
#             metadata={
#                 'detail': 'Funds withdrawal via check requested.',
#                 'amount': amount
#             }
#         )
#
#         # on successful lineup creation:
#         return Response({'message': 'Withdraw request submitted for approval.'}, status=200)


class PayPalWithdrawAPIView(APIView):
    """
    api for user to submit a withdraw request via a paypal payout

    example json to POST to this api:

        >>> {"amount":20.00,"email":"valid@email.com"}

    """

    permission_classes = (IsAuthenticated, HasIpAccess, HasVerifiedIdentity)
    serializer_class = PayPalWithdrawSerializer

    def post(self, request, *args, **kwargs):
        # raise validation errors if there are any
        self.serializer_class(data=self.request.data).is_valid(raise_exception=True)

        user = self.request.user
        amount = self.request.data.get('amount')
        email = self.request.data.get('email')

        try:
            withdraw = PayPalWithdraw(user)
            withdraw.set_paypal_email(email)
            withdraw.withdraw(amount)
        except MaxCurrentWithdrawsException:
            return Response(
                'Withdraw request declined. You currently have the maximum outstanding requests.',
                status=status.HTTP_400_BAD_REQUEST)
        except CashoutWithdrawOutOfRangeException:
            raise serializers.ValidationError({'amount': ['Cashout amount is out of range.']})

        create_user_log(
            request=request,
            type=_account_const.FUNDS,
            action=_account_const.WITHDRAWAL_PAYPAL,
            metadata={
                'detail': 'Funds withdrawal via PayPal requested.',
                'amount': amount,
                'email': email,
            }
        )

        # on successful lineup creation:
        return Response({'message': 'Withdraw request submitted for approval.'}, status=200)
