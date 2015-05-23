# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mlb', '0005_auto_20150522_0338'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePortion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game this is associate with')),
                ('game_id', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=32, default='', help_text='typically one of these: ["inning-half","quarter","period"]')),
                ('sequence', models.IntegerField(default=0, help_text='an ordering of all GamePortions with the same srid_game')),
                ('game_type', models.ForeignKey(related_name='mlb_gameportion_sport_game', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
