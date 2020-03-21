# Generated by Django 3.0.4 on 2020-03-18 22:37

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_auto_20200318_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='address_city',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='event',
            name='address_line_1',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Address Line 1'),
        ),
        migrations.AlterField(
            model_name='event',
            name='address_line_2',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Address Line 2'),
        ),
        migrations.AlterField(
            model_name='event',
            name='address_state',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='event',
            name='address_zipcode',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=wagtail.core.fields.RichTextField(default='', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, help_text='In hours', max_digits=4, null=True, verbose_name='Duration'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('benefits_meeting', 'Benefits Meeting'), ('benefits_training', 'Benefits Training'), ('webcast', 'Compliance Webcast'), ('tradeshow', 'Tradeshow')], default='', max_length=24, verbose_name='Event Type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_type',
            field=models.CharField(choices=[('online', 'Online'), ('in_person', 'In Person')], default='', help_text='If online, no address is necessary', max_length=24, verbose_name='Location Type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_datetime',
            field=models.DateTimeField(help_text='The date and time the event starts.', verbose_name='Date & Time'),
        ),
    ]