# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0008_auto_20160108_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='tsxplayer',
            name='player',
            field=models.ForeignKey(to='nba.Player', default=None),
            preserve_default=False,
        ),
    ]
