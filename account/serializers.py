#
# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import (
    Information,
    EmailNotification,
    UserEmailNotification,
    SavedCardDetails,
)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class UserSerializerNoPassword(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class InformationSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    def get_email(self, information):
        return information.user.email

    class Meta:
        model = Information
        fields = ("dob", "email", "fullname", "address1", "address2", "city", "state", "zipcode")


class EmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = ("id", "category", "name", "description", "deprecated")


class UserEmailNotificationSerializer(serializers.ModelSerializer):
    notification_info = EmailNotificationSerializer(source="email_notification")

    class Meta:
        model = UserEmailNotification
        fields = ("notification_info", "enabled")


class UpdateUserEmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmailNotification
        fields = ("id", "enabled")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

class SavedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedCardDetails
        fields = ('user','token','type','last_4','exp_month','exp_year','default')

class SetSavedCardDefaultSerializer(serializers.Serializer):
    token = serializers.CharField()

    # dont need default, because assume we are trying to set this one to the default
    #default = serializers.BooleanField()

class SavedCardAddSerializer(serializers.Serializer):
    type = serializers.CharField()
    number = serializers.CharField()
    exp_month = serializers.CharField()
    exp_year = serializers.CharField()
    cvv2 = serializers.CharField()

class SavedCardDeleteSerializer(serializers.Serializer):
    token = serializers.CharField()