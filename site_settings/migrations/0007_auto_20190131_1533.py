# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-31 21:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0006_auto_20190131_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesettings',
            name='pwa_icon_large',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='pwa_icon_small',
        ),
    ]
