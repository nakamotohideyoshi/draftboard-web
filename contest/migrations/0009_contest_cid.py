# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0008_auto_20150703_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='cid',
            field=models.CharField(max_length=6, default='', editable=False, help_text='unique, randomly chosen when Contest is created', blank=True),
        ),
    ]
