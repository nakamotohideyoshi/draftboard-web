# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0005_tsxinjury_tsxnews_tsxplayer_tsxteam_tsxtransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='injury',
            name='ddtimestamp',
            field=models.BigIntegerField(help_text='the time this injury update was parsed by dataden.this will be the same value for all objects that were in the feed on the last parse.', default=0),
        ),
        migrations.AddField(
            model_name='tsxplayer',
            name='content_published',
            field=models.DateTimeField(help_text='the item ref is a GFK so also store the publish date here for ordering purposes.', default=datetime.datetime(1999, 1, 1, 12, 0, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='tsxplayer',
            name='player',
            field=models.ForeignKey(default=None, to='mlb.Player'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tsxteam',
            name='content_published',
            field=models.DateTimeField(help_text='the item ref is a GFK so also store the publish date here for ordering purposes.', default=datetime.datetime(1999, 1, 1, 12, 0, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='tsxteam',
            name='team',
            field=models.ForeignKey(default=None, to='mlb.Team'),
            preserve_default=False,
        ),
    ]
