# Generated by Django 3.0.5 on 2020-05-21 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0089_eventpage_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='require_registration',
            field=models.BooleanField(default=False, verbose_name='Requires Registration'),
        ),
    ]
