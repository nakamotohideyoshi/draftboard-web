# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0014_auto_20150319_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentDraftGroup',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('draftgroup.draftgroup',),
        ),
        migrations.AddField(
            model_name='draftgroup',
            name='closed',
            field=models.DateTimeField(null=True, help_text='the time at which all live games in the draft group were closed out and stats were finalized by the provider', blank=True),
        ),
    ]
