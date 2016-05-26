# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0019_player_starter_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='starter_info',
        ),
    ]
