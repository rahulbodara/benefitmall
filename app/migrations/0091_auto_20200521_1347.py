# Generated by Django 3.0.5 on 2020-05-21 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0090_eventpage_require_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='summary',
            field=models.TextField(blank=True, default='', max_length=300, null=True, verbose_name='Summary'),
        ),
    ]
