# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-15 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('dataden', '0001_initial'), ('dataden', '0002_livestatscacheconfig_trigger'), ('dataden', '0003_auto_20150513_0406'), ('dataden', '0004_auto_20160411_2117'), ('dataden', '0005_pbpdebug_timestamp_pushered'), ('dataden', '0006_pbpdebug_delta_seconds_valid')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LiveStatsCacheConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('key_timeout', models.IntegerField(default=1800)),
                ('timeout_mod', models.IntegerField(default=25, help_text='the percentage as an integer [25-100], of how much to randomize the key_timeout. 25 indicates +/-25%  If its set too low the database has a higher likelihood of getting big bursts of insert/updates')),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('enabled', models.BooleanField(default=True)),
                ('db', models.CharField(max_length=128)),
                ('collection', models.CharField(max_length=128)),
                ('parent_api', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='trigger',
            unique_together=set([('db', 'collection', 'parent_api')]),
        ),
        migrations.CreateModel(
            name='PbpDebug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=2048, null=True)),
                ('game_srid', models.CharField(max_length=128)),
                ('srid', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=2048, null=True)),
                ('xml_str', models.CharField(max_length=16384, null=True)),
                ('timestamp_pushered', models.DateTimeField(null=True)),
                ('delta_seconds_valid', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='pbpdebug',
            unique_together=set([('game_srid', 'srid')]),
        ),
    ]
