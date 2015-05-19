# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0003_auto_20150518_2349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerstats',
            old_name='save',
            new_name='saves',
        ),
    ]
