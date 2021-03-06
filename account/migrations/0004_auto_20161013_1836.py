# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-13 18:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_day', models.PositiveSmallIntegerField()),
                ('birth_month', models.PositiveSmallIntegerField()),
                ('birth_year', models.PositiveSmallIntegerField()),
                ('postal_code', models.CharField(max_length=16)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Trulioo User Identity',
            },
        ),
        migrations.AlterField(
            model_name='userlog',
            name='action',
            field=models.SmallIntegerField(choices=[(0, 'Country check failed'), (1, 'State check failed'), (2, 'VPN check failed'), (3, 'IP check status'), (4, 'IP check bypassed, user on local network'), (5, 'User Login'), (6, 'Lineup creation'), (7, 'Lineup edited'), (8, 'Contest entered'), (9, 'Contest deregistered'), (10, 'Deposit funds'), (11, 'Deposit pageview'), (12, 'Withdraw request - paypal'), (13, 'Trulioo verification failed'), (14, 'Trulioo verification success'), (15, 'User identity is already claimed.')]),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Location verification'), (1, 'Contest actions'), (2, 'User funds actions'), (3, 'User authenntication')]),
        ),
    ]
