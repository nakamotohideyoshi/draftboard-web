# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promocode', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirstDeposit',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('enabled', models.BooleanField(default=True)),
                ('code', models.CharField(default='', unique=True, max_length=16)),
                ('description', models.CharField(default='', help_text='This text may be displayed on the site.', max_length=20148)),
                ('admin_notes', models.CharField(default='', help_text='make any internal notes here. dont show this to users', max_length=20148)),
                ('expires', models.DateTimeField()),
                ('max_bonuscash', models.DecimalField(default=0, decimal_places=2, help_text='the max amount of bonuscash the site will match, ie: $600', max_digits=20)),
                ('fpp_per_bonus_dollar', models.FloatField(default=0, help_text='number of FPP (ie:rake) that have to be earned for $1 of bonuscash to convert to real cash.')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
