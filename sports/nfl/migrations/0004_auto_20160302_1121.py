# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def load_initial_data(apps, schema_editor):
    """
    adds a dummy Season object to facillitate the migratino of older
    Game objects which cant have a foreign key to a null Season!

    :param apps:
    :param schema_editor:
    :return:
    """

    # get the model by name
    sport = 'nfl'
    Season = apps.get_model(sport, 'Season')
    try:
        # this must exist for migration to work
        season = Season.objects.get(pk=1)
    except Season.DoesNotExist:
        season = Season()
        season.srid = '%s_dummy_srid' % sport
        season.season_year = 0
        season.season_type = '%s_dummy_season_type' % sport
        season.save()

class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0003_auto_20160229_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='season',
            name='start_year',
        ),

        migrations.AddField(
            model_name='season',
            name='season_year',
            field=models.IntegerField(default=0, help_text='the year the season started'),
        ),
        migrations.AddField(
            model_name='season',
            name='srid',
            field=models.CharField(default=None, help_text='the sportsradar global id of the season/schedule', max_length=64, unique=True),
            preserve_default=False,
        ),

        # add dummy/initial Season
        migrations.RunPython(
            load_initial_data
        ),

        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(to='nfl.Season', default=1),
            preserve_default=False,
        ),
    ]
