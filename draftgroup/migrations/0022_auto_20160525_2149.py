# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0021_playerupdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update_id', models.CharField(null=True, max_length=64)),
                ('game_srid', models.CharField(max_length=64)),
                ('game_id', models.IntegerField(default=0)),
                ('category', models.CharField(choices=[('news', 'News'), ('lineup', 'Lineup')], default='news', max_length=64)),
                ('type', models.CharField(default='', max_length=128)),
                ('value', models.CharField(default='', max_length=8192)),
                ('draft_groups', models.ManyToManyField(to='draftgroup.DraftGroup')),
            ],
        ),
        migrations.AddField(
            model_name='playerupdate',
            name='type',
            field=models.CharField(default='', max_length=128),
        ),
    ]
