import calendar
import logging
from datetime import datetime, date, timedelta

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as authLogin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from raven.contrib.django.raven_compat.models import client
from rest_framework import generics
from rest_framework import response, schemas
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import (APIException, ValidationError)
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

import account.tasks
from account import const as _account_const
from account.forms import (
    LoginForm,
    SelfExclusionForm,
)
from account.models import (
    Information,
    EmailNotification,
    UserEmailNotification,
    SavedCardDetails,
    Limit
)
from account.permissions import (
    HasIpAccess,
    HasVerifiedIdentity,
)
from account.serializers import (
    LoginSerializer,
    ForgotPasswordSerializer,
    PasswordResetSerializer,
    RegisterUserSerializer,
    UserSerializer,
    UserCredentialsSerializer,
    UserSerializerNoPassword,
    UserEmailNotificationSerializer,
    UpdateUserEmailNotificationSerializer,
    SavedCardSerializer,
    SetSavedCardDefaultSerializer,
    SavedCardAddSerializer,
    SavedCardDeleteSerializer,
    SavedCardPaymentSerializer,
    CreditCardPaymentSerializer,
    UserLimitsSerializer
)
from account.utils import create_user_log
from cash.classes import (
    CashTransaction,
)
from contest.models import CurrentEntry
from contest.refund.tasks import unregister_entry_task
from pp.classes import (
    CardData,
    PayPal,
    VZero,
    VZeroTransaction,
)
from pp.serializers import (
    VZeroDepositSerializer,
)

logger = logging.getLogger('account.views')


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    """
    Swagger documentation
    """
    generator = schemas.SchemaGenerator(title='Draftboard API')
    return response.Response(generator.get_schema(request=request))


class AuthAPIView(APIView):
    """
    Login endpoint. POST to login. DELETE to logout.
    """

    authentication_classes = (BasicAuthentication,)
    serializer_class = LoginSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        args = request.data
        user = authenticate(username=args.get('username'),
                            password=args.get('password'))
        if user is not None:
            authLogin(request, user)
            #
            # return a 201
            return Response({}, status=status.HTTP_200_OK)

        #
        # the case they dont login properly
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def delete(request, *args, **kwargs):
        logout(request)
        return Response({}, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(APIView):
    """
    This api always return http 200.

    If the specified email is actually associated with a user,
    issue an email, and generate a temp password hash for them.
    """

    authentication_classes = (BasicAuthentication,)
    serializer_class = ForgotPasswordSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        #
        # validate this email is associated with a user in the db,
        # and if it is, send a password reset email to that account.
        args = request.data
        email = args.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None  # no user found... moving on.

            if user:
                #
                # fire the task that sends a password reset email to this user
                account.tasks.send_password_reset_email.delay(user)

                #
                #
        #
        # return success no matter what
        return Response({}, status=status.HTTP_200_OK)


class PasswordResetAPIView(APIView):
    # handles
    # https://www.draftboard.com/api/account/password-reset-confirm/MjA0/47k-95ee193717cb75448cf0/
    authentication_classes = (BasicAuthentication,)
    serializer_class = PasswordResetSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        args = request.data
        uid = args.get('uid')
        token = args.get('token')

        if uid and token:
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class UserAPIView(generics.RetrieveAPIView):
    """
    General user information.

    * |api-text| :dfs:`account/user/`
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserCredentialsAPIView(generics.GenericAPIView):
    """
    Allows the logged in user to modify their password and email.

        .. note::

            If username is modified in the put, it will not be saved.

        * |api-text| :dfs:`account/settings/`
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserCredentialsSerializer

    def get_object(self):
        user = self.request.user
        return user

    def post(self, request):
        user = self.get_object()
        data = request.data
        serializer = self.serializer_class(user, data=data, partial=True)

        if serializer.is_valid():
            if data.get('email'):
                user.email = data.get('email')
            if data.get('password'):
                user.set_password(data.get('password'))
            user.save()
            return Response(UserSerializerNoPassword(user).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEmailNotificationAPIView(generics.GenericAPIView):
    """
    Allows the user to get and update their user email settings

        * |api-text| :dfs:`account/notifications/email/`
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserEmailNotificationSerializer

    # Get all of the notification types, then run through each type and check if the user has a
    # setting, if not, create one in get_object().
    def get_objects(self):
        user = self.request.user
        notifications = EmailNotification.objects.filter(deprecated=False)
        for notif in notifications:
            self.get_object(notif)

        return UserEmailNotification.objects.filter(user=user)

    def get_object(self, notif):
        user = self.request.user

        try:
            email_notif = UserEmailNotification.objects.get(
                user=user,
                email_notification=notif
            )
        except UserEmailNotification.DoesNotExist:
            #
            # Creates the corresponding email notification
            email_notif = UserEmailNotification()
            email_notif.email_notification = notif
            email_notif.user = user
            email_notif.save()

        return email_notif

    def get(self, request):
        user_email_notifications = self.get_objects()
        serializer = UserEmailNotificationSerializer(user_email_notifications, many=True)

        return Response(serializer.data)

    # Update a list of UserEmailNotifications.
    def post(self, request):
        errors = []

        # Run through each supplied UserEmailNotification, updating the 'enabled' field and saving.
        for setting in request.data:
            try:
                notif = EmailNotification.objects.get(
                    deprecated=False,
                    id=setting['id']
                )
            except EmailNotification.DoesNotExist:
                errors.append("Notification id: %s does not exist" % setting.id)

            # Get the UserEmailNotification from the DB, and update the enabled field.
            user_email_notification = self.get_object(notif)
            user_email_notification.enabled = setting['enabled']
            serializer = UpdateUserEmailNotificationSerializer(
                user_email_notification, data=setting, many=False
            )
            # Save or add error to errors list.
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request)


def login(request, **kwargs):
    """
    Extension of the Django login view, redirects to the feed if already logged in.
    Unfortunately Django does not use class based views for auth so we must keep this old as well.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('frontend:lobby'))

    return auth_views.login(request, authentication_form=LoginForm)


class RegisterView(TemplateView):
    def get(self, request, *args, **kwargs):
        """
        if already logged in, redirect to lobby, otherwise allow page
        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('frontend:lobby'))

        return super(RegisterView, self).get(request, *args, **kwargs)

    template_name = 'registration/register.html'


#
##########################################################
# PayPal specific views
###########################################################


class PayPalDepositWithPayPalAccountAPIView(APIView):
    pass  # TODO


class PayPalDepositWithPayPalAccountSuccessAPIView(APIView):
    pass  # TODO


class PayPalDepositWithPayPalAccountFailAPIView(APIView):
    pass  # TODO


class PayPalDepositMixin:
    """
    it may be useful to have a mixin that can validate and perform our
    own server side deposit (a CashTransaction)
    """

    def deposit(self, user, payment_data):
        print('     ', str(payment_data))
        # check the payment state to determine if the funds deposit was successful
        success = payment_data.get('state') == 'approved'
        message = payment_data.get('message')
        if message is not None:
            raise APIException(message)
        if not success:
            raise APIException('The deposit was unsuccessful.')

        #
        paypal_transaction_id = payment_data.get('id')
        # 'transactions': [
        #   {'amount':
        #       {'currency': 'USD',
        #       'details': {'subtotal': '25.55'},
        #       'total': '25.55'
        #   },

        # if we fail to get the amount here, thats bad i think
        try:
            amount = float(payment_data.get('transactions')[0].get('amount').get('total'))
        except Exception as e:
            print("float(payment_data.get('transactions')[0].get('amount').get('total'))")
            raise APIException(e)

        if paypal_transaction_id is None:
            raise APIException('PayPal payment did not respond with a valid "id".')

        ct = CashTransaction(user)
        ct.deposit_paypal_with_saved_card(amount, paypal_transaction_id)

        # money deposited!
        return Response(status=200)


class PayPalDepositCreditCardAPIView(APIView, PayPalDepositMixin):
    """
    example of the POST data:

        {
            "type":"visa","number":"4032036765082399",
            "exp_month":"12","exp_year":"2020","cvv2":"012",
            "first_name":"joe","last_name":"depositor","amount":21.99
        }

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CreditCardPaymentSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class(data=self.request.data).is_valid(raise_exception=True)

        # get the values from the serializer
        type = self.request.data.get('type')
        number = self.request.data.get('number')
        exp_month = self.request.data.get('exp_month')
        exp_year = self.request.data.get('exp_year')
        cvv2 = self.request.data.get('cvv2')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        amount = self.request.data.get('amount')

        # return Response(status=200)

        pp = PayPal()
        pp.auth()

        # example: we could build a CardData() object for some light
        # validation, but we could also let the serializer do it...or paypals own api...
        # but lets just ship it to paypal and use their error responses and see
        # how that works out initially.

        # execute paypal api call
        try:
            payment_data = pp.pay_with_credit_card(amount, type, number, exp_month, exp_year,
                                                   cvv2, first_name, last_name)
        except PayPal.PayPalException as e:
            raise APIException(e)

        # uses the mixin's method to validate the
        # paypal response and deposit a cash transaction
        # in the users account if the pp transaction was successful
        return self.deposit(self.request.user, payment_data)


class PayPalDepositSavedCardAPIView(APIView):
    """
    example format json post params:

        {"amount":77.00,"token":"CARD-6WP04454GN306160EK5ZOADI"}

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SavedCardPaymentSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class(data=self.request.data).is_valid(raise_exception=True)
        token = self.request.data.get('token')
        amount = self.request.data.get('amount')
        print('%.2f' % amount)

        # make sure the card token is valid for this user
        try:
            saved_card = SavedCardDetails.objects.get(user=self.request.user, token=token)
        except SavedCardDetails.DoesNotExist:
            raise APIException('No saved card exists for the user and token specified.')

        # make the deposit
        pp = PayPal()
        pp.auth()
        payment_data = pp.pay_with_saved_card(amount, saved_card.user.username, saved_card.token)

        # check the payment state to determine if the funds deposit was successful
        success = payment_data.get('state') == 'approved'
        message = payment_data.get('message')
        if message is not None:
            raise APIException(message)
        if not success:
            raise APIException('The deposit was unsuccessful.')

        #
        paypal_transaction_id = payment_data.get('id')
        if paypal_transaction_id is None:
            raise APIException('PayPal payment did not respond with a valid "id".')

        ct = CashTransaction(self.request.user)
        ct.deposit_paypal_with_saved_card(amount, paypal_transaction_id)

        # money deposited!
        return Response(status=200)

        # In [4]: pp.pay_with_saved_card(25.55, 'admin', 'CARD-6WP04454GN306160EK5ZOADI')
        # Out[4]:
        # {'create_time': '2016-06-28T20:47:39Z',
        #  'id': 'PAY-8B978986LB367434PK5ZOE2Y',
        #  'intent': 'sale',
        #  'links': [{
        #       'href':
        #           'https://api.sandbox.paypal.com/v1/payments/payment/PAY-8B978986LB367434PK5ZOE2Y',
        #    'method': 'GET',
        #    'rel': 'self'}],
        #  'payer': {
        #      'funding_instruments':
        #           [{'credit_card_token': {'credit_card_id': 'CARD-6WP04454GN306160EK5ZOADI',
        #      'expire_month': '12',
        #      'expire_year': '2020',
        #      'last4': '2399',
        #      'payer_id': 'admin',
        #      'type': 'visa'}}],
        #   'payment_method': 'credit_card'},
        #  'state': 'approved',
        #  'transactions': [{'amount': {'currency': 'USD',
        #     'details': {'subtotal': '25.55'},
        #     'total': '25.55'},
        #    'description': 'This is the payment transaction description.',
        #    'related_resources': [{'sale': {'amount': {'currency': 'USD',
        #        'total': '25.55'},
        #       'create_time': '2016-06-28T20:47:39Z',
        #       'fmf_details': {},
        #       'id': '3CS45219T6507753W',
        #       'links': [{'href':
        #           'https://api.sandbox.paypal.com/v1/payments/sale/3CS45219T6507753W',
        #         'method': 'GET',
        #         'rel': 'self'},
        #        {'href':
        #           'https://api.sandbox.paypal.com/v1/payments/sale/3CS45219T6507753W/refund',
        #         'method': 'POST',
        #         'rel': 'refund'},
        #        {'href':
        #           'https://api.sandbox.paypal.com/v1/payments/payment/PAY-8B978986LB367434PK5ZOE2Y',
        #         'method': 'GET',
        #         'rel': 'parent_payment'}],
        #       'parent_payment': 'PAY-8B978986LB367434PK5ZOE2Y',
        #       'processor_response': {'avs_code': 'X', 'cvv_code': 'M'},
        #       'state': 'completed',
        #       'update_time': '2016-06-28T20:47:50Z'}}]}],
        #  'update_time': '2016-06-28T20:47:50Z'}


class PayPalSavedCardAddAPIView(APIView):
    """
    the first card added will be set to be the default saved card.

    post json to this endpoint in the form:

        {"type":"visa","number":"4032036765082399","exp_month":"12","exp_year":"2020","cvv2":"012"}

    """

    permission_classes = (IsAuthenticated,)
    serializer_class = SavedCardAddSerializer

    def validate_information(self, info):
        missing_fields = []
        # print('address1', info.address1)
        if not info.address1:
            # print('  not address1')
            missing_fields.append('address1')
        # print('address2', info.address2)
        # if not info.address2:
        #     print('  not address2')
        # print('city',  info.city)
        if not info.city:
            # print('  not city')
            missing_fields.append('city')
        # print('state', info.state)
        if not info.state:
            # print('  not state')
            missing_fields.append('state')
        # print('zipcode', info.zipcode)
        if not info.zipcode:
            # print('  not zipcode')
            missing_fields.append('zipcode')

        if len(missing_fields) > 0:
            raise APIException('Accout Information is missing: ' + str(missing_fields))

    # TODO - test
    def create_paypal_saved_card(self, user, card_type, number, exp_month, exp_year, cvv2):
        """
        using paypal api, try to save a card, and return the data
        """

        # ensure the users first_name and last_name exist! we require them

        card_data = CardData()

        # populate the CardData with required user/creditcard info
        card_data.set_card_field(CardData.EXTERNAL_CUSTOMER_ID, user.username)
        card_data.set_card_field(CardData.TYPE, card_type)
        card_data.set_card_field(CardData.NUMBER, number)
        card_data.set_card_field(CardData.EXPIRE_MONTH, exp_month)
        card_data.set_card_field(CardData.EXPIRE_YEAR, exp_year)
        card_data.set_card_field(CardData.CVV2, cvv2)
        card_data.set_card_field(CardData.FIRST_NAME, user.first_name)
        card_data.set_card_field(CardData.LAST_NAME, user.last_name)

        # get the billing address information
        # TODO - all the fields we use should exist (its possible they do not)
        info = Information.objects.get(user=user)
        self.validate_information(info)

        # populate the CardData with required billing info
        line1 = info.address1
        # line2 = info.address2  # unused currently
        card_data.set_billing_field(CardData.LINE_1, line1)
        card_data.set_billing_field(CardData.CITY, info.city)
        card_data.set_billing_field(CardData.STATE, info.state)
        card_data.set_billing_field(CardData.COUNTRY_CODE, 'US')  # TODO allow others?
        card_data.set_billing_field(CardData.POSTAL_CODE, info.zipcode)

        # print('card_data.get_data():', str(card_data.get_data()))

        # call paypal api
        pp = PayPal()
        pp.auth()
        saved_card_data = pp.save_card(card_data.get_data())
        return saved_card_data

    # TODO - finish/test
    def create_saved_card_details(self, user, token, card_type, last_4, exp_month, exp_year):
        """
        once we have successfully saved a card using paypal's api,
        create a reference to that saved card (especially the token)
        in our own backend.
        """

        default = False
        # check if any previously saved cards
        existing_saved_cards = SavedCardDetails.objects.filter(user=user)
        if existing_saved_cards.count() == 0:
            default = True

        # get the card type properties
        # and create the SavedCardDetails instance.
        saved_card = SavedCardDetails()
        saved_card.token = token
        saved_card.user = user
        saved_card.type = card_type
        saved_card.last_4 = last_4
        saved_card.exp_month = exp_month
        saved_card.exp_year = exp_year
        saved_card.default = default
        saved_card.save()
        return saved_card

    def post(self, request, *args, **kwargs):
        self.serializer_class(data=self.request.data).is_valid(raise_exception=True)

        user = self.request.user
        args = self.request.data

        # get the card type properties so we can create a SavedCardDetails instance
        # the first/last name will come from the user object internally
        # first_name  = args.get('first_name')       # TODO - validate the CARDHOLDER first name
        # last_name   = args.get('last_name')        # TODO - validate the CARDHOLDER last name
        card_type = args.get('type')
        number = args.get('number')
        exp_month = args.get('exp_month')
        exp_year = args.get('exp_year')
        cvv2 = args.get('cvv2')

        # save the card using paypal
        try:
            save_card_api_data = self.create_paypal_saved_card(
                user, card_type, number, exp_month, exp_year, cvv2)
        except Information.DoesNotExist:
            raise APIException("Incomplete information. Is billing address filled out?")

        # use the paypal api response to stash some
        # information about the saved card in our db.
        # we do not save sensitive information for security reasons!
        token = save_card_api_data.get('id')
        if token is None:
            paypal_details = save_card_api_data.get('details')
            raise APIException(paypal_details)

        last_4 = number[-4:]  # slice off the last 4 digits
        saved_card = self.create_saved_card_details(
            user, token, card_type, last_4, exp_month, exp_year)

        # return serialized data of the new saved card
        return Response(SavedCardSerializer(saved_card, many=False).data, status=200)


class PayPalSavedCardDeleteAPIView(APIView):
    """
    post json in this form to delete a saved card:

        {"token": "Card-99999"}

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SavedCardDeleteSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        token = self.request.data.get('token')
        if token is None:
            return Response("token required", status=405)
        try:
            card = SavedCardDetails.objects.get(user=user, token=token)
        except SavedCardDetails.DoesNotExist:
            return Response("card not found for user, token: %s" % token, status=404)

        deleted_card_was_default = card.default
        card.delete()

        # if the card was the default card, and there are any more cards
        # randomly set one of them to the new default
        remaining_cards = SavedCardDetails.objects.filter(user=user)
        if deleted_card_was_default and remaining_cards.count() > 0:
            new_default_card = remaining_cards[0]
            new_default_card.default = True
            new_default_card.save()

        return Response(status=200)


class PayPalSavedCardListAPIView(APIView):
    """
    get a list of the saved cards.

    these cards have an id which can be used to
    quickly deposit money to the site.
    """

    permission_classes = (IsAuthenticated,)
    response_serializer = SavedCardSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # print('PayPalSavedCardListAPIView user:', user)

        saved_cards = None
        try:
            saved_cards = SavedCardDetails.objects.filter(user=user)
        except TypeError:
            raise APIException("Invalid user: %s" % user)

        # serialize the list of saved cards
        serialized_data = self.response_serializer(saved_cards, many=True).data
        return Response(serialized_data)


class SetSavedCardDefaultAPIView(APIView):
    """
    the arguments to this method should be passed
    in the POST as application/json, ie: {"token":"theToken"}
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SetSavedCardDefaultSerializer

    def post(self, request):
        user = self.request.user
        args = self.request.data
        token = args.get('token')

        # if token is None: # TODO raise error if token is not set
        #     raise rest_framework

        saved_cards = None
        try:
            saved_cards = SavedCardDetails.objects.filter(user=user)
        except TypeError:
            return Response(status=405)

        # update this specific card to default=True
        enabled_cards = saved_cards.filter(token=token)  # filter() returns a queryset
        if enabled_cards.count() >= 1:
            # update all the cards to default=False
            saved_cards.update(default=False)
            # update this card to default=True
            card = enabled_cards[0]
            card.default = True
            card.save()

        # return success response of simply http 200
        return Response(status=200)


class VZeroGetClientTokenView(APIView):
    """
    retrieve a paypal vzero client token
    """

    permission_classes = (IsAuthenticated, HasIpAccess)
    serializer_classes = None

    def get(self, request, *args, **kwargs):
        vzero = VZero()
        client_token = vzero.get_client_token()
        return Response({'client_token': client_token}, status=200)


class VZeroDepositView(APIView):
    """
    deposit to the site using paypal vzero

    this api requires the client to provide a 'payment_method_nonce'
    which was acquired from having previously retrieved a
    'client_token' from the server and dont any client side setup necessary.

    example:

        >>> {"first_name":"Steve","last_name":"Steverton","street_address":"1 Steve St",
            "extended_address":"Suite 1","locality":"Dover","region":"NH","postal_code":"03820",
            "country_code_alpha2":"US","amount":"100.00","payment_method_nonce":"FAKE_NONCE"}
    """

    permission_classes = (IsAuthenticated, HasIpAccess, HasVerifiedIdentity)
    serializer_class = VZeroDepositSerializer

    def post(self, request, *args, **kwargs):
        # get the django user
        # user = self.request.user

        # shipping_data = {
        #     'first_name': user.information.fullname,
        #     'last_name': user.information.fullname,
        #     'street_address': user.information.address1,
        #     'extended_address': user.information.address2,
        #     'locality': user.information.city,
        #     'region': user.information.state,
        #     'postal_code': user.information.zipcode
        # }

        # validate the validity of the params
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        transaction_data = serializer.data
        amount = float(transaction_data.get('amount'))
        user_deposits = float(request.user.information.deposits_for_period)
        user_limit = request.user.information.deposits_limit
        if user_limit:
            if amount + user_deposits > user_limit:
                raise APIException('Sorry but you have exceeded your limit')

        # shipping_serializer = VZeroShippingSerializer(data=self.request.data)
        # shipping_serializer.is_valid(raise_exception=True)
        # shipping_data = shipping_serializer.data

        # using the information (payment_method_nonce, amount, shipping info)
        # make the deposit using the VZero object to create the transaction (sale)
        transaction = VZeroTransaction()
        transaction.update_data(shipping_data={}, transaction_data=transaction_data)

        vzero = VZero()
        try:
            transaction_id = vzero.create_transaction(transaction)
        # except VZero.VZeroException as e:
        except Exception as e:
            # Throw Paypal exceptions back through the API, log & report the details
            logger.error("VZeroDepositView() user: %s - %s" % (request.user.username, str(e)))
            client.captureException()
            raise APIException({'detail': "vzero create transaction error"})

        # TODO add a transaction type (?)

        # TODO create a model for saving the transaction information

        # create the draftboard cash deposit with the transaction id
        try:
            ct = CashTransaction(self.request.user)
            ct.deposit_vzero(amount, transaction_id)
        except Exception:
            raise APIException({'detail': """
                Error adding funds to draftboard account. Please contact admin@draftboard.com"""})

        create_user_log(
            user=request.user,
            request=request,
            type=_account_const.FUNDS,
            action=_account_const.DEPOSIT,
            metadata={
                'detail': 'Funds deposited via PayPal.',
                'amount': amount,
                'transaction_data': transaction_data,
            }
        )

        # return success response if everything went ok
        return Response(status=200)


class VerifyLocationAPIView(APIView):
    """
    A simple endpoint to run the HasIpAccess permission class.
    If the user's IP acceptable, return 200. otherwise a 403.
    This location check is done with our local IP database. This does NOT
    use GIDX to do a hard check on the user.
    """
    permission_classes = (HasIpAccess,)

    @staticmethod
    def get(request):
        return Response(
            data={
                "status": "SUCCESS",
                "detail": "location verification passed"
            },
            status=200,
        )


class VerifyUserAPIView(APIView):
    """

    """
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        return Response(
            data={
                "status": "TODO",
                "detail": "This doesn't do anything yet."
            },
            status=200,
        )


class RegisterAccountAPIView(APIView):
    """
    verify the user is real based on the information specified.
    this will create a log of the trulioo transaction in the django admin

    - Attempt to verify user identity with Trulioo.

    if success:
        - Attempt to create User account.

        if success:
            - Create user Identity.

            if failure:
                - return validation errors.

        if failure:
            - return validation errors

    if failure:
        - return Identity validation errors


    example POST param (JSON):

    {"username": "myUserName", "password": "pa$$word", "email": "me@email.com"}
    """

    permission_classes = ()
    register_user_serializer_class = RegisterUserSerializer

    def post(self, request):
        # - Attempt to create User account.
        user_serializer = self.register_user_serializer_class(data=request.data)

        if user_serializer.is_valid(raise_exception=True):
            username = user_serializer.validated_data.get('username')
            email = user_serializer.validated_data.get('email')
            password = user_serializer.validated_data.get('password')

            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            # Make sure each user gets an information model.
            Information.objects.create(user=user)
            new_user = authenticate(username=user.username, password=password)

            # Log user in.
            if new_user is not None:
                authLogin(request, new_user)

                # DO NOT respond yet. we still need to save the user's Identity below.
        else:
            # If there were user user_serializer, send em back to the user.
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If the verification request was successful...
        #
        # Save the information so we can do multi-account checking.
        # create_user_identity(new_user, first, last, birth_day, birth_month, birth_year, postal_code)
        # return success response if everything went ok
        return Response(data={"detail": "Account Created"}, status=status.HTTP_201_CREATED)


class AccessSubdomainsTemplateView(LoginRequiredMixin, TemplateView):
    """
    A view that, if you have access, sets a cookie to let you view other Run It Once sites in development.
    """
    template_name = 'frontend/access_subdomains.html'

    def render_to_response(self, context, **response_kwargs):
        """
        If user is logged in, redirect them to their feed
        """
        response = super(AccessSubdomainsTemplateView, self).render_to_response(context,
                                                                                **response_kwargs)

        if not self.request.user.has_perm('sites.access_subdomains'):
            raise Http404

        days_expire = 7
        max_age = days_expire * 24 * 60 * 60
        expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age),
                                    "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie('access_subdomains', 'true', max_age=max_age, expires=expires,
                            domain=settings.COOKIE_ACCESS_DOMAIN)
        return response


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


class ExclusionFormView(FormView):
    template_name = 'frontend/self-exclusion.html'
    form_class = SelfExclusionForm
    success_url = '/'
    months = [3, 6, 9, 12]

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data()
        cur_date = date.today()
        for month in self.months:
            kwargs['%s_month' % month] = add_months(cur_date, month)
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user.information
        return kwargs

    def form_valid(self, form):
        information = form.save()
        entries = CurrentEntry.objects.filter(user=information.user)
        for entry in entries:
            unregister_entry_task.delay(entry)
            UserEmailNotification.objects.filter(user=information.user).update(enabled=False)
            logout(self.request)
        return super().form_valid(form)


class UserLimitsAPIView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = UserLimitsSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        limits = user.limits.all()
        user_limits = []
        serializer = None
        if limits.exists():
            serializer = self.serializer_class(limits, many=True)
        else:
            for limit_type in Limit.TYPES:
                limit_type_index = limit_type[0]
                val = Limit.TYPES_GLOBAL[limit_type_index]['value'][0][0]
                user_limits.append({'user': user.pk,
                                    'type': limit_type_index,
                                    'value': val,
                                    'time_period': Limit.PERIODS[0][
                                        0] if limit_type != Limit.ENTRY_FEE else None})
        limits_data = {'types': Limit.TYPES_GLOBAL,
                       'current_values': serializer.data if serializer else user_limits}
        return Response(limits_data)

    def post(self, request, *args, **kwargs):
        user = request.user
        limits = user.limits.all()

        if limits.exists():
            serializer = self.serializer_class(limits, data=self.request.data, many=True)
            # If the user has no Identity, we can't set play limits.
            if not user.information.has_verified_identity:
                raise ValidationError(
                    {'detail': 'You must verify your identity before setting play limits.'})
            state = user.identity.state
            if state:
                days = settings.LIMIT_DAYS_RESTRAINT.get(state)
                if days:
                    change_allowed_on = limits[0].updated + timedelta(days=days)
                    if timezone.now() < change_allowed_on:
                        return JsonResponse(data={
                            "detail": "Not allowed to change limits until {}".format(
                                change_allowed_on.strftime('%Y-%m-%d %I:%M %p'))}, status=400,
                            safe=False)

        else:
            serializer = self.serializer_class(data=self.request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"detail": "Limits Saved"}, status=200)
