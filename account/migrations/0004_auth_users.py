# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings

def load_initial_data(apps, schema_editor):
    """
    Loads the initial Auth Users(s). This function will be passed to 'migrations.RunPython' which supplies the arguments.

    :param apps:
    :param schema_editor:
    :return:
    """


    #
    # get the model by name
    user = apps.get_model('auth', 'User')
    draftboard = user.objects.create_user(username=settings.USERNAME_DRAFTBOARD, password="")
    draftboard.is_superuser   = False
    draftboard.is_staff       = True
    draftboard.save()

    escrow = user.objects.create_user(username=settings.USERNAME_ESCROW, password="")
    escrow.is_superuser   = False
    escrow.is_staff       = True
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
