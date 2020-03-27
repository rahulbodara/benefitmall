# Generated by Django 3.0.4 on 2020-03-26 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0014_sitesettings_show_breadcrumbs'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='show_search',
            field=models.BooleanField(default=False, help_text='Check this box if you want global search on this site.', verbose_name='Show Search'),
        ),
    ]
