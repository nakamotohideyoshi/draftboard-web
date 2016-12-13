# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-13 13:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_auto_20161017_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Limit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(0, 'Deposit Limit'), (1, 'Contest Entry Alert'), (2, 'Contest Entry Limit'), (3, 'Entry Fee Limit')])),
                ('value', models.IntegerField(blank=True, choices=[(0, '$50'), (1, '$100'), (2, '$250'), (3, '$500'), (4, '$750'), (5, '$1000')])),
                ('time_period', models.SmallIntegerField(choices=[(0, 'Monthly')])),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='limits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='userlog',
            name='action',
            field=models.SmallIntegerField(choices=[(0, 'Country check failed'), (1, 'State check failed'), (2, 'VPN check failed'), (3, 'IP check status'), (4, 'IP check bypassed, user on local network'), (5, 'User Login'), (6, 'Lineup creation'), (7, 'Lineup edited'), (8, 'Contest entered'), (9, 'Contest deregistered'), (10, 'Deposit funds'), (11, 'Deposit pageview'), (12, 'Withdraw request - paypal'), (13, 'Trulioo verification failed'), (14, 'Trulioo verification success'), (15, 'User identity is already claimed'), (16, 'IP not found in the db')]),
        ),
    ]
