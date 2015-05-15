# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0017_gameboxscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameboxscore',
            name='title',
            field=models.CharField(max_length=256, default=''),
        ),
    ]
