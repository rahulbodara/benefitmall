# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-31 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='background_color',
            field=models.TextField(blank=True, default='', help_text='The overall background color of the app.', null=True, verbose_name='Background Color'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='display',
            field=models.CharField(choices=[('fullscreen', 'fullscreen'), ('standalone', 'standalone'), ('browser', 'browser')], default='standalone', help_text='Display type for the app', max_length=16, verbose_name='Display'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='orientation',
            field=models.CharField(choices=[('user-selected', 'user-selected'), ('portrait', 'portrait'), ('landscape', 'landscape')], default='user-selected', help_text='Orientation of the app (generally should be left to user selected).', max_length=16, verbose_name='Display'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='pwa_name',
            field=models.TextField(blank=True, default='', help_text='The full name of the site.', null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='pwa_short_name',
            field=models.TextField(blank=True, default='', help_text='The short name of the site.', null=True, verbose_name='Short Name'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='scope',
            field=models.TextField(blank=True, default='', help_text='The scope of the app. In most cases should be root of the site. Start URL must be in the scope.', null=True, verbose_name='Scope'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='start_url',
            field=models.TextField(blank=True, default='', help_text='The relative path from which the app should start when opened.', null=True, verbose_name='Start URL'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='theme_color',
            field=models.TextField(blank=True, default='', help_text='The theme_color sets the color of the tool bar, and may be reflected in the app&rsquo;s preview in task switchers.', null=True, verbose_name='Theme Color'),
        ),
    ]
