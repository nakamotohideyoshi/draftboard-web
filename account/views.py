from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

from account.models import Information, EmailNotification, UserEmailNotification
from account.permissions import IsNotAuthenticated
from account.serializers import (
    LoginSerializer,
    ForgotPasswordSerializer,
    PasswordResetSerializer,
    RegisterUserSerializer,
    UserSerializer,
    InformationSerializer,
    UserEmailNotificationSerializer,
    EmailNotificationSerializer
)
import account.tasks
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
            return Response(serializer.data)
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


class EmailNotificationAPIView (generics.ListCreateAPIView):
    """
    Allows the admin to modify and insert new Email Notifications

        * |api-text| :dfs:`account/email/notification/`
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)
    serializer_class = EmailNotificationSerializer
    queryset = EmailNotification.objects.all()


class UserEmailNotificationAPIView (generics.GenericAPIView):
    """
    Allows the user to get and update their user email settings

        * |api-text| :dfs:`account/email/settings/`
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = UserEmailNotificationSerializer

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

    def post(self, request, format=None):
        print(request.data)
        try:
            notif = EmailNotification.objects.get(
                deprecated=False,
                id=request.data['email_notification']
            )
        except EmailNotification.DoesNotExist:
            return Response("Notification does not exist", status=status.HTTP_400_BAD_REQUEST)

        user_email_notification = self.get_object(notif)

        serializer = UserEmailNotificationSerializer(
            user_email_notification, data=request.data, many=False
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
