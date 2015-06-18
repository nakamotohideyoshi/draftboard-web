# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0003_auto_20150612_2112'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ActualCash',
        ),
        migrations.DeleteModel(
            name='ActualTicket',
        ),
        migrations.AlterUniqueTogether(
            name='cash',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='cash',
            name='prize_structure',
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='prize_structure',
        ),
        migrations.DeleteModel(
            name='Cash',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
