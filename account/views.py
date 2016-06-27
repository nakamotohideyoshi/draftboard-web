from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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
    EmailNotificationSerializer,
    UpdateUserEmailNotificationSerializer,
    SavedCardSerializer,
    SetSavedCardDefaultSerializer,
    SavedCardAddSerializer,
    # TODO there are a few more things
)
import account.tasks
from pp.classes import (
    CardData,
)
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import loader
from rest_framework import response, status
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import permissions
# from rest_framework.generics import CreateAPIView
# from django.contrib.auth import get_user_model # If used custom user model
# /password/reset/confirm/{uid}/{token}
from django.contrib.auth import authenticate, login, logout

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
            login(request, user)
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
            # The serializer does not check if the email field is None
            if email is None:
                return Response("Email is required", status=status.HTTP_400_BAD_REQUEST)

            password = data.get('password')
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
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
    authentication_classes = (SessionAuthentication, BasicAuthentication)
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

class RegisterView(TemplateView):

    template_name = 'registration/register.html'

#
##########################################################
# PayPal specific views
###########################################################
class PayPalDepositWithPayPalAccountAPIView(APIView): pass          # TODO
class PayPalDepositWithPayPalAccountSuccessAPIView(APIView): pass   # TODO
class PayPalDepositWithPayPalAccountFailAPIView(APIView): pass      # TODO

class PayPalDepositCreditCardAPIView(APIView): pass                 # TODO

class PayPalDepositSavedCardAPIView(APIView): pass                  # TODO

class PayPalSavedCardAddAPIView(APIView):
    """
    the first card added will be set to be the default saved card
    """

    authentication_classes = (IsAuthenticated, )
    serializer_class = SavedCardAddSerializer

    def __create_paypal_saved_card(self, asdf): # TODO - finish/test
        """
        using paypal api, try to save a card, and return the data
        """
        pass # TODO

    def __create_saved_card_details(self, token, user, type, number, exp_month, exp_year, cvv2): # TODO - finish/test
        """
        once we have successfully saved a card using paypal's api,
        create a reference to that saved card (especially the token)
        in our own backened.
        """

        #
        #####################
        # paypal api stuff
        #####################
        card_data = CardData()
        card_data.set_card_field(CardData.EXTERNAL_CUSTOMER_ID, user.username)
        card_data.set_card_field(CardData.TYPE, type)
        card_data.set_card_field(CardData.NUMBER, number)

        #
        #####################
        # server side stuff
        #####################
        default = False
        # check if any previously saved cards
        existing_saved_cards = SavedCardDetails.objects.filter(user=user)
        if existing_saved_cards.count() > 0:
            default = True

        # # get the card type properties so we can create a SavedCardDetails instance
        # token       = None # TODO
        # card_type   = None # TODO
        # last_4      = None # TODO
        # exp_month   = None # TODO
        # exp_year    = None # TODO

        # create the new card
        saved_card = SavedCardDetails()
        saved_card.token = token
        saved_card.user = user
        saved_card.type = type
        saved_card.last_4 = last_4
        saved_card.exp_month = exp_month
        saved_card.exp_year = exp_year
        saved_card.default = default
        saved_card.save()
        return saved_card

    def post(self, request, *args, **kwargs):
        user = self.request.user
        args = self.request.data

        # get the card type properties so we can create a SavedCardDetails instance
        token       = None # TODO
        card_type   = None # TODO
        last_4      = None # TODO
        exp_month   = None # TODO
        exp_year    = None # TODO
        cvv2        = None # TODO - necessary for paypal api call

        saved_card = self.__create_saved_card_details(token, user, card_type, last_4, exp_month, exp_year, cvv2)

class PayPalSavedCardDeleteAPIView(APIView): pass                   # TODO

class PayPalSavedCardListAPIView(APIView):
    """
    get a list of the saved cards.

    these cards have an id which can be used to
    quickly deposit money to the site.
    """

    authentication_classes = (IsAuthenticated, )
    response_serializer = SavedCardSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        print('PayPalSavedCardListAPIView user:', user)

        saved_cards = None
        try:
            saved_cards = SavedCardDetails.objects.filter(user=user)
        except TypeError:
           return Response(status=405)

        # serialize the list of saved cards
        serialized_data = self.response_serializer(saved_cards, many=True).data
        return Response(serialized_data)

class SetSavedCardDefaultAPIView(APIView):
    """
    the arguments to this method should be passed
    in the POST as application/json, ie: {"token":"theToken"}
    """
    authentication_classes = (IsAuthenticated, )
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
        enabled_cards = saved_cards.filter(token=token) # filter() returns a queryset
        if enabled_cards.count() >= 1:
            # update all the cards to default=False
            saved_cards.update(default=False)
            # update this card to default=True
            card = enabled_cards[0]
            card.default = True
            card.save()

        # return success response of simply http 200
        return Response(status=200)

# In [1]: from account.models import SavedCardDetails
# In [2]: saved_card = SavedCardDetails()
# In [3]: from django.contrib.auth.models import User
# In [4]: user = User.objects.get(username='admin')
# In [5]: saved_card.user = user
# In [6]: saved_card.type = 'visa'
# In [7]: saved_card.last_4 =
# In [8]: saved_card.exp_month = '11'
# In [9]: saved_card.exp_year = 2017
# In [10]: saved_card.default = True
# In [11]: saved_card.save()
