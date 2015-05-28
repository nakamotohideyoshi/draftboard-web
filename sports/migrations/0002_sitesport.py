# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def load_initial_data(apps, schema_editor):
    """
    Loads the initial WithdrawStatus(s). This function will be passed to 'migrations.RunPython' which supplies the arguments.

    :param apps:
    :param schema_editor:
    :return:
    """
    #
    # get the model by name
    sports = ['nfl','mlb','nba','nhl']
    SiteSport = apps.get_model('sports', 'SiteSport')
    for sport in sports:
        model = SiteSport()
        model.name = sport
        model.save()

class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSport',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),

        #
        # additionally, run function to load the initial objects
        migrations.RunPython( load_initial_data )
    ]
