# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0011_salary_avg_fppg_for_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='num_games_included',
            field=models.IntegerField(default=0),
        ),
    ]
