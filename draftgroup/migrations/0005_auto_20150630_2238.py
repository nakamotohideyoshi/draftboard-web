# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0004_gameteam'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameteam',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameteam',
            name='game_start',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
