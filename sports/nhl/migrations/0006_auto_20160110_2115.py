# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0005_tsxinjury_tsxnews_tsxplayer_tsxteam_tsxtransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='injury',
            name='ddtimestamp',
            field=models.BigIntegerField(default=0, help_text='the time this injury update was parsed by dataden.this will be the same value for all objects that were in the feed on the last parse.'),
        ),
        migrations.AddField(
            model_name='tsxplayer',
            name='content_published',
            field=models.DateTimeField(default=datetime.datetime(1999, 1, 1, 12, 0, tzinfo=utc), help_text='the item ref is a GFK so also store the publish date here for ordering purposes.'),
        ),
        migrations.AddField(
            model_name='tsxplayer',
            name='player',
            field=models.ForeignKey(default=None, to='nhl.Player'),
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
            field=models.ForeignKey(default=None, to='nhl.Team'),
            preserve_default=False,
        ),
    ]
