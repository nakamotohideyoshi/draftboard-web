# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('schedule', '0005_auto_20160405_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockGame',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=256)),
                ('srid', models.CharField(max_length=128)),
                ('game_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.RenameField(
            model_name='block',
            old_name='start',
            new_name='dfsday_start',
        ),
        migrations.AddField(
            model_name='block',
            name='cutoff_time',
            field=models.TimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='block',
            name='dfsday_end',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='block',
            unique_together=set([('site_sport', 'dfsday_start', 'dfsday_end', 'cutoff_time')]),
        ),
        migrations.AddField(
            model_name='blockgame',
            name='block',
            field=models.ForeignKey(to='schedule.Block'),
        ),
        migrations.AddField(
            model_name='blockgame',
            name='game_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AlterUniqueTogether(
            name='blockgame',
            unique_together=set([('block', 'srid')]),
        ),
    ]
