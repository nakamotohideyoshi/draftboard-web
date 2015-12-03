# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0002_replay_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('loader_task_id', models.CharField(max_length=255, default=None, null=True)),
                ('playback_task_id', models.CharField(max_length=255, default=None, null=True)),
                ('replay', models.CharField(help_text='the filename of the replay fixture', default='', max_length=255)),
                ('loading_status', models.CharField(help_text='status of replay. initial -> loading -> playing', default='', max_length=255)),
                ('playback_status', models.CharField(help_text='status of replay. initial -> loading -> playing', default='', max_length=255)),
                ('start', models.DateTimeField(help_text='the time you want to start at in the replay. must be within the start and end of the recorded stats')),
                ('current', models.DateTimeField(help_text='the time you want to start at in the replay. must be within the start and end of the recorded stats')),
                ('playback_mode', models.CharField(choices=[('play-until-end', 'Play Until End'), ('paused', 'Paused')], max_length=64)),
            ],
        ),
    ]
