# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0007_auto_20160315_1927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerstatshitter',
            old_name='play',
            new_name='played',
        ),
        migrations.RenameField(
            model_name='playerstatshitter',
            old_name='start',
            new_name='started',
        ),
        migrations.RenameField(
            model_name='playerstatspitcher',
            old_name='play',
            new_name='played',
        ),
        migrations.RenameField(
            model_name='playerstatspitcher',
            old_name='start',
            new_name='started',
        ),
    ]
