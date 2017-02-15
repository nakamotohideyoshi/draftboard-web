#
# cash/views.py

from time import time
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from cash.models import CashTransactionDetail
from cash.serializers import TransactionHistorySerializer, BalanceSerializer
from datetime import datetime, timedelta
from cash.classes import CashTransaction
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from django.views.generic.edit import FormView
import braintree
from django.conf import settings
from braces.views import LoginRequiredMixin
from cash.forms import DepositAmountForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from cash.classes import CashTransaction
from transaction.models import Transaction

class TransactionHistoryAPIView(generics.GenericAPIView):
    """
    Allows the logged in user to get their transaction history

        * |api-text| :dfs:`cash/transactions/`

        .. note::

            A get parameter of **?start_ts=X&end_ts=Y** can be used. This argument
            describes how many days of history from today to get. If
            it is not set, by default it will return the max which is 30.
            If anything greater than 30 is set, it will return the 30 days.
    """

    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionHistorySerializer

    def get_queryset(self, *args, **kwargs):
        return Transaction

    def get_user_for_id(self, user_id=None):
        """
        if a user can be found via the 'user_id' return it,
        else return None.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, user_id=None, format=None):
        """
        Gets the filtered Cash Transaction Details for the logged in user.

        If the admin calls this api and ALSO specifies a 'user_id' get PARAM
        then the transactions for that user is displayed.
        """
        # If no start was provided, use 30 days ago as default.
        start_ts = self.request.query_params.get('start_ts', int(time()) - 60 * 60 * 24 * 30)
        # If no end was provided, use the current time.
        end_ts = self.request.query_params.get('end_ts', int(time()))
        user = self.request.user

        admin_specified_user_id = user_id
        admin_specified_user = self.get_user_for_id(admin_specified_user_id)
        if user.is_superuser and admin_specified_user is not None:
            # override the user whos transactions we will look at
            user = admin_specified_user

        #
        if start_ts > end_ts:
            return Response(
                status=409,
                data={
                    'errors': {
                        'name': {
                            'title': 'start_ts is a later time that end_ts'
                        }
                    }
                })

        return self.filter_on_range(user, int(start_ts), int(end_ts))


    def filter_on_range(self, user, start_ts, end_ts):
        start   = datetime.utcfromtimestamp( start_ts )
        end     = datetime.utcfromtimestamp( end_ts )

        transactions = Transaction.objects.filter( user=user,
                       created__range=(start, end) ).order_by('-created')

        return_json = []
        for transaction in transactions:
            return_json.append(transaction.to_json())

        return Response(return_json)


class BalanceAPIView(generics.GenericAPIView):
    """
    Gets the cash balance as a string for the logged in user formatted like '5.50'.

        * |api-text| :dfs:`cash/balance/`


    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = BalanceSerializer

    def get(self, request, format=None):
        user = self.request.user
        cash_transaction = CashTransaction(user)

        serializer = self.serializer_class(cash_transaction)
        return Response(serializer.data)


class DepositView( LoginRequiredMixin, FormView ):
    """
    The form for submitting the deposit via Braintree.

    This view requires the user to be logged in.
    """
    template_name = 'deposit.html'
    form_class = DepositAmountForm
    failure_redirect_url  = '/cash/deposit/'
    success_redirect_url  = '/cash/balance/'

    def form_valid(self, form):

        user = self.request.user
        cleaned_data = form.cleaned_data
        payment_method_nonce = self.request.POST.get('payment_method_nonce', None)

        #
        # Error out of there is not message
        if payment_method_nonce is None:
            messages.error(
                self.request,
                'Did not receive response from payment gateway'
            )
            return HttpResponseRedirect( self.failure_redirect_url )
        #
        # Attempts the transaction via braintree setting
        # customers pk and email in the braintree database
        amount = cleaned_data['amount']
        result = braintree.Transaction.sale({
                    "amount":amount,
                    "payment_method_nonce": payment_method_nonce,
                    "customer": {
                        "id": user.pk,
                        "email": user.email,
                    },
                })
        #
        # If the transaction is a success we return a success
        # message, create the database transaction, and
        # link the braintree transaction id with the dfs
        # transaction.
        if(result.is_success):
            messages.success(
                self.request,
                'The deposit was a success!',
            )
            trans = CashTransaction(user)
            trans.deposit_braintree(amount, result.transaction.id)
            return HttpResponseRedirect(self.success_redirect_url)
        #
        # On failure we redirect them and report the transaction
        # failure to the user.
        else:
            messages.error(
                self.request,
                result.transaction.processor_response_text,
            )
            return HttpResponseRedirect(self.failure_redirect_url)

    def get_context_data(self, **kwargs):
        """
        Adds the braintree client token into the context data
        for the braintree javascript to insert payment_method_nonce
        """
        context = super().get_context_data(**kwargs)
        braintree.Configuration.configure(
            settings.BRAINTREE_MODE,
            merchant_id=settings.BRAINTREE_MERCHANT,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY
        )
        context['braintree_client_token'] = braintree.ClientToken.generate()
        return context
