# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0018_draftgroup_fantasy_points_finalized'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='starter_info',
            field=models.CharField(max_length='64', null=True),
        ),
    ]
