# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0008_auto_20150630_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='salary',
            field=models.FloatField(help_text='the amount of salary for the player at the this draft group was created', default=0),
        ),
    ]
