# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mlb', '0002_auto_20150520_0352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameboxscore',
            name='away',
        ),
        migrations.RemoveField(
            model_name='gameboxscore',
            name='home',
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='away_id',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='away_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType', related_name='mlb_gameboxscore_away_team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='home_id',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='home_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType', related_name='mlb_gameboxscore_home_team'),
            preserve_default=False,
        ),
    ]
