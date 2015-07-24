# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('contest', '0010_auto_20150722_1328'),
        ('buyin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyin',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('entry', models.OneToOneField(to='contest.Entry')),
                ('transaction', models.OneToOneField(to='transaction.Transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
