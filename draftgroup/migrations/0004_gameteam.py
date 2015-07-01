# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0003_auto_20150630_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('game_srid', models.CharField(max_length=64)),
                ('team_srid', models.CharField(max_length=64)),
                ('alias', models.CharField(max_length=64)),
                ('draft_group', models.ForeignKey(to='draftgroup.DraftGroup')),
            ],
        ),
    ]
