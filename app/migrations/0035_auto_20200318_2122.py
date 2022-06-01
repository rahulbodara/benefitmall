# Generated by Django 3.0.4 on 2020-03-18 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20200318_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location_type',
            field=models.CharField(choices=[('online', 'Online'), ('in_person', 'In Person')], default='', help_text='If online, no address is necessary', max_length=24),
        ),
    ]
