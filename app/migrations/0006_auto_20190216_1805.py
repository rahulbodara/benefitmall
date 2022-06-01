# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-16 18:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('app', '0005_auto_20181223_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultpage',
            name='canonical_url',
            field=models.CharField(blank=True, help_text='Leave this blank unless you know there is a canonical URL for this content.', max_length=255, null=True, verbose_name='Canonical URL'),
        ),
        migrations.AddField(
            model_name='defaultpage',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta Keywords'),
        ),
        migrations.AddField(
            model_name='defaultpage',
            name='og_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='OG:Description'),
        ),
        migrations.AddField(
            model_name='defaultpage',
            name='og_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_og_image', to='wagtailimages.Image', verbose_name='OG:Image'),
        ),
        migrations.AddField(
            model_name='defaultpage',
            name='og_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='OG:Title'),
        ),
        migrations.AddField(
            model_name='defaultpage',
            name='og_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='OG:Type'),
        ),
        migrations.AddField(
            model_name='defaultpage',
            name='og_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='OG:URL'),
        ),
    ]
