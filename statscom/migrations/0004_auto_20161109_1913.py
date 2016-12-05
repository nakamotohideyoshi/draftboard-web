# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-09 19:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('statscom', '0003_auto_20160831_1633'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playerlookup',
            options={'ordering': ('last_name', 'first_name', 'created')},
        ),
        migrations.RemoveField(
            model_name='playerlookup',
            name='player',
        ),
        migrations.AddField(
            model_name='playerlookup',
            name='player_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playerlookup',
            name='player_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statscom_playerlookup_player_lookup', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='playerlookup',
            name='pid',
            field=models.CharField(max_length=255),
        ),
    ]
