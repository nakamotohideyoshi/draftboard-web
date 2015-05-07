# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keyprefix', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyPrefix',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('prefix', models.CharField(max_length=8)),
            ],
        ),
    ]
