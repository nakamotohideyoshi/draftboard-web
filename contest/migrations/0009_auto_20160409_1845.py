# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0008_livecontestpool'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CurrentContestPool',
        ),
        migrations.AlterModelOptions(
            name='lobbycontestpool',
            options={'verbose_name_plural': 'Contest Pools (Lobby)', 'verbose_name': 'Contest Pools (Lobby)'},
        ),
    ]
