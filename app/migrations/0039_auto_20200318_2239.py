# Generated by Django 3.0.4 on 2020-03-18 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_auto_20200318_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='cost',
            field=models.CharField(default='Free', help_text='If adding a price, please use the currency symbol, e.g. $, £, etc.', max_length=50),
        ),
    ]
