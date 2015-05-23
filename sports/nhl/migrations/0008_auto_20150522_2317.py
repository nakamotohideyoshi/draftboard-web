# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0007_gameportion_srid_period'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameportion',
            old_name='srid_period',
            new_name='srid',
        ),
    ]
