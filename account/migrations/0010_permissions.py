# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-03 10:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20161028_0029'),
    ]

    def forward(apps, schema_editor):
        Group = apps.get_model('auth', 'group')
        Permission = apps.get_model('auth', 'permission')
        User = apps.get_model('auth', 'user')
        ContentType = apps.get_model('contenttypes', 'contenttype')
        group = Group(name="feature-access_subdomains")
        group.save()
        c_type = ContentType.objects.get_for_model(User)
        permission = Permission(
            codename="access_subdomains",
            content_type=c_type,
            name='Can access all subdomain sites'
        )
        permission.save()
        group.permissions.add(permission)

    def backward(apps, schema_editor):
        Group = apps.get_model('auth', 'group')
        Group.objects.filter(name="feature-access_subdomains").delete()


    operations = [
        migrations.RunPython(
            forward,
            backward
        ),
    ]
