# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-31 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0005_auto_20190131_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='pwa_icon_large',
            field=models.ImageField(blank=True, help_text='This icon should be a 512x512 pixel png file', null=True, upload_to='', verbose_name='Large Icon'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='pwa_icon_small',
            field=models.ImageField(blank=True, help_text='This icon should be a 192x192 pixel png file', null=True, upload_to='', verbose_name='Small Icon'),
        ),
    ]
