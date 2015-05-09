# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataden', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveStatsCacheConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('key_timeout', models.IntegerField(default=1800)),
                ('timeout_mod', models.IntegerField(default=25, help_text='the percentage as an integer [25-100], of how much to randomize the key_timeout. 25 indicates +/-25%  If its set too low the database has a higher likelihood of getting big bursts of insert/updates')),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('enabled', models.BooleanField(default=True)),
                ('db', models.CharField(max_length=128)),
                ('collection', models.CharField(max_length=128)),
                ('parent_api', models.CharField(max_length=128)),
            ],
        ),
    ]
