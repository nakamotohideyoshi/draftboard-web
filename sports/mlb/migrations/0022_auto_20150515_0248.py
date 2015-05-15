# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0021_auto_20150515_0246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameboxscore',
            name='srid_blown_save',
        ),
        migrations.RemoveField(
            model_name='gameboxscore',
            name='srid_save',
        ),
    ]
