# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings
from django.contrib.auth.hashers import make_password

def load_initial_data(apps, schema_editor):
    """
    Loads the initial Auth Users(s). This function will be passed to 'migrations.RunPython' which supplies the arguments.

    :param apps:
    :param schema_editor:
    :return:
    """


    #
    # get the model by name
    User = apps.get_model('auth', 'User')
    password = User.objects.make_random_password()


    draftboard = User()
    draftboard.username= settings.USERNAME_DRAFTBOARD
    draftboard.password = make_password(password)
    draftboard.is_superuser = False
    draftboard.is_staff = True
    draftboard.save()

    escrow = User()
    escrow.username = settings.USERNAME_ESCROW
    escrow.password= make_password(password)
    escrow.is_superuser = False
    escrow.is_staff = True
    escrow.save()

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150428_0038'),
        ('auth', '0006_require_contenttypes_0002'),

    ]

    operations = [

        #
        # additionally, run function to load the initial objects
        migrations.RunPython( load_initial_data )
    ]
