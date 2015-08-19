# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0002_auto_20150625_1824'),
        ('contest', '0003_auto_20150630_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='draft_group',
            field=models.ForeignKey(verbose_name='DraftGroup', help_text='the pool of draftable players and their salaries, for the games this contest includes.', null=True, to='draftgroup.DraftGroup'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='end',
            field=models.DateTimeField(verbose_name='the time, after which real-life games will not be included in this contest', help_text='this field is overridden if the TodayOnly box is enabled'),
        ),
    ]
