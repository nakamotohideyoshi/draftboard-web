# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

def load_initial_email_notification(apps, scheme_editor):
    """
    Loads the initial EmailNotification(s). this function will be passed to 'migrations.RunPython' which supplies the arguments

    :param apps:
    :param scheme_editor:
    :return:
    """
    email_notifs = [
      {
        "pk": 1,
        "model": "account.emailnotification",
        "fields":
          {
            "category": "contest",
            "description": "Contests are starting",
            "name": "starting",
            "deprecated": False,
            "default_value": True
          }
      },
      {
        "pk": 2,
        "model": "account.emailnotification",
        "fields":
          {
            "category": "contest",
            "description": "Contests victories",
            "name": "victories",
            "deprecated": False,
            "default_value": True
          }
      },
      {
        "pk": 3,
        "model": "account.emailnotification",
        "fields":
          {
            "category": "campaign",
            "description": "Newsletter",
            "name": "newsletter",
            "deprecated": False,
            "default_value": True
          }
      },
      {
        "pk": 4,
        "model": "account.emailnotification",
        "fields":
          {
            "category": "campaign",
            "description": "Upcoming Contest",
            "name": "upcoming-contest",
            "deprecated": False,
            "default_value": True
          }
      }
    ]

    #
    # get the model by name
    EmailNotification = apps.get_model('account', 'EmailNotification')

    #
    # create the "fixtures" -- the 1.8 way, ie: programmatically
    for data in email_notifs:
        fields = data['fields']
        try:
            en = EmailNotification.objects.get( pk=data['pk'] )
        except EmailNotification.DoesNotExist:
            en = EmailNotification()

        #
        # set the data['fields'] to the email notification
        en.category         = fields['category']
        en.description      = fields['description']
        en.name             = fields['name']
        en.deprecated       = fields['deprecated']
        en.default_value    = fields['category']
        en.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('category', models.CharField(default='', max_length=100, choices=[('contest', 'Contest'), ('campaign', 'Campaign')])),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=255)),
                ('default_value', models.BooleanField(default=True)),
                ('deprecated', models.BooleanField(default=False)),
                ('caleb_temp1', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('fullname', models.CharField(default='', max_length=100)),
                ('address1', models.CharField(default='', max_length=255)),
                ('address2', models.CharField(default='', max_length=255)),
                ('city', models.CharField(default='', max_length=64)),
                ('state', models.CharField(default='', max_length=2, choices=[('NH', 'NH'), ('CA', 'CA'), ('FL', 'FL')])),
                ('zipcode', models.CharField(default='', max_length=5)),
                ('dob', models.DateField(default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserEmailNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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

        #
        # additionally, run function to load the initial objects
        migrations.RunPython( load_initial_email_notification )
    ]
