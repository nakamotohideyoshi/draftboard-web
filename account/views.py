#
# views.py

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from account.models import (
    Information,
    EmailNotification,
    UserEmailNotification,
    SavedCardDetails,
)
from account.permissions import IsNotAuthenticated
from account.serializers import (
    LoginSerializer,
    ForgotPasswordSerializer,
    PasswordResetSerializer,
    RegisterUserSerializer,
    UserSerializer,
    UserSerializerNoPassword,
    InformationSerializer,
    UserEmailNotificationSerializer,
    UpdateUserEmailNotificationSerializer,
    SavedCardSerializer,
    SetSavedCardDefaultSerializer,
    SavedCardAddSerializer,
    SavedCardDeleteSerializer,
    SavedCardPaymentSerializer,
    CreditCardPaymentSerializer,
)
import account.tasks
from pp.classes import (
    CardData,
    PayPal,
)
from cash.classes import (
    CashTransaction,
)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as authLogin
from django.contrib.auth import authenticate, logout
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


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

    def post(self, request, *args, **kwargs):
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

    def delete(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
        args = request.data
        uid = args.get('uid')
        token = args.get('token')

        print(uid, token)
        if uid and token:
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterAccountAPIView(generics.CreateAPIView):
    """
    Registers new users.

        * |api-text| :dfs:`account/register/`
    """
    permission_classes = (IsNotAuthenticated,)

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, format=None):
        data = request.data
        serializer = RegisterUserSerializer(data=data)

        if serializer.is_valid():
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()

            newUser = authenticate(username=user.username, password=password)
            if newUser is not None:
                authLogin(request, newUser)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(generics.GenericAPIView):
    """
    Allows the logged in user to modify their password and email.

        .. note::

            If username is modified in the put, it will not be saved.

        * |api-text| :dfs:`account/settings/`
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        return user

    def post(self, request, format=None):
        user = self.get_object()
        data = request.data
        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            if(data.get('email')):
                user.email = data.get('email')
            if(data.get('password')):
                user.set_password(data.get('password'))
            user.save()
            return Response(UserSerializerNoPassword(user).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InformationAPIView (generics.GenericAPIView):
    """
    Allows the logged in user to modify their personal information.

        * |api-text| :dfs:`account/information/`
    """
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = InformationSerializer

    def get_object(self):
        user = self.request.user

        try:
            info = Information.objects.get(user=user)
        except Information.DoesNotExist:
            #
            # Creates the user information for the user to modify
            # if it does not already exist in the database.
            #
            info = Information()
            info.user = user
            info.fullname = ""
            info.address1 = ""
            info.address2 = ""
            info.city = ""
            info.state = ""
            info.zipcode = ""
            info.dob = None
            info.save()
            info = Information.objects.filter(user=user)
        return info

    def get(self, request, format=None):
        info = self.get_object()
        serializer = InformationSerializer(info, many=False)

        return Response(serializer.data)

    def post(self, request, format=None):
        info = self.get_object()
        serializer = InformationSerializer(info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class EmailNotificationAPIView (generics.ListCreateAPIView):
#     """
#     Allows the admin to modify and insert new Email Notifications
#
#         * |api-text| :dfs:`account/email/notification/`
#     """
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAdminUser,)
#     serializer_class = EmailNotificationSerializer
#     queryset = EmailNotification.objects.all()


class UserEmailNotificationAPIView (generics.GenericAPIView):
    """
    Allows the user to get and update their user email settings

        * |api-text| :dfs:`account/notifications/email/`
    """
    permission_classes = (IsAuthenticated, )
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

    def get(self, request, format=None):
        user_email_notifications = self.get_objects()
        serializer = UserEmailNotificationSerializer(user_email_notifications, many=True)

        return Response(serializer.data)

    # Update a list of UserEmailNotifications.
    def post(self, request, format=None):
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


class WithdrawAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def post(self, request, *args, **kwargs):
        return Response(
            status=409,
            data={'errors': {
                'ssn': {
                    'title': 'SSN needed.',
                    'description': """By law restrictions, if you are willing to withdraw
                            more than $700, ssn is needed."""
                }
            }
            }
        )


class DepositAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def post(self, request, *args, **kwargs):
        return Response(status=202)


class PaymentsAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        return Response([
            {
                'type': 'visa',
                'ending': 2785,
                'expires': '11/2016',
                'isDefault': False,
                'id': 1,
            },
            {
                'type': 'amex',
                'ending': 2785,
                'expires': '11/2016',
                'isDefault': True,
                'id': 2,
            },
            {
                'type': 'discover',
                'ending': 2785,
                'expires': '11/2016',
                'isDefault': False,
                'id': 3,
            },
            {
                'type': 'mastercard',
                'ending': 2785,
                'expires': '11/2016',
                'isDefault': False,
                'id': 10,
            }
        ])


class AddPaymentMethodAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def post(self, request, *args, **kwargs):
        return Response({
            'type': 'mastercard',
            'ending': 6612,
            'expires': '11/2316',
            'isDefault': False,
            'id': 14,
        })


class RemovePaymentMethodAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def delete(self, request, *args, **kwargs):
        return Response(status=204)


class SetDefaultPaymentMethodAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def post(self, request, *args, **kwargs):
        return Response(status=201)


def login(request, **kwargs):
    """
    Extension of the Django login view, redirects to the feed if already logged in.
    Unfortunately Django does not use class based views for auth so we must keep this old as well.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('frontend:lobby'))

    return auth_views.login(request)


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
    pass          # TODO


class PayPalDepositWithPayPalAccountSuccessAPIView(APIView):
    pass   # TODO


class PayPalDepositWithPayPalAccountFailAPIView(APIView):
    pass      # TODO


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
    permission_classes = (IsAuthenticated, )
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
    permission_classes = (IsAuthenticated, )
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
        #  'links': [{'href': 'https://api.sandbox.paypal.com/v1/payments/payment/PAY-8B978986LB367434PK5ZOE2Y',
        #    'method': 'GET',
        #    'rel': 'self'}],
        #  'payer': {'funding_instruments': [{'credit_card_token': {'credit_card_id': 'CARD-6WP04454GN306160EK5ZOADI',
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
        #       'links': [{'href': 'https://api.sandbox.paypal.com/v1/payments/sale/3CS45219T6507753W',
        #         'method': 'GET',
        #         'rel': 'self'},
        #        {'href': 'https://api.sandbox.paypal.com/v1/payments/sale/3CS45219T6507753W/refund',
        #         'method': 'POST',
        #         'rel': 'refund'},
        #        {'href': 'https://api.sandbox.paypal.com/v1/payments/payment/PAY-8B978986LB367434PK5ZOE2Y',
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

    permission_classes = (IsAuthenticated, )
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
    permission_classes = (IsAuthenticated, )
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

    permission_classes = (IsAuthenticated, )
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
    permission_classes = (IsAuthenticated, )
    serializer_class = SetSavedCardDefaultSerializer

    def post(self, request):
        user = self.request.user
        args = self.request.data
        token = args.get('token')
        print('args:', str(args))
        print('token:', str(token))
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
