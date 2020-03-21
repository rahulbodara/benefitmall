# Generated by Django 3.0.4 on 2020-03-18 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20200318_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end_datetime',
        ),
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.DecimalField(decimal_places=2, default=1, help_text='In hours', max_digits=4),
        ),
    ]