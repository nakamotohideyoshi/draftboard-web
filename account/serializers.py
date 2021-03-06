from re import search

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from account.blacklist import BLACKLIST
from account.models import (
    EmailNotification,
    UserEmailNotification,
    SavedCardDetails,
    Limit,
    Identity,
)


class UserIdentitySerializer(serializers.ModelSerializer):
    """
    Serializer for User.Identity. This gets nested in UserSerializer.
    """

    class Meta:
        model = Identity
        fields = ('country', 'region', 'status')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for general user information.
    This is the response payload for /api/account/user/
    """
    identity_verified = serializers.SerializerMethodField()
    cash_balance = serializers.SerializerMethodField()
    cash_balance_formatted = serializers.SerializerMethodField()
    has_created_a_lineup = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    identity = UserIdentitySerializer(read_only=True)

    @staticmethod
    def get_identity_verified(user):
        # Bypass this if they have the permission.
        if user.has_perm('account.can_bypass_identity_verification'):
            return True
        # Has the user verified their identity with GIDX?
        return user.information.has_verified_identity

    @staticmethod
    def get_cash_balance(user):
        return user.information.cash_balance

    @staticmethod
    def get_has_created_a_lineup(user):
        return user.information.has_created_a_lineup

    @staticmethod
    def get_cash_balance_formatted(user):
        # A string formatted to 2 decimal places and a dollar sign ("$99,997.40")
        return "${:,.2f}".format(user.information.cash_balance)

    @staticmethod
    def get_permissions(user):
        # A list of user permissions.
        return {
            'is_staff': user.is_staff,
            'can_bypass_location_check': user.has_perm('account.can_bypass_location_check'),
            'can_bypass_age_check': user.has_perm('account.can_bypass_age_check'),
            'can_bypass_identity_verification': user.has_perm(
                'account.can_bypass_identity_verification')
        }

    class Meta:
        model = User
        fields = (
            "username", "email", "identity_verified", "cash_balance", "cash_balance_formatted",
            "has_created_a_lineup", "permissions", "identity",)


class UserCredentialsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")


class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    # We don't currently require password confirmation.
    # password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def return_no_password(self, obj):
        """
        Make sure password is never given back, even encrypted
        """
        return None

    @staticmethod
    def validate_email(value):
        error_message = 'This email/username is not valid.'

        # First, validate the email with django's validators.
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError(error_message)

        """
        Extra check on email for whether it's in use
        """
        UserModel = get_user_model()

        if value is None or value == '' or UserModel.objects.filter(
                email__iexact=value).count() > 0:
            # notice how i don't say the email already exists, prevents people from
            # hacking to find someone's email
            raise serializers.ValidationError(error_message)

        return value

    @staticmethod
    def validate_username(value):
        """
        Validation method to ensure that the username is valid, of proper length and unique
        """
        UserModel = get_user_model()

        if value in BLACKLIST:
            raise serializers.ValidationError('This username is in a black list.')

        if UserModel.objects.filter(username__iexact=value).count() > 0:
            # notice how i don't say the email already exists, prevents people from
            # hacking to find someone's email
            raise serializers.ValidationError('This email/username is not valid.')

        if not search(r'^%s{3,}$' % '[a-zA-Z0-9_.-]', value):
            raise serializers.ValidationError('Must be 3 or more alphanumeric characters.')

        return value

    @staticmethod
    def validate_password(value):
        if value:
            if len(value) < 8:
                raise serializers.ValidationError(
                    'The password must be a minimum 8 characters in length.')
        else:
            raise serializers.ValidationError('You must provide a password.')
        return value


class UserSerializerNoPassword(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


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


class VerifyUserIdentitySerializer(serializers.Serializer):
    first = serializers.CharField(max_length=100)
    last = serializers.CharField(max_length=100)
    birth_day = serializers.IntegerField(min_value=1, max_value=31)
    birth_month = serializers.IntegerField(min_value=1, max_value=12)
    birth_year = serializers.IntegerField(min_value=1900, max_value=9999)


class LimitsListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        limit_mapping = {limit.type: limit for limit in instance}
        data_mapping = {item['type']: item for item in validated_data}

        # Perform updates.
        updated = []
        for limit_type, data in data_mapping.items():
            limit = limit_mapping.get(limit_type, None)

            updated.append(self.child.update(limit, data))
        return updated


class UserLimitsSerializer(serializers.ModelSerializer):
    """
    Serializer for user limits.
    """

    class Meta:
        model = Limit
        field = ('type', 'value', 'time_period')
        list_serializer_class = LimitsListSerializer
