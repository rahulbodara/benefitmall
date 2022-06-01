# Generated by Django 3.0.5 on 2020-05-04 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0081_auto_20200504_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headerfooter',
            name='copyright_text',
            field=models.CharField(blank=True, default='', help_text='Enter the text that should appear after the year in the copyright line.', max_length=512, null=True, verbose_name='Copyright text'),
        ),
    ]
