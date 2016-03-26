# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0005_auto_20160321_2239'),
    ]

    operations = [
        migrations.CreateModel(
            name='LobbyContestPool',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contestpool',),
        ),
        migrations.AddField(
            model_name='entry',
            name='contest_pool',
            field=models.ForeignKey(related_name='contest_pools', null=True, to='contest.ContestPool'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='contest',
            field=models.ForeignKey(related_name='contests', null=True, to='contest.Contest'),
        ),
    ]
