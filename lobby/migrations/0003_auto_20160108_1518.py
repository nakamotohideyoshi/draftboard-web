# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0002_contestbanner_promotionbanner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestbanner',
            options={'ordering': ['priority']},
        ),
        migrations.AddField(
            model_name='contestbanner',
            name='priority',
            field=models.IntegerField(help_text='1 = highest priority, 1 > 2 > 3... etc...', default=1),
        ),
        migrations.AddField(
            model_name='promotionbanner',
            name='priority',
            field=models.IntegerField(help_text='1 = highest priority, 1 > 2 > 3... etc...', default=1),
        ),
    ]
