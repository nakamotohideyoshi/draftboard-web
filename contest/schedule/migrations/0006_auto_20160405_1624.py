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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256, default='')),
                ('srid', models.CharField(max_length=128)),
                ('game_id', models.PositiveIntegerField()),
                ('block', models.ForeignKey(to='schedule.Block')),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='blockgame',
            unique_together=set([('block', 'srid')]),
        ),
    ]
