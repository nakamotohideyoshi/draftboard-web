# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0008_player_on_active_roster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='status',
            field=models.CharField(max_length=64, help_text='roster status - ie: "A01" means they are ON the roster. Not particularly active as in not-injured!', default=''),
        ),
    ]
