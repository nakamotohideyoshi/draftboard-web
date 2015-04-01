from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from account.serializers import RegisterUserSerializer, UserSerializer, InformationSerializer, UserEmailNotificationSerializer, EmailNotificationSerializer
from django.contrib.auth.models import User
from account.models import Information, EmailNotification, UserEmailNotification
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from account.permissions import IsNotAuthenticated


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
            #
            # The serializer does not check if the email field is None
            if email == None:
                return Response("Email is required", status=status.HTTP_400_BAD_REQUEST)

            password = data.get('password')
            user = User.objects.create(username=username,  email= email)
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
        notifications = EmailNotification.objects.filter(deprecated = False)
        for notif in notifications:
            self.get_object(notif)

        return UserEmailNotification.objects.filter(user = user)

    def get_object(self, notif):
        user = self.request.user

        try:
            email_notif = UserEmailNotification.objects.get(user = user,
                                            email_notification  = notif )
        except UserEmailNotification.DoesNotExist:
            #
            # Creates the corresponding email notification
            email_notif = UserEmailNotification()
            email_notif.email_notification= notif
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
            notif = EmailNotification.objects.get(deprecated = False, id = request.data['email_notification'])
        except EmailNotification.DoesNotExist:
            return Response("Notification does not exist", status=status.HTTP_400_BAD_REQUEST)

        user_email_notification = self.get_object(notif)

        serializer = UserEmailNotificationSerializer(user_email_notification, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

