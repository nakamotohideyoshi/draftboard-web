# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replay',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=256)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('ts', models.DateTimeField()),
                ('ns', models.CharField(max_length=64)),
                ('o', models.CharField(max_length=8192)),
            ],
        ),
    ]
