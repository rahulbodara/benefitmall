# Generated by Django 3.0.4 on 2020-03-17 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0013_merge_20191205_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='show_breadcrumbs',
            field=models.BooleanField(default=False, help_text='Check this box if you want breadcrumbs on this site.', verbose_name='Show Breadcrumbs'),
        ),
    ]
