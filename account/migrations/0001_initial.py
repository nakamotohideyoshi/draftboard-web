# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('category', models.CharField(default='', max_length=100, choices=[('contest', 'Contest'), ('campaign', 'Campaign')])),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=255)),
                ('default_value', models.BooleanField(default=True)),
                ('deprecated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('fullname', models.CharField(default='', max_length=100)),
                ('address1', models.CharField(default='', max_length=255)),
                ('address2', models.CharField(default='', max_length=255)),
                ('city', models.CharField(default='', max_length=64)),
                ('state', models.CharField(default='', max_length=2, choices=[('NH', 'NH'), ('CA', 'CA'), ('FL', 'FL')])),
                ('zipcode', models.CharField(default='', max_length=5)),
                ('dob', models.DateField(default='', null=True)),
                ('user', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEmailNotification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('email_notification', models.ForeignKey(to='account.EmailNotification')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='emailnotification',
            unique_together=set([('category', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='useremailnotification',
            unique_together=set([('user', 'email_notification')]),
        ),
    ]
