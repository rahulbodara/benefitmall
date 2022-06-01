# Generated by Django 3.0.4 on 2020-03-27 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0065_auto_20200326_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventindexpage',
            name='email_enabled_global',
            field=models.BooleanField(default=False, help_text='Check to enable sending registration emails. This is the default global setting for all events, but can be individually configured per event.', verbose_name='Send Registration Emails'),
        ),
        migrations.AddField(
            model_name='eventindexpage',
            name='email_recipients_global',
            field=models.CharField(blank=True, help_text='Add registration email recipients separated by commas. This is the default global setting for all events.', max_length=200, null=True, verbose_name='Email Recipients'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='email_recipients',
            field=models.CharField(blank=True, help_text='Add registration email recipients separated by commas. This overrides the default global setting.', max_length=200, null=True, verbose_name='Email Recipients'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='email_setting',
            field=models.CharField(blank=True, choices=[('', '-- Use Default Global Setting --'), ('enabled', 'Enabled'), ('disabled', 'Disabled')], default='', help_text='Select a setting for sending registration emails. This overrides the default global setting', max_length=20, verbose_name='Send Registration Email'),
        ),
    ]
