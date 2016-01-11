# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0007_injury_ddtimestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='tsxplayer',
            name='content_published',
            field=models.DateTimeField(default=datetime.datetime(1999, 1, 1, 12, 0, tzinfo=utc), help_text='the item ref is a GFK so also store the publish date here for ordering purposes.'),
        ),
        migrations.AddField(
            model_name='tsxplayer',
            name='player',
            field=models.ForeignKey(to='nba.Player', default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tsxteam',
            name='content_published',
            field=models.DateTimeField(default=datetime.datetime(1999, 1, 1, 12, 0, tzinfo=utc), help_text='the item ref is a GFK so also store the publish date here for ordering purposes.'),
        ),
        migrations.AddField(
            model_name='tsxteam',
            name='team',
            field=models.ForeignKey(to='nba.Team', default=None),
            preserve_default=False,
        ),
    ]
