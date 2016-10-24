#
# serializers.py

from re import search
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import (
    Information,
    EmailNotification,
    UserEmailNotification,
    SavedCardDetails,
)
from cash.classes import CashTransaction
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for general user information.
    This is the response payload for /api/account/user/
    """
    identity_verified = serializers.SerializerMethodField()
    cash_balance = serializers.SerializerMethodField()
    cash_balance_formatted = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    def get_identity_verified(self, user):
        # Has the user verified their identity with Trulioo? If they have there will be a
        # user.identity model.
        is_verified = False
        try:
            is_verified = (user.identity is not None)
        except ObjectDoesNotExist:
            pass
        return is_verified

    def get_cash_balance(self, user):
        # Unformatted float (99997.4)
        cash_transaction = CashTransaction(user)
        return cash_transaction.get_balance_amount()

    def get_cash_balance_formatted(self, user):
        # A string formatted to 2 decimal places and a dollar sign ("$99,997.40")
        cash_transaction = CashTransaction(user)

        return "${:,.2f}".format(cash_transaction.get_balance_amount())

    def get_permissions(self, user):
        # A list of user permissions.
        return {
            'is_staff': user.is_staff
        }

    class Meta:
        model = User
        fields = (
            "username", "email", "identity_verified", "cash_balance", "cash_balance_formatted",
            "permissions")


class UserCredentialsSerializer(serializers.ModelSerializer):
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


# This serializer was re-defined with the same name as the one above...
# I don't think this one is needed but I'll keep it here just in case.
#
# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ("email", "password")


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm")

    def return_no_password(self, obj):
        """
        Make sure password is never given back, even encrypted
        """
        return None

    def validate_email(self, value):
        """
        Extra check on email for whether it's in use
        """
        UserModel = get_user_model()

        if UserModel.objects.filter(email__iexact=value):
            # notice how i don't say the email already exists, prevents people from
            # hacking to find someone's email
            raise serializers.ValidationError('This email/username is not valid.')

        return value

    def validate_username(self, value):
        """
        Validation method to ensure that the username is valid, of proper length and unique
        """
        UserModel = get_user_model()

        if UserModel.objects.filter(username__iexact=value):
            # notice how i don't say the email already exists, prevents people from
            # hacking to find someone's email
            raise serializers.ValidationError('This email/username is not valid.')

        # TODO add in blacklist of usernames

        if not search(r'^%s{3,}$' % '[a-zA-Z0-9_.-]', value):
            raise serializers.ValidationError('Must be 3 or more alphanumeric characters.')

        return value

    def validate(self, data):
        """
        Check length and password strength
        """
        if 'password' in data and 'password_confirm' in data:
            pw1 = data['password']
            pw2 = data['password_confirm']
            if pw1 != pw2:
                raise serializers.ValidationError('The two password fields didn\'t match.')

            if len(pw1) < 8:
                raise serializers.ValidationError(
                    'The password must be a minimum 8 characters in length')

        elif 'password' in data or 'password_confirm' in data:
            raise serializers.ValidationError('You must submit matching passwords')

        return data


class UserSerializerNoPassword(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)


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
        fields = ('user', 'token', 'type', 'last_4', 'exp_month', 'exp_year', 'default')


class SetSavedCardDefaultSerializer(serializers.Serializer):
    token = serializers.CharField()

    # dont need default, because assume we are trying to set this one to the default
    # default = serializers.BooleanField()


class SavedCardAddSerializer(serializers.Serializer):
    type = serializers.CharField()
    number = serializers.CharField()
    exp_month = serializers.CharField()
    exp_year = serializers.CharField()
    cvv2 = serializers.CharField()


class SavedCardDeleteSerializer(serializers.Serializer):
    token = serializers.CharField()


class SavedCardPaymentSerializer(serializers.Serializer):
    token = serializers.CharField()
    # amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.FloatField()


class CreditCardPaymentSerializer(SavedCardAddSerializer):
    """
    Note: we also get a bunch of fields from the inherited serializer...
    """

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    amount = serializers.FloatField()


class TruliooVerifyUserSerializer(serializers.Serializer):
    first = serializers.CharField(max_length=100)
    last = serializers.CharField(max_length=100)
    birth_day = serializers.IntegerField(min_value=1, max_value=31)
    birth_month = serializers.IntegerField(min_value=1, max_value=12)
    birth_year = serializers.IntegerField(min_value=1900, max_value=9999)
    postal_code = serializers.CharField(max_length=16)
    # This is 11 to allow the use of separator dashes.
    ssn = serializers.CharField(max_length=11)
