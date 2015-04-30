# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('contest', 'Contest'), ('campaign', 'Campaign')], default='', max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=255)),
                ('default_value', models.BooleanField(default=True)),
                ('deprecated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fullname', models.CharField(default='', max_length=100)),
                ('address1', models.CharField(default='', max_length=255)),
                ('address2', models.CharField(default='', max_length=255)),
                ('city', models.CharField(default='', max_length=64)),
                ('state', models.CharField(choices=[('NH', 'NH'), ('CA', 'CA'), ('FL', 'FL')], default='', max_length=2)),
                ('zipcode', models.CharField(default='', max_length=5)),
                ('dob', models.DateField(null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='UserEmailNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
