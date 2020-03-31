# Generated by Django 3.0.4 on 2020-03-25 21:10

import app.blocks.custom_choice_block
import app.widgets.custom_radio_select
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_auto_20200325_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='headerfooter',
            name='utility_nav',
            field=wagtail.core.fields.StreamField([('header_link_block', wagtail.core.blocks.StructBlock([('link', wagtail.core.blocks.StructBlock([('link_type', app.blocks.custom_choice_block.CustomChoiceBlock(choices=(('url', 'URL'), ('page', 'Page'), ('document', 'Document'), ('email', 'Email')), default='url', label='Type', required=False, widget=app.widgets.custom_radio_select.CustomRadioSelect)), ('url', wagtail.core.blocks.CharBlock(label='URL', required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('email', wagtail.core.blocks.EmailBlock(required=False)), ('phone', wagtail.core.blocks.CharBlock(required=False)), ('link_text', wagtail.core.blocks.CharBlock(label='Text', required=False)), ('children', wagtail.core.blocks.StreamBlock([('link', wagtail.core.blocks.StructBlock([('link_type', app.blocks.custom_choice_block.CustomChoiceBlock(choices=(('url', 'URL'), ('page', 'Page'), ('document', 'Document'), ('email', 'Email')), default='url', label='Type', required=False, widget=app.widgets.custom_radio_select.CustomRadioSelect)), ('url', wagtail.core.blocks.CharBlock(label='URL', required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('email', wagtail.core.blocks.EmailBlock(required=False)), ('phone', wagtail.core.blocks.CharBlock(required=False)), ('link_text', wagtail.core.blocks.CharBlock(label='Text', required=False))]))], blank=True, null=True, required=False))]))]))], blank=True, help_text='Populate the utility nav with custom links', null=True, verbose_name='Links'),
        ),
    ]
