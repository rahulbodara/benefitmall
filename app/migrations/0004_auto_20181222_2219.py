# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-22 22:19
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20181222_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorpages',
            name='body_404',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='errorpages',
            name='body_500',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='errorpages',
            name='title_404',
            field=models.TextField(blank=True, default='404 not found', null=True),
        ),
        migrations.AlterField(
            model_name='errorpages',
            name='title_500',
            field=models.TextField(blank=True, default='500 Server Error', null=True),
        ),
    ]
