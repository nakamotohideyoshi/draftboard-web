# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0011_auto_20150817_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='game_team',
            field=models.ForeignKey(to='draftgroup.GameTeam', default=None),
            preserve_default=False,
        ),
    ]
