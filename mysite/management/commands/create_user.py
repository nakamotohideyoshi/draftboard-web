from pprint import pprint

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from account.models import (Information)
from account.serializers import RegisterUserSerializer


class Command(BaseCommand):
    """
    Since there are a number of steps that go into creating a user, we
    can't do it via the django admin panel.

    Usage:

        $> ./manage.py create_user <username> <email> <password>

    Example:
        python manage.py create_user user213 user213@gmail.com hunter2
    """

    # help is a Command inner variable
    help = 'usage: ./manage.py create_user <username> <email> <password>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('username', nargs='+', type=str)
        parser.add_argument('email', nargs='+', type=str)
        parser.add_argument('password', nargs='+', type=str)

    def handle(self, *args, **options):
        data = {
            'username': options['username'][0],
            'email': options['email'][0],
            'password': options['password'][0],
            'password_confirm': options['password'][0],
        }

        user_serializer = RegisterUserSerializer(data=data)

        if user_serializer.is_valid(raise_exception=False):
            try:
                with transaction.atomic():
                    username = user_serializer.validated_data.get('username')
                    email = user_serializer.validated_data.get('email')
                    password = user_serializer.validated_data.get('password')

                    user = User.objects.create(username=username, email=email)
                    user.set_password(password)
                    user.save()
                    # Make sure each user gets Information and Identity models
                    Information.objects.create(user=user)
                    new_user = authenticate(username=user.username, password=password)

                    print('\nUser account created succesfully!\n')
                    pprint(vars(new_user))
            except Exception as e:
                print('\nUSER NOT CREATED! Errors:\n')
                pprint(e)
        else:
            print('\nUSER NOT CREATED! Errors:\n')
            pprint(user_serializer.errors)
