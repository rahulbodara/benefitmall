# Generated by Django 3.0.4 on 2020-03-25 21:22

import app.blocks.custom_choice_block
import app.widgets.custom_radio_select
from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_headerfooter_utility_nav'),
    ]

    operations = [
        migrations.AddField(
            model_name='headerfooter',
            name='header_utility_nav',
            field=models.BooleanField(default=True, help_text='Add Utility Nav Bar', verbose_name='Utility Nav'),
        ),
        migrations.AlterField(
            model_name='headerfooter',
            name='utility_nav',
            field=wagtail.core.fields.StreamField([('utility_link', wagtail.core.blocks.StructBlock([('link_type', app.blocks.custom_choice_block.CustomChoiceBlock(choices=(('', 'None'), ('url', 'URL'), ('page', 'Page'), ('document', 'Document'), ('email', 'Email'), ('phone', 'Phone')), default='', label='Type', required=False, widget=app.widgets.custom_radio_select.CustomRadioSelect)), ('url', wagtail.core.blocks.CharBlock(label='URL', required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('email', wagtail.core.blocks.EmailBlock(required=False)), ('phone', wagtail.core.blocks.CharBlock(required=False)), ('link_text', wagtail.core.blocks.CharBlock(label='Text', required=False)), ('link_format', app.blocks.custom_choice_block.CustomChoiceBlock(choices=(('', 'Text'), ('btn btn--primary', 'Button')), default='', label='Format', required=False, widget=app.widgets.custom_radio_select.CustomRadioSelect))])), ('utility_text', wagtail.core.blocks.CharBlock())], blank=True, help_text='Populate the utility nav with links and text', null=True, verbose_name='Utility Links'),
        ),
    ]