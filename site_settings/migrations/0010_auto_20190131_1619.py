# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-31 22:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('site_settings', '0009_auto_20190131_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='apple_touch_icon',
            field=models.ForeignKey(blank=True, help_text='The apple touch icon should be 114 x 114 or 144 x 144, and a png file.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='large_icon', to='wagtailimages.Image', verbose_name='Apple Touch Icon'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='favicon_ico',
            field=models.ForeignKey(blank=True, help_text='The favicon must be 16x16 pixels or 32x32 pixels, using either 8-bit or 24-bit colors. The format of the image must be one of PNG (a W3C standard), GIF, or ICO.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favicon', to='wagtailimages.Image', verbose_name='Favicon'),
        ),
    ]
