# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def load_initial_data(apps, schema_editor):
    """
    adds

    :param apps:
    :param schema_editor:
    :return:
    """

    data = [
        {
            'category'      : 'contest',
            'name'          : 'starting',
            'description'   : 'contest have started',
            'displayed_text': 'Contests are starting',
            'default_value' : True,
            'deprecated'    : False
        },
        {
            'category'      : 'contest',
            'name'          : 'prizes-paid',
            'description'   : 'user has won money from contests',
            'displayed_text': 'Contest victories',
            'default_value' : True,
            'deprecated'    : False
        },
        {
            'category'      : 'campaign',
            'name'          : 'newsletter',
            'description'   : 'whether to send the newsletter',
            'displayed_text': 'Newsletter',
            'default_value' : True,
            'deprecated'    : False
        },
        {
            'category'      : 'contest',
            'name'          : 'starting-soon',
            'description'   : 'user has contests which are starting soon',
            'displayed_text': 'Upcoming contests',
            'default_value' : True,
            'deprecated'    : False
        },
    ]

    # get the model by name
    EmailNotification = apps.get_model('account', 'EmailNotification')

    for obj in data:

        try:
            n = EmailNotification.objects.get( category=obj['category'],
                                               name=obj['name'])
        except EmailNotification.DoesNotExist:
            n = EmailNotification()

            #
            # set the data['fields'] to the email notification
            n.category          = obj['category']
            n.name              = obj['name']
            n.description       = obj['description']
            n.displayed_text    = obj['displayed_text']
            n.default_value     = obj['default_value']
            n.deprecated        = obj['deprecated']
            n.save()

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auth_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailnotification',
            name='displayed_text',
            field=models.CharField(max_length=512, default='', help_text='this text is shown to users'),
        ),

        #
        # additionally, run function to load the initial objects
        migrations.RunPython( load_initial_data )
    ]
