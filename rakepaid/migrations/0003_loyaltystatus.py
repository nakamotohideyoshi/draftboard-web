# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from rakepaid.classes import LoyaltyStatusManager

def load_initial_data(apps, schema_editor):
    """
    load the initial loyalty tiers from rakepaid/classes.py LoyaltyStatusManager
    """

    #
    # get the model by name
    LoyaltyStatus = apps.get_model('rakepaid', 'LoyaltyStatus')
    for s in LoyaltyStatusManager.DEFAULT_STATUSES:
        status, created = LoyaltyStatus.objects.get_or_create( name=s.get('name'),
                                        rank=s.get('rank'),
                                        thirty_day_avg=s.get('thirty_day_avg'),
                                        multiplier=s.get('multiplier') )

class Migration(migrations.Migration):

    dependencies = [
        ('rakepaid', '0002_auto_20150731_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoyaltyStatus',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=32)),
                ('rank', models.IntegerField(default=0)),
                ('thirty_day_avg', models.FloatField(help_text='the minimum required base fpp earned in the last 30 days to achieve this status', default=0)),
                ('multiplier', models.FloatField(default=1.0)),
            ],
        ),

        #
        # additionally, run function to load the initial objects
        migrations.RunPython( load_initial_data )
    ]
