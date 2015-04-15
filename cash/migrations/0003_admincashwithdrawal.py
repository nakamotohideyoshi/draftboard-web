# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cash', '0002_auto_20150409_0245'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCashWithdrawal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, default=0)),
                ('reason', models.CharField(blank=True, max_length=255, default='')),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('user', models.ForeignKey(related_name='admincashwithdrawal_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
