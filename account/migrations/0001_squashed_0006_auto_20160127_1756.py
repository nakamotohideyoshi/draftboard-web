# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# account.migrations.0004_auth_users
# account.migrations.0005_emailnotification_displayed_text

from django.db import models, migrations
from django.conf import settings
from django.contrib.auth.hashers import make_password

def load_initial_users(apps, schema_editor):
    """
    Loads the initial Auth Users(s). This function will be passed to 'migrations.RunPython' which supplies the arguments.

    :param apps:
    :param schema_editor:
    :return:
    """


    #
    # get the model by name
    User = apps.get_model('auth', 'User')
    password = User.objects.make_random_password()


    draftboard = User()
    draftboard.username= settings.USERNAME_DRAFTBOARD
    draftboard.password = make_password(password)
    draftboard.is_superuser = False
    draftboard.is_staff = True
    draftboard.save()

    escrow = User()
    escrow.username = settings.USERNAME_ESCROW
    escrow.password= make_password(password)
    escrow.is_superuser = False
    escrow.is_staff = True
    escrow.save()

def load_initial_data(apps, schema_editor):
    """
    adds

    :param apps:
    :param schema_editor:
    :return:
    """

    data = [
        {
            'category'      : 'contest',
            'name'          : 'starting',
            'description'   : 'contest have started',
            'displayed_text': 'Contests are starting',
            'default_value' : True,
            'deprecated'    : False
        },
        {
            'category'      : 'contest',
            'name'          : 'prizes-paid',
            'description'   : 'user has won money from contests',
            'displayed_text': 'Contest victories',
            'default_value' : True,
            'deprecated'    : False
        },
        {
            'category'      : 'campaign',
            'name'          : 'newsletter',
            'description'   : 'whether to send the newsletter',
            'displayed_text': 'Newsletter',
            'default_value' : True,
            'deprecated'    : False
        },
        {
            'category'      : 'contest',
            'name'          : 'starting-soon',
            'description'   : 'user has contests which are starting soon',
            'displayed_text': 'Upcoming contests',
            'default_value' : True,
            'deprecated'    : False
        },
    ]

    # get the model by name
    EmailNotification = apps.get_model('account', 'EmailNotification')

    for obj in data:

        try:
            n = EmailNotification.objects.get( category=obj['category'],
                                               name=obj['name'])
        except EmailNotification.DoesNotExist:
            n = EmailNotification()

            #
            # set the data['fields'] to the email notification
            n.category          = obj['category']
            n.name              = obj['name']
            n.description       = obj['description']
            n.displayed_text    = obj['displayed_text']
            n.default_value     = obj['default_value']
            n.deprecated        = obj['deprecated']
            n.save()

class Migration(migrations.Migration):

    replaces = [('account', '0001_initial'), ('account', '0002_auto_20150418_0110'), ('account', '0003_auto_20150428_0038'), ('account', '0004_auth_users'), ('account', '0005_emailnotification_displayed_text'), ('account', '0006_auto_20160127_1756')]

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('category', models.CharField(default='', choices=[('contest', 'Contest'), ('campaign', 'Campaign')], max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=255)),
                ('default_value', models.BooleanField(default=True)),
                ('deprecated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('fullname', models.CharField(default='', max_length=100)),
                ('address1', models.CharField(default='', max_length=255)),
                ('address2', models.CharField(default='', max_length=255)),
                ('city', models.CharField(default='', max_length=64)),
                ('state', models.CharField(default='', choices=[('NH', 'NH'), ('CA', 'CA'), ('FL', 'FL')], max_length=2)),
                ('zipcode', models.CharField(default='', max_length=5)),
                ('dob', models.DateField(null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='UserEmailNotification',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
        migrations.AlterField(
            model_name='information',
            name='address2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),

        # load the administrative accounts before any users get in there
        migrations.RunPython( load_initial_users ),

        migrations.AddField(
            model_name='emailnotification',
            name='displayed_text',
            field=models.CharField(default='', max_length=512, help_text='this text is shown to users'),
        ),

        # additionally, run function to load the initial objects
        migrations.RunPython( load_initial_data ),

        migrations.AlterModelOptions(
            name='emailnotification',
            options={'verbose_name': 'Email Notification'},
        ),
        migrations.AlterModelOptions(
            name='information',
            options={'verbose_name': 'Information'},
        ),
        migrations.AlterField(
            model_name='information',
            name='zipcode',
            field=models.CharField(default='', max_length=6),
        ),
    ]
