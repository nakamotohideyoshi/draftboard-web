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
    RegisterUserSerializer,
    UserSerializer,
    InformationSerializer,
    UserEmailNotificationSerializer,
    EmailNotificationSerializer,
)
from braces.views import LoginRequiredMixin


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

    def put(self, request, format=None):
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

    def put(self, request, format=None):
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

        serializer = UserEmailNotificationSerializer(user_email_notification, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountSettingsView(LoginRequiredMixin, TemplateView):

    template_name = 'account/settings.html'


class DepositView(LoginRequiredMixin, TemplateView):

    template_name = 'account/deposits.html'


class WithdrawalView(LoginRequiredMixin, TemplateView):

    template_name = 'account/withdrawals.html'


class TransactionsView(LoginRequiredMixin, TemplateView):

    template_name = 'account/transactions.html'


class UserBasicAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        return Response({
            'username': 'fancyusername',
            'email': 'example@dfs.com',
            'balance': '23130.00',
            'bonus': '3130.00',
            'emailNotifications': {
                'contests_starting': True,
                'contests_victories': True,
                'contests_upcoming': True,
                'newsletters': False
            },
            'name': 'Lookma Noname',
            'address1': 'Some address or should it',
            'address2': 'Be connected with specific payment method',
            'city': 'Denver',
            'state': 'Colorado',
            'stateShort': 'CO',
            'zipcode': '4000'
        })

    def post(self, request, *args, **kwargs):
        import random
        errors = random.choice([0, 1, 2, 3])

        if errors == 0:
            return Response(status=200)

        return Response(
            status=409,
            data={
                'errors': {
                    'email': {
                        'title': 'Email already taken!',
                        'description': 'It looks like this email is already taken by another user. Please choose a different one.'
                    }
                }
            })


class UserInformationAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        return Response({
            'name': 'Lookma Noname',
            'address1': 'Some address or should it',
            'address2': 'Be connected with specific payment method',
            'city': 'Denver',
            'state': 'Colorado',
            'stateShort': 'CO',
            'zipcode': '4000'
        })

    def post(self, request, *args, **kwargs):
        import random
        errors = random.choice([0, 1, 2, 3])

        if errors == 0:
            return Response(status=200)

        return Response(
            status=409,
            data={
                'errors': {
                    'name': {
                        'title': 'Name you have..not.',
                        'description': 'You must provide us with your name. It is probably not that unique so no need to hide!'
                    }
                }
            })


class WithdrawAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def post(self, request, *args, **kwargs):
        return Response(
            status=409,
            data={
                'errors': {
                    'ssn': {
                        'title': 'SSN needed.',
                        'description': 'By law restrictions, if you are willing to withdraw more than $700, ssn is needed.'
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


class TransactionsAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        return Response([
            {
                'date_date': '04/24/2015',
                'date_time': '7:15:32 PM',
                'amount': '$1,300.32',
                'balance': '$2,249.32',
                'type': 'GPP',
                'description': 'Contest with multiple entries.',
                'pk': 1
            },
            {
              'date_date': '11/32/2015',
              'date_time': '7:15:32 PM',
              'amount': '$1,300.32',
              'balance': '$2,249.32',
              'type': 'GPP',
              'description': 'Contest with multiple entries.',
              'pk': 2
            },
            {
              'date_date': '04/24/20',
              'date_time': '7:15:32 PM',
              'amount': '$1,300.32',
              'balance': '$2,249.32',
              'type': 'GPP',
              'description': 'Contest with multiple entries.',
              'pk': 3
            },
            {
              'date_date': '04/24/20',
              'date_time': '7:15:32 PM',
              'amount': '$1,300.32',
              'balance': '$2,249.32',
              'type': 'GPP',
              'description': 'Contest with multiple entries.',
              'pk': 4
            }
        ])


class TransactionHistoryAPI(APIView):

    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        return Response({
            'pk': 2,
            'number': '00823432',
            'status': 'completed',
            'transaction_type': 'Contest Result',
            'transaction_description': 'Payout from contest with ID 23401230',
            'fee': '$25',
            'prize-pool': '$150,000',
            'date_date': '11/32/15',
            'date_time': '7:15:32 PM',
            'amount': '$1,300.32',
            'balance': '$2,249.32',
            'type': 'GPP',
            'description': 'Contest with multiple entries.',
            'standings': [
            ],
            'scorings': [
            ],
            'prizes': [
            ],
            'teams': [
            ]
        })
