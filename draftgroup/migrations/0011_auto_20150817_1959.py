# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0010_player_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='draft_group',
            field=models.ForeignKey(to='draftgroup.DraftGroup', verbose_name='the DraftGroup this player is a member of', related_name='players'),
        ),
    ]
