# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0009_player_salary'),
        ('lineup', '0002_lineup'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineup',
            name='draftgroup',
            field=models.ForeignKey(default=0, to='draftgroup.DraftGroup', null=None),
            preserve_default=False,
        ),
    ]
