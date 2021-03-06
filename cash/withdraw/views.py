import json
from logging import getLogger

from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.gidx.models import GidxSession
from account.gidx.request import WebCashierCreatePayoutSession
from account.gidx.request import (
    get_user_from_session_id,
    get_customer_id_for_user,
    make_web_cashier_payment_detail_request,
)
from account.gidx.response import (
    GidxTransactionStatusWebhookResponse
)
from account.permissions import (HasIpAccess, HasVerifiedIdentity)
from account.utils import (get_client_ip)
from cash.classes import CashTransaction
from cash.models import GidxTransaction

logger = getLogger('cash.withdraw.views')


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


class GidxWithdrawFormAPIView(APIView):
    """
    Fetch + return a withdrawal drop-in form from GIDX
    """

    permission_classes = (IsAuthenticated, HasIpAccess, HasVerifiedIdentity)

    @staticmethod
    def get(request, amount):
        # first make sure it's a float.
        try:
            amount = float(amount)
        except ValueError:
            return Response(
                data={
                    "status": "FAIL",
                    "detail": "Please enter a valid USD amount",
                },
                status=400,
            )

        # Enforce minimum withdraw amount.
        if float(amount) < 5:
            return Response(
                data={
                    "status": "FAIL",
                    "detail": "Minimum withdraw amount is $5.00.",
                },
                status=400,
            )

        # Ensure the user has the funds available for withdrawal.
        ct = CashTransaction(request.user)
        has_funds = ct.check_sufficient_funds(float(amount))

        if not has_funds:
            return Response(
                data={
                    "status": "FAIL",
                    "detail": "You do not have the funds to cover this withdrawal amount.",
                    "reasonCodes": [],
                },
                status=400,
            )

        web_cashier = WebCashierCreatePayoutSession(
            ip_address=get_client_ip(request),
            user=request.user,
            amount=amount
        )

        # Make the request.
        web_cashier_response = web_cashier.send()
        message = web_cashier_response.get_response_message()

        # If we didn't receive a JS embed...
        if not message:
            return Response(
                data={
                    "status": "FAIL",
                    "detail": "We were unable to initiate the withdraw process.",
                    "reasonCodes": web_cashier_response.get_reason_codes(),
                },
                status=400,
            )

        return Response(
            data={
                "status": "SUCCESS",
                "detail": message,
                "reasonCodes": web_cashier_response.get_reason_codes(),
            },
            status=200,
        )


class GidxWithdrawSessionComplete(APIView):
    """
    When a user has sucessfully completed the JS drop-in form withdraw session, the client
    hits this endpoint with a merchant_session_id, we look up that session and create a withdraw
    for the appropriate amount.

    This is so we can get instantaneous withdraws. Without it, there is a 10-30 second
    delay between a user requesting a withdraw, and us reducing thier balance, which is ripe
    for abuse.
    """
    permission_classes = (IsAuthenticated, HasIpAccess, HasVerifiedIdentity)

    @staticmethod
    def post(request):
        merchant_session_id = request.data.get('session_id')

        if merchant_session_id is None:
            return Response(
                data={"detail": "Session ID is missing"},
                status=400,
            )

        # get the merchant session entry that initiated this session.
        gidx_session = GidxSession.objects.get(
            session_id=merchant_session_id,
            service_type='WebCashier_CreateSession'
        )
        session_data = gidx_session.request_data

        # Check that they are the correct user for this session
        if not gidx_session.user == request.user:
            raise PermissionDenied(detail='Requesting user does not own this session.')

        if not session_data.get('PayActionCode') == 'PAYOUT':
            logger.error(
                'Attempated to GidxWithdrawSessionComplete a session that is not a '
                'PAYOUT: session %s' % gidx_session)
            return Response(
                data={"detail": ":("},
                status=400,
            )

        # Make sure we can determine the amount of the withdrawal
        amount = session_data.get('CashierPaymentAmount', {}).get('PaymentAmount')

        if not amount:
            logger.error(
                'Attempated to GidxWithdrawSessionComplete a session that has no '
                'amount: session %s' % gidx_session)
            return Response(
                data={"detail": ":/"},
                status=400,
            )

        # Ensure there is not an exiting cash transaction for this transaction.
        merchant_transaction_id = session_data.get('MerchantTransactionID')
        existing_transaction = GidxTransaction.objects.filter(
            merchant_transaction_id=merchant_transaction_id)

        if existing_transaction.count() > 0:
            logger.error(
                'Attempated to GidxWithdrawSessionComplete a session that has an existing '
                'transaction!: session %s | merchant_transaction_id' % (
                    gidx_session, merchant_transaction_id))
            return Response(
                data={"detail": ">:"},
                status=400,
            )

        # ok, so we know that the session we have is a valid withdraw that does not already
        # have a transaction associated with it. This means we can initiate a withdraw.
        trans = CashTransaction(request.user)
        trans.withdraw_gidx(float(amount), merchant_transaction_id)

        # As long as nothing errors out, send a 200 back to the browser.
        return Response(
            data={
                "detail": "cool."
            },
            status=200,
        )


class GidxWithdrawCallbackAPIView(APIView):
    """
    Note: this very similar to GidxDepositCallbackAPIView -- maybe these can be merged?

    When a user withdraws money, we embed a gidx-provided form. When the form is submitted and
    the transaction processed, we will get a request to this endpoint with info about
    the transaction.
    """

    parser_classes = (MultiPartParser, FormParser,)

    @staticmethod
    @csrf_exempt
    def post(request):
        request_data = json.loads(request.data.dict()['result'])

        logger.info({
            "action": "WebCashier_Withdraw_Callback",
            "request": None,
            "response": request_data,
        })

        response_wrapper = GidxTransactionStatusWebhookResponse(request_data)
        # Grab some of the data from the previous session that is not included in the webhook.
        user = get_user_from_session_id(response_wrapper.json['MerchantSessionID'])
        customer_id = get_customer_id_for_user(user)

        # Save our session info
        GidxSession.objects.create(
            user=user,
            gidx_customer_id=customer_id,
            session_id=response_wrapper.json['MerchantSessionID'],
            service_type='WebCashier_Withdraw_Callback',
            reason_codes=response_wrapper.json['ReasonCodes'],
            response_data=request_data,
        )

        # If the webhook says that the transaction has completed (good or bad), we need to fetch
        # the payment details in order to proceed.
        if response_wrapper.is_done():
            payment_detail = make_web_cashier_payment_detail_request.delay(
                user=user,
                transaction_id=response_wrapper.json['MerchantTransactionID'],
                session_id=response_wrapper.json['MerchantSessionID']
            )
        else:
            logger.warning('Transaction pending or failed: %s' % response_wrapper.json)

        # As long as nothing errors out, send a 200 back to gidx.
        return Response(
            data={
                "status": "SUCCESS",
                "detail": "cool, thanks!"
            },
            status=200,
        )
