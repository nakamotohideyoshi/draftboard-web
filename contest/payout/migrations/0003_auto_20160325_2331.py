# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payout', '0002_auto_20160209_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fpp',
            name='contest',
            field=models.ForeignKey(to='contest.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='payout',
            name='contest',
            field=models.ForeignKey(to='contest.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='rake',
            name='contest',
            field=models.ForeignKey(to='contest.Contest', null=True),
        ),
    ]
