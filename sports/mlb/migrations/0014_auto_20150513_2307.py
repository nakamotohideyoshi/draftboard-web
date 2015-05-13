# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0013_auto_20150513_2307'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='playerstatshitter',
            unique_together=set([('player', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='playerstatspitcher',
            unique_together=set([('player', 'game')]),
        ),
    ]
