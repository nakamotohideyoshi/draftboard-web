#
# optimal_payments/views.py

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

from .models import Profile, Address, Card
from .serializers import AddPaymentMethodSerializer, PaymentMethodSerializer, \
                            RemovePaymentMethodSerializer
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