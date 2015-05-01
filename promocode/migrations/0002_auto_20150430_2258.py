# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promocode', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('code', models.CharField(max_length=16, default='', help_text='the code you want users to enter for the promo, ie: "DFS600"', unique=True)),
                ('first_deposit_only', models.BooleanField(default=True, help_text='should we limit this promotion to ONLY first time depositors?')),
                ('description', models.CharField(max_length=2048, default='', help_text='This text may be displayed on the site.')),
                ('admin_notes', models.CharField(max_length=2048, default='', help_text='make any internal notes here. dont show this to users')),
                ('expires', models.DateTimeField(blank=True, null=True, default=None, help_text='leave blank if you dont want it to ever expire')),
                ('max_bonuscash', models.DecimalField(help_text='the max amount of bonuscash the site will match up to, ie: $600', default=0, decimal_places=2, max_digits=20)),
                ('fpp_per_bonus_dollar', models.FloatField(help_text='number of FPP (ie:rake) that have to be earned for $1 of bonuscash to convert to real cash.', default=0)),
            ],
        ),
        migrations.AddField(
            model_name='promocode',
            name='promotion',
            field=models.ForeignKey(to='promocode.Promotion'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='transaction',
            field=models.ForeignKey(to='transaction.Transaction'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
