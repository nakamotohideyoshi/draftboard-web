#
# optimal_payments/views.py

from django.db.transaction import atomic
from django.contrib.auth.models import User
from django.core.cache import caches

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from cash.classes import CashTransaction
from .classes import CardPurchase
from .models import Profile, Address, Card
from .serializers import AddPaymentMethodSerializer, PaymentMethodSerializer, \
                            RemovePaymentMethodSerializer, \
                            DepositPaymentTokenSerializer, DepositCreditCardSerializer
from .classes import NetBanxApi, CustomerProfile, CreateAddress, CreateCard, PaymentMethodManager

class AddPaymentMethodAPIView(generics.CreateAPIView):
    """
    add a payment method (ie: save a credit card to the users account for future use)
    """
    permission_classes      = (IsAuthenticated,)
    serializer_class        = AddPaymentMethodSerializer

    def post(self, request, format=None):
        print( request.user )
        print( request.data )

        billing_nickname    = request.data.get('billing_nickname')
        street              = request.data.get('street')
        city                = request.data.get('city')
        state               = request.data.get('state')
        country             = request.data.get('country')
        zip                 = request.data.get('zip')

        # card fields
        card_nickname       = request.data.get('card_nickname')
        holder_name         = request.data.get('holder_name')
        card_num            = request.data.get('card_num')
        exp_month           = request.data.get('exp_month')
        exp_year            = request.data.get('exp_year')

        # get or create the CustomerProfile object from the User
        try:
            cp = CustomerProfile()
            profile, created = cp.get_or_create( request.user )
        except NetBanxApi.NetBanxApiException:
            return Response( 'There was an error creating this payment method.',
                                status=status.HTTP_403_FORBIDDEN )

        # create an Address to associate the new payment method (card) with
        # try:
        ad = CreateAddress( profile )
        address = ad.create( billing_nickname, street, city, state, zip, country )
        # except NetBanxApi.NetBanxApiException:
        #     return Response( 'There was an error creating this payment method. (Address)',
        #                         status=status.HTTP_403_FORBIDDEN )

        # create a payment method (ie: add a card)
        try:
            c = CreateCard( profile, address )                  # 2 digits,  4 digits
            crd = c.create( card_nickname, holder_name, card_num, exp_month, exp_year )

        except NetBanxApi.CustomerCardExistsException:
            return Response( 'This card is already a payment method.',
                                    status=status.HTTP_403_FORBIDDEN )
        except NetBanxApi.NetBanxApiException:
            return Response( 'There was an error creating this payment method. (Card)',
                                    status=status.HTTP_403_FORBIDDEN )

        # on successful retrieval/creation of Profile, and creation of Address & Card:
        return Response('Payment method added successfuly.', status=status.HTTP_201_CREATED)

class PaymentMethodAPIView(generics.ListAPIView):
    """
    view for all of a Users payment methods
    """

    permission_classes      = (IsAuthenticated,)
    serializer_class        = PaymentMethodSerializer

    def get_queryset(self):
        """
        get the Card objects (ie: the payment methods) this user has
        """
        return Card.objects.filter( user=self.request.user )

class RemovePaymentMethodAPIView(generics.CreateAPIView):
    """
    remove a payment method (this also removes the billing object associated with it)
    """

    permission_classes      = (IsAuthenticated,)
    serializer_class        = RemovePaymentMethodSerializer

    def post(self, request, format=None):
        print( request.user )
        print( request.data )

        oid = request.data.get('oid')  # the oid identifier of the  Card to delete

        #try:
            # this results in some hidden third-party api
            # calls and may not return for a few seconds
        payment_manager = PaymentMethodManager(request.user)
        payment_manager.delete(oid)

        # except NetBanxApi.NetBanxApiException:
        #     return Response( 'NetBanxApiException', status=status.HTTP_403_FORBIDDEN )
        #
        # except:
        #     return Response( 'Unknown error while removing payment method', status=status.HTTP_403_FORBIDDEN )

        # on successful retrieval/creation of Profile, and creation of Address & Card:
        return Response('Payment method removed.', status=status.HTTP_201_CREATED)

class AbstractOptimalDepositAPIView(generics.CreateAPIView):
    """
    parent class for views that perform any type of deposit using OpitmalPayments(NetBanx)
    """
    permission_classes      = (IsAuthenticated,)

    def deposit(self, user, amount, optimal_transaction_id):
        ct = CashTransaction( user )
        ct.deposit_optimal( amount, optimal_transaction_id )   # optimal_api_response.id  example: 'a6e29e26-74a3-4a70-a7ac-b9bf25a06f3e'

class DepositPaymentTokenAPIView(AbstractOptimalDepositAPIView):
    """
    make a deposit with a saved payment method
    """

    serializer_class        = DepositPaymentTokenSerializer

    @atomic
    def post(self, request, format=None):
        print( request.user )
        print( request.data )

        amount = request.data.get('amount')
        oid = request.data.get('oid')  # the oid identifier of the Card to use

        # TODO test this
        crd = Card.objects.get(user=request.user, oid=oid)
        cp = CardPurchase()
        optimal_transaction_id = cp.process_purchase_token( amount, crd.payment_token )
        self.deposit( request.user, float(amount), optimal_transaction_id)

        return Response('Funds have been successfully deposited into your account.', status=status.HTTP_201_CREATED)

class DepositCreditCardAPIView(AbstractOptimalDepositAPIView):
    """
    make a deposit with a credit card
    """

    serializer_class        = DepositPaymentTokenSerializer

    @atomic
    def post(self, request, format=None):
        print( request.user )
        print( request.data )

        amount          = request.data.get('amount')
        cc_num          = request.data.get('cc_num')
        cvv             = request.data.get('cvv')
        exp_month       = request.data.get('exp_month')
        exp_year        = request.data.get('exp_year')
        billing_zipcode = request.data.get('billing_zipcode')

        cp = CardPurchase()
        optimal_transaction_id = cp.process_purchase( amount, cc_num, cvv,
                                        exp_month, exp_year, billing_zipcode )

#         # CardPurchase.process_payment() may raise the following Exceptions:
#         #     CardPurchase.OptimalServiceMonitorDownException
#         #     CardPurchase.OptimalServiceMonitorNotReadyException
#         #     CardPurchase.InvalidArgumentException
#         #     CardPurchase.ExpiredCreditCardException
#         #     CardPurchase.ProcessingException
#         #     CardPurchase.PaymentDeclinedException
#         #     CardPurchase.UnknownNetbanxErrorCodeException
#         #     CardPurchase.ProcessPaymentResponseStatusException

        # create a record of the transaction in our own database
        # with enough information so we could match this
        # payment with the same payment on the netbanx/optimal account
        # ct = CashTransaction( request.user )
        # ct.deposit_optimal( amount, optimal_api_response.id )   # optimal_api_response.id  example: 'a6e29e26-74a3-4a70-a7ac-b9bf25a06f3e'

        self.deposit( request.user, float(amount), optimal_transaction_id)

        return Response('Funds have been successfully deposited into your account.', status=status.HTTP_201_CREATED)
