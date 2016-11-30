# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-27 22:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0006_auto_20160127_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedCardDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(max_length=256)),
                ('type', models.CharField(choices=[('amex', 'AmericanExpress'), ('discover', 'Discover'), ('mastercard', 'MasterCard'), ('visa', 'Visa')], max_length=32)),
                ('last_4', models.CharField(max_length=4)),
                ('exp_month', models.IntegerField(default=0)),
                ('exp_year', models.IntegerField(default=0)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='savedcarddetails',
            unique_together=set([('user', 'token')]),
        ),
    ]
