# Generated by Django 3.0.5 on 2020-05-21 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0088_auto_20200508_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='summary',
            field=models.TextField(default='', max_length=300, verbose_name='Summary'),
        ),
    ]
