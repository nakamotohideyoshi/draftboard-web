# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rakepaid', '0003_loyaltystatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerTier',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.ForeignKey(to='rakepaid.LoyaltyStatus')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
