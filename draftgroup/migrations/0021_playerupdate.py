# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0020_remove_player_starter_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerUpdate',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update_id', models.CharField(null=True, max_length=64)),
                ('player_srid', models.CharField(max_length=64)),
                ('player_id', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=64, default='news', choices=[('news', 'News'), ('injury', 'Injury'), ('lineup', 'Lineup'), ('start', 'Start')])),
                ('value', models.CharField(max_length=8192, default='')),
                ('draft_groups', models.ManyToManyField(to='draftgroup.DraftGroup')),
            ],
        ),
    ]
