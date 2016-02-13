# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0016_auto_20160209_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='final_fantasy_points',
            field=models.FloatField(default=0, help_text='the payout-time fantasy points of this player'),
        ),
    ]
