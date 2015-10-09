# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0012_player_game_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpcomingDraftGroup',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('draftgroup.draftgroup',),
        ),
        migrations.AddField(
            model_name='draftgroup',
            name='category',
            field=models.CharField(null=True, max_length=32),
        ),
        migrations.AddField(
            model_name='draftgroup',
            name='num_games',
            field=models.IntegerField(help_text='the number of live games this draft group spans', default=0),
            preserve_default=False,
        ),
    ]
