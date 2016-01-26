# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from sports.classes import SiteSportManager
from roster.classes import Initial

def load_initial_data(apps, schema_editor):
    """
    delete any existing RosterSpotPositions, and then any RosterSpots,
    then create the new rosters.

    :param apps:
    :param schema_editor:
    :return:
    """

    # get the two models required for creating lineup rosters
    RosterSpotPosition  = apps.get_model('roster',  'RosterSpotPosition')
    RosterSpot          = apps.get_model('roster',  'RosterSpot')

    # delete everything
    RosterSpotPosition.objects.all().delete()
    RosterSpot.objects.all().delete()

    # create the new rosters for each sport
    for sport in SiteSportManager.SPORTS:
        initial = Initial()
        initial.setup(sport)

class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        ('roster', '0002_auto_20150529_0216'),
    ]

    operations = [
        #
        # make the initial rosters
        migrations.RunPython( load_initial_data ),
    ]


