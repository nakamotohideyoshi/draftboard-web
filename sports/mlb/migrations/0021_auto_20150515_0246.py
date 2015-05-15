# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0020_auto_20150515_0219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameboxscore',
            old_name='srid_hold',
            new_name='srid_blown_save',
        ),
    ]
