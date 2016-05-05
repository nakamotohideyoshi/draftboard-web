# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0009_auto_20160409_1845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestpool',
            options={'verbose_name_plural': 'Contest Pools (All)', 'verbose_name': 'Contest Pools (All)'},
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(max_length=64, default='', help_text='frontfacing name', verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='contestpool',
            name='name',
            field=models.CharField(max_length=64, default='', help_text='frontfacing name', verbose_name='Name'),
        ),
    ]
