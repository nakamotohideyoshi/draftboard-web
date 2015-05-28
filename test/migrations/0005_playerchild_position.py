# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0003_auto_20150528_2131'),
        ('test', '0004_auto_20150527_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerchild',
            name='position',
            field=models.ForeignKey(default=None, to='sports.Position', related_name='test_playerchild_player_position'),
            preserve_default=False,
        ),
    ]
