# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-12 17:24
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_headerfooter_header_banner_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='headerfooter',
            name='footer_category_links',
            field=wagtail.core.fields.StreamField([('footer_category_link_block', wagtail.core.blocks.StructBlock([('category_label', wagtail.core.blocks.CharBlock(label='URL', required=False))]))], blank=True, help_text='Populate the footer with categorized links', null=True, verbose_name='Categorized Links'),
        ),
    ]
