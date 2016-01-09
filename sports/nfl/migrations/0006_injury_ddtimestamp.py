# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0005_tsxinjury_tsxnews_tsxplayer_tsxteam_tsxtransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='injury',
            name='ddtimestamp',
            field=models.IntegerField(help_text='the time this injury update was parsed by dataden.this will be the same value for all objects that were in the feed on the last parse.', default=0),
        ),
    ]
