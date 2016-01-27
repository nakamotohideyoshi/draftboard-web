# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_emailnotification_displayed_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailnotification',
            options={'verbose_name': 'Email Notification'},
        ),
        migrations.AlterModelOptions(
            name='information',
            options={'verbose_name': 'Information'},
        ),
        migrations.AlterField(
            model_name='information',
            name='zipcode',
            field=models.CharField(max_length=6, default=''),
        ),
    ]
