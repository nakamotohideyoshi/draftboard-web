# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0010_probablepitcher'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='probablepitcher',
            unique_together=set([('srid_game', 'srid_player')]),
        ),
    ]
