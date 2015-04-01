from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Information, EmailNotification, UserEmailNotification

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( "email", "password")

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = ( "dob", "fullname", "address1", "address2", "city", "state", "zipcode")

class EmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = ("pk", "category", "name", "description", "default_value", "deprecated")

class UserEmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmailNotification
        fields = ("email_notification", "enabled")