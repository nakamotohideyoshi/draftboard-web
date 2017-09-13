from datetime import datetime
from logging import getLogger
from time import time

import braintree
import xlwt
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.views.generic.edit import FormView
from raven.contrib.django.raven_compat.models import client
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cash.classes import CashTransaction
from cash.forms import DepositAmountForm
from cash.serializers import (
    TransactionHistorySerializer, BalanceSerializer, TransactionDetailSerializer)
from transaction.models import Transaction
from transaction.tasks import send_deposit_receipt

logger = getLogger('cash.views')


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

    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionHistorySerializer

    def get_queryset(self, *args, **kwargs):
        return Transaction

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
        export = self.request.query_params.get('export', None)
        user = self.request.user

        if start_ts > end_ts:
            return Response(
                status=409,
                data={'detail': 'start_ts is a later time that end_ts'},
            )

        if export:
            return self.export_exel(user, int(start_ts), int(end_ts))

        return self.filter_on_range(user, int(start_ts), int(end_ts))

    @staticmethod
    def export_exel(user, start_ts, end_ts):
        start = datetime.utcfromtimestamp(start_ts)
        end = datetime.utcfromtimestamp(end_ts)
        transactions = Transaction.objects.filter(
            user=user, created__range=(start, end)).order_by('-created')

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="transactions-history.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('History')
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Created', 'Amount', 'Type']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows = [
            [transaction.created,
             transaction.to_json(user_only=True).get('details', [{}])[0].get('amount'),
             transaction.to_json(user_only=True).get('details', [{}])[0].get('type')] for
            transaction in transactions]
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    @staticmethod
    def filter_on_range(user, start_ts, end_ts):
        start = datetime.utcfromtimestamp(start_ts)
        end = datetime.utcfromtimestamp(end_ts)

        # TODO: this would be a lot easier if we queried the CashTransactionDetail here
        # then pulled transactions + actions from that.
        transactions = Transaction.objects.filter(
            user=user, created__range=(start, end)).order_by('-created')

        return_json = []
        for transaction in transactions:
            return_json.append(transaction.to_json(user_only=True))

        return Response(return_json)


class TransactionDetailAPIView(generics.RetrieveAPIView):
    # TODO: Finish up this transaction detail view - it will populate the detail pane
    # on the transaction page.
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()
    lookup_field = 'pk'
    lookup_url_kwarg = 'transaction_id'
    serializer_class = TransactionDetailSerializer


class BalanceAPIView(generics.GenericAPIView):
    """
    Gets the cash balance as a string for the logged in user formatted like '5.50'.

        * |api-text| :dfs:`cash/balance/`


    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = BalanceSerializer

    def get(self, request):
        user = self.request.user
        cash_transaction = CashTransaction(user)

        serializer = self.serializer_class(cash_transaction)
        return Response(serializer.data)


class DepositView(LoginRequiredMixin, FormView):
    """
    The form for submitting the deposit via Braintree.

    This view requires the user to be logged in.
    """
    template_name = 'deposit.html'
    form_class = DepositAmountForm
    failure_redirect_url = '/cash/deposit/'
    success_redirect_url = '/cash/balance/'

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
            return HttpResponseRedirect(self.failure_redirect_url)
        #
        # Attempts the transaction via braintree setting
        # customers pk and email in the braintree database
        amount = cleaned_data['amount']
        result = braintree.Transaction.sale({
            "amount": amount,
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
        if result.is_success:
            messages.success(
                self.request,
                'The deposit was a success!',
            )
            trans = CashTransaction(user)
            trans.deposit_braintree(amount, result.transaction.id)
            # Create a task that will send the user an email confirming the transaction
            try:
                send_deposit_receipt.delay(user, amount, trans.get_balance_string_formatted(),
                                           timezone.now())
            except Exception as e:
                logger.error(e)
                client.captureException(e)
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
